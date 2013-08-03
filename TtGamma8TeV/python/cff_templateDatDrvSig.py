
import FWCore.ParameterSet.Config as cms
from MyPackage.TtGamma8TeV.cff_photonIDCuts import make_histo_analyzer, cuts

photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("tightPhoton"),
    cut = cms.string("(hadTowOverEm<0.05) && (max(neutralHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_neutral')), 0.) < (0.4 + 0.04*pt))"),
    filter = cms.bool(False)
)

photonsWithSihihCut = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("photonInputDummy"),
#    cut = cms.string("sigmaIetaIeta<0.011"),
    cut = cms.string(""),
    filter = cms.bool(False)
)

photonsWithChHadIsoCut = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("photonInputDummy"),
#    cut = cms.string("max(chargedHadronIso - (userFloat('kt6pf_rho')*userFloat('EA_charged')), 0.) < 0.7"),
    cut = cms.string(""),
    filter = cms.bool(False)
)

photonSigTemplateSihih = make_histo_analyzer(
    "photonsWithSihihCut",
    cuts["chargedHadronIsoEB"]
)

photonSigTemplateChHadIso = make_histo_analyzer(
    "photonsWithChHadIsoCut",
    cuts["sihihEB"]
)

signalTemplateSequence = cms.Sequence(
    photonInputDummy
    * photonsWithSihihCut
    * photonsWithChHadIsoCut
    * photonSigTemplateSihih
    * photonSigTemplateChHadIso
)

from MyPackage.TtGamma8TeV.cff_templateCreation import \
    realPhotonsSihih, \
    realPhotonsChHadIso, \
    fakePhotonsSihih, \
    fakePhotonsChHadIso

realPhotonsSihih.src = "photonsWithChHadIsoCut"
realPhotonsChHadIso.src = "photonsWithSihihCut"
fakePhotonsSihih.src = "photonsWithChHadIsoCut"
fakePhotonsChHadIso.src = "photonsWithSihihCut"

signalTemplateTruthSequence = cms.Sequence(
    realPhotonsSihih
    * realPhotonsChHadIso
    * fakePhotonsSihih
    * fakePhotonsChHadIso
)