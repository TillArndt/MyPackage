import FWCore.ParameterSet.Config as cms


trigWeight = cms.EDProducer("TopTriggerWeight",
    uncertMode = cms.untracked.int32(0),
)

trigWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src = cms.InputTag("trigWeight"),
    name = cms.untracked.string("histo"),
    title = cms.untracked.string(";trigger weight;events"),
    nbins = cms.untracked.int32(100),
    min = cms.untracked.double(0.),
    max = cms.untracked.double(2.),
)

trigWeightSequence = cms.Sequence(
    trigWeight *
    trigWeightHisto
)