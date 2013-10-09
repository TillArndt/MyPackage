
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

# use loose deno id as in shilpi's method
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PhotonFakeRateLstar
cut_keys_nm2 = list(
    c
    for c in pho_cuts.cut_key_order
    if c not in ["sihihEB", "chargedHadronIsoEB"]
)
loose_cuts_list = list(
    pho_cuts.cuts_loose[cutkey][0] for cutkey in cut_keys_nm2
)
loose_cuts_str = "( " + ") && (".join(loose_cuts_list) + " )"


def sihih_sideband_cut(l, h):
    return loose_cuts_str+" && (sigmaIetaIeta>%3f && sigmaIetaIeta<%3f)"%(l, h)
loose_cuts_bkg_str = sihih_sideband_cut(0.015, 0.02)


def add_path_core(process):
    ################################################# path for bkg template ###

    process.FiltLooseIDSihihSB = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut = cms.string(loose_cuts_bkg_str),
        filter = cms.bool(False)
    )

    process.PlotLooseIDSihihSB = pho_cuts.make_histo_analyzer(
        "FiltLooseIDSihihSB",
        pho_cuts.cuts_loose["chargedisoSCFootRmEB"]
    )

    process.pathTmpltLooseID = cms.Path(
        process.preSel
        * process.FiltLooseIDSihihSB
        * process.PlotLooseIDSihihSB
    )

    for i in xrange(12, 20):
        name = "LooseIDSliceSihihSB%02dto%02d"%(i,i+1)
        cut = sihih_sideband_cut(0.001*i, 0.001*(i+1))
        setattr(
            process,
            "Filt"+name,
            process.FiltLooseIDSihihSB.clone(cut=cut)
        )
        setattr(
            process,
            "Plot"+name,
            process.PlotLooseIDSihihSB.clone(src="Filt"+name)
        )
        process.pathTmpltLooseID *= getattr(process, "Filt"+name)
        process.pathTmpltLooseID *= getattr(process, "Plot"+name)


    return [process.pathTmpltLooseID]


def add_path_truth(process):
    ######################################## path for bkg template mc truth ###
    paths = add_path_core(process)

    # divide into matched photons classes
    process.FiltLooseIDSihihSBreal = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("FiltLooseIDSihihSB"),
        cut = cms.string(tmpl_cr.real),
        filter = cms.bool(False)
    )
    process.FiltLooseIDSihihSBfake = process.FiltLooseIDSihihSBreal.clone(
        cut = cms.string(tmpl_cr.fake)
    )

    # n-2 Plots after real and fake filters
    process.PlotLooseIDSihihSBreal = process.PlotLooseIDSihihSB.clone(
        src = cms.InputTag("FiltLooseIDSihihSBreal")
    )
    process.PlotLooseIDSihihSBfake = process.PlotLooseIDSihihSB.clone(
        src = cms.InputTag("FiltLooseIDSihihSBfake")
    )

    # make path
    process.pathTmpltLooseIDTruthSequence = cms.Sequence(
        process.FiltLooseIDSihihSBreal
        * process.FiltLooseIDSihihSBfake
        * process.PlotLooseIDSihihSBreal
        * process.PlotLooseIDSihihSBfake
    )

    paths[0] *= process.pathTmpltLooseIDTruthSequence

    return paths
