

import cff_photonIDCuts as pho_cuts
from cff_templateCreation import prompt as prompt_photon_cut_str

import FWCore.ParameterSet.Config as cms

# change charged hadron isolation cut according to shilpi's method
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/PhotonFakeRateLstar
cuts = pho_cuts.cuts_for_plot
chhadiso_tuple = list(cuts["chargedHadronIsoEB"])
chhadiso_cut = chhadiso_tuple[-1]
chhadiso_tuple[0] = chhadiso_cut + " > 2.0 && 6.0 > " + chhadiso_cut
cuts["chargedHadronIsoEBInv"] = tuple(chhadiso_tuple)
sihih_tuple = list(cuts["sihihEB"])
sihih_cut = sihih_tuple[-1]
sihih_tuple[0] = sihih_cut + " > 0.012 && 2.0 > " + sihih_cut
cuts["sihihEBInv"] = tuple(sihih_tuple)

cut_key_order = pho_cuts.cut_key_order[:]
cut_key_order.remove("chargedHadronIsoEB")
cut_key_order.remove("sihihEB")
cut_key_order.remove("drjet")


def add_nm2_path_core(process):
    ################################################# path for bkg template ###
    # Additionally make a path where neither chhadiso nor sihih is applied
    cutkeys_Nm2 = cut_key_order[:]
    cuts_Nm2_list = list(cuts[cutkey][0] for cutkey in cutkeys_Nm2)
    cuts_Nm2_str = "( " + ") && (".join(cuts_Nm2_list) + " )"

    # Filter for n - 1 plot
    process.Nm2Filt = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut = cms.string(cuts_Nm2_str),
        filter = cms.bool(False)
    )

    # Take only one photon per event (photons are pt-ordered)
    process.Nm2FirstPhoton = cms.EDProducer("FirstPhotonPicker",
        src = cms.InputTag("Nm2Filt")
    )

    # n - 2 Plot
    process.Nm2PlotsihihEB = pho_cuts.make_histo_analyzer(
        "Nm2FirstPhoton",
        cuts["sihihEB"]
    )
    process.Nm2PlotchargedHadronIsoEB = pho_cuts.make_histo_analyzer(
        "Nm2FirstPhoton",
        cuts["chargedHadronIsoEB"]
    )

    process.pathNm2Core = cms.Path(
        process.preSel
        * process.Nm2Filt
        * process.Nm2FirstPhoton
        * process.Nm2PlotsihihEB
        * process.Nm2PlotchargedHadronIsoEB
    )
    return [process.pathNm2Core]

def add_nm2_path(process):

    paths = add_nm2_path_core(process)

    # divide into matched photons classes
    process.Nm2realPhotons = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("Nm2FirstPhoton"),
        cut = cms.string(prompt_photon_cut_str),
        filter = cms.bool(False)
    )
    process.Nm2fakePhotons = process.Nm2realPhotons.clone(
        cut = cms.string('!(' + prompt_photon_cut_str + ')')
    )

    # n-2 Plots after real and fake filters
    process.realNm2PlotsihihEB = process.Nm2PlotsihihEB.clone(
        src = cms.InputTag("Nm2realPhotons")
    )
    process.fakeNm2PlotsihihEB = process.Nm2PlotsihihEB.clone(
        src = cms.InputTag("Nm2fakePhotons")
    )
    process.realNm2PlotchargedHadronIsoEB = process.Nm2PlotchargedHadronIsoEB.clone(
        src = cms.InputTag("Nm2realPhotons")
    )
    process.fakeNm2PlotchargedHadronIsoEB = process.Nm2PlotchargedHadronIsoEB.clone(
        src = cms.InputTag("Nm2fakePhotons")
    )

    # make path
    process.Nm2TemplateSequence = cms.Sequence(
        process.Nm2realPhotons
        * process.Nm2fakePhotons
        * process.realNm2PlotsihihEB
        * process.fakeNm2PlotsihihEB
        * process.realNm2PlotchargedHadronIsoEB
        * process.fakeNm2PlotchargedHadronIsoEB
    )

    paths[0] *= process.Nm2TemplateSequence
    return paths


def add_bkg_template_path(process):

    ###################################################### inverse chhadiso ###
    # make one cut string for the N-1 plots
    cutkeys_Nm1 = cut_key_order[:]
    cutkeys_Nm1.append("chargedHadronIsoEBInv")
    cuts_Nm1_list = list(cuts[cutkey][0] for cutkey in cutkeys_Nm1)
    cuts_Nm1_str = "(" + ") && (".join(cuts_Nm1_list) + ")"

    # Filter for inverse n - 1 plots
    process.Nm1FiltChHadIsoInv = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut = cms.string(cuts_Nm1_str),
        filter = cms.bool(False)
    )

    # Take only one photon per event (photons are pt-ordered)
    process.Nm1FirstPhotonChHadIsoInv = cms.EDProducer("FirstPhotonPicker",
        src = cms.InputTag("Nm1FiltChHadIsoInv")
    )

    # inverse n - 1 Plots
    process.Nm1PlotSihihChHadIsoInv = pho_cuts.make_histo_analyzer(
        "Nm1FirstPhotonChHadIsoInv",
        cuts["sihihEB"]
    )

    ######################################################### inverse sihih ###
    # make one cut string for the N-1 plots
    cutkeys_Nm1 = cut_key_order[:]
    cutkeys_Nm1.append("sihihEBInv")
    cuts_Nm1_list = list(cuts[cutkey][0] for cutkey in cutkeys_Nm1)
    cuts_Nm1_str = "( " + ") && (".join(cuts_Nm1_list) + " )"

    # Filter for inverse n - 1 plots
    process.Nm1FiltSihihInv = cms.EDFilter("PATPhotonSelector",
        src = cms.InputTag("photonInputDummy"),
        cut = cms.string(cuts_Nm1_str),
        filter = cms.bool(False)
    )

    # Take only one photon per event (photons are pt-ordered)
    process.Nm1FirstPhotonSihihInv = cms.EDProducer("FirstPhotonPicker",
        src = cms.InputTag("Nm1FiltSihihInv")
    )

    # inverse n - 1 Plots
    process.Nm1PlotChHadIsoSihihInv = pho_cuts.make_histo_analyzer(
        "Nm1FirstPhotonSihihInv",
        cuts["chargedHadronIsoEB"]
    )

    # make path
    process.pathChHadIsoInv = cms.Path(
        process.preSel
        * process.Nm1FiltChHadIsoInv
        * process.Nm1FirstPhotonChHadIsoInv
        * process.Nm1PlotSihihChHadIsoInv
        * process.Nm1FiltSihihInv
        * process.Nm1FirstPhotonSihihInv
        * process.Nm1PlotChHadIsoSihihInv
    )

    return [process.pathChHadIsoInv]
