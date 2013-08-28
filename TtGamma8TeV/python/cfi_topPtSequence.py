
import FWCore.ParameterSet.Config as cms

topPtTTbar          = cms.EDProducer("TopPtProducer")
topPtWeight         = cms.EDProducer("TopPtWeight")
topPtHistoVanilla   = cms.EDAnalyzer("TopPtHisto")
topPtHistoWeighted  = cms.EDAnalyzer("TopPtHisto",
    weights = cms.untracked.InputTag("topPtWeight"),
)

topPtWeightHisto    = cms.EDAnalyzer("DoubleValueHisto",
    src     = cms.InputTag("topPtWeight"),
    name    = cms.untracked.string("histo"),
    title   = cms.untracked.string(";top quark pt weight;events"),
    nbins   = cms.untracked.int32(50),
    min     = cms.untracked.double(0.),
    max     = cms.untracked.double(2.),
)

topPtSequenceTTBar = cms.Sequence(
    topPtTTbar
    * topPtWeight
    * topPtHistoVanilla
    * topPtHistoWeighted
    * topPtWeightHisto
)
