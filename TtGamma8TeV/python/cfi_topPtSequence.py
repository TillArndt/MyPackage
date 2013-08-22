
import FWCore.ParameterSet.Config as cms

topPtTTbar          = cms.EDProducer("TopPtProducer")
topPtWeight         = cms.EDProducer("TopPtWeight")
topPtHistoVanilla   = cms.EDAnalyzer("TopPtHisto")
topPtHistoWeighted  = cms.EDAnalyzer("TopPtHisto",
    weights = cms.untracked.InputTag("topPtWeight"),
)

topPtSequenceTTBar = cms.Sequence(
    topPtTTbar
    * topPtWeight
    * topPtHistoVanilla
    * topPtHistoWeighted
)
