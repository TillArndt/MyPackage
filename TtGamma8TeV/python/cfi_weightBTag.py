import FWCore.ParameterSet.Config as cms


bTagWeight = cms.EDProducer("BTagWeight",
    src=cms.InputTag("bTagRequirement"),
    weights = cms.untracked.InputTag(""),
    errorModeBC = cms.untracked.int32(0),
    errorModeUDSG = cms.untracked.int32(0),
    twoBTagMode = cms.untracked.bool(False),
)

bTagWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src = cms.InputTag("bTagWeight"),
    name = cms.untracked.string("histo"),
    title = cms.untracked.string(";btag weight;events"),
    nbins = cms.untracked.int32(100),
    min = cms.untracked.double(0.),
    max = cms.untracked.double(2.),
)


bTagWeightSequence = cms.Sequence(
	bTagWeight*
	bTagWeightHisto
)
