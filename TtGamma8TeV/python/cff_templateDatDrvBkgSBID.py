
puWeight    = None
try:
    puWeight    = cms_var.get("puWeight", puWeight)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import cff_photonIDCuts as pho_cuts
import cff_templateCreation as tmpl_cr

import FWCore.ParameterSet.Config as cms
if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)


hoe             = "hadTowOverEm"
sieie           = "sigmaIetaIeta"
pfneutralIso    = "max(neutralHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_neutral')), 0.)"
pfphoIso        = "max(photonIso - (userFloat('kt6pf_rho')*userFloat('EA_photons')), 0.)"

cuthoe          = "0.05"
cutsieie        = "0.012"
cutneutralIso   = "(4.5 + 0.04*pt)"
cutphoIso       = "(4.5 + 0.005*pt)"

maxsieie        = "0.013" # orig: 0.015
maxneutralIso   = "min(0.2*et, 6*" + cutneutralIso  + ")" # orig : 5*cut
maxphoIso       = "min(0.2*et, 1*" + cutphoIso      + ")" # orig : 5*cut
maxhoe          = cuthoe

lower_cut = (
    "( "       + sieie          + ">" + cutsieie
    + ") || (" + pfneutralIso   + ">" + cutneutralIso
    + ") || (" + pfphoIso       + ">" + cutphoIso
    + ")"
    )
upper_cut = (
    "( "       + sieie          + "<" + maxsieie
    + ") && (" + pfneutralIso   + "<" + maxneutralIso
    + ") && (" + pfphoIso       + "<" + maxphoIso
    + ") && (" + hoe            + "<" + maxhoe
    + ")"
    )


def add_path_core(process):
    ################################################# path for bkg template ###

    process.FiltSBID = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut = cms.string(lower_cut+"&&"+upper_cut),
        filter = cms.bool(False)
    )

    process.PlotSBID = pho_cuts.make_histo_analyzer(
        "FiltSBID",
        pho_cuts.cuts_loose["chargedisoSCFootRmEB"]
    )

    process.pathTmpltSBID = cms.Path(
        process.preSel
        * process.FiltSBID
        * process.PlotSBID
    )
    return [process.pathTmpltSBID]

def add_path_truth(process):
    ######################################## path for bkg template mc truth ###
    paths = add_path_core(process)

    # divide into matched photons classes
    process.FiltSBIDreal = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("FiltSBID"),
        cut = cms.string(tmpl_cr.real),
        filter = cms.bool(False)
    )
    process.FiltSBIDfake = process.FiltSBIDreal.clone(
        cut = cms.string(tmpl_cr.fake)
    )

    # n-2 Plots after real and fake filters
    process.PlotSBIDreal = process.PlotSBID.clone(
        src = cms.InputTag("FiltSBIDreal")
    )
    process.PlotSBIDfake = process.PlotSBID.clone(
        src = cms.InputTag("FiltSBIDfake")
    )

    # make path
    process.pathTmpltSBIDTruthSequence = cms.Sequence(
        process.FiltSBIDreal
        * process.FiltSBIDfake
        * process.PlotSBIDreal
        * process.PlotSBIDfake
    )

    paths[0] *= process.pathTmpltSBIDTruthSequence

    return paths


