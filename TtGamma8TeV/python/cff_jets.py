

from MyPackage.TtGamma8TeV.cff_photonIDCuts import make_histo_analyzer
import FWCore.ParameterSet.Config as cms

JetAnaChEmFrac = make_histo_analyzer(
    "selectedPatJetsForAnalysis20",
    ("", 0., 1.1, 80,
     "Jets: neutralEmEnergyFraction", "neutralEmEnergyFraction"),
)

JetAnaChHadFrac = make_histo_analyzer(
    "selectedPatJetsForAnalysis20",
    ("", 0., 1.1, 80,
     "Jets: neutralHadronEnergyFraction","neutralHadronEnergyFraction"),
)

AnalysisJets = cms.EDFilter("PATJetSelector",
    src = cms.InputTag("selectedPatJetsForAnalysis20"),
    cut = cms.string("neutralEmEnergyFraction < 0.75"),
    filter = cms.bool(False)
)

jetSequence = cms.Sequence(
    JetAnaChEmFrac *
    JetAnaChHadFrac *
    AnalysisJets
)
