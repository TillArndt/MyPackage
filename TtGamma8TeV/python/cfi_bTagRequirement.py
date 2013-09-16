

import FWCore.ParameterSet.Config as cms

bTagRequirement = cms.EDFilter(
    "PATJetSelector",
    src = cms.InputTag("selectedPatJetsForAnalysis20"),
    cut = cms.string('bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679'),
    filter = cms.bool(False)
)

bTagCounter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("bTagRequirement"),
    maxNumber = cms.uint32(10000),
    minNumber = cms.uint32(1),
    filter = cms.bool(True)
)

bTagWeight = cms.EDProducer("BTagWeight",
    src = cms.InputTag("bTagRequirement"),
    weights = cms.untracked.InputTag(""),
    errorMode = cms.untracked.int32(0),
    twoBTagMode = cms.untracked.bool(False),
)

bTagWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src     = cms.InputTag("bTagWeight"),
    name    = cms.untracked.string("histo"),
    title   = cms.untracked.string(";btag weight;events"),
    nbins   = cms.untracked.int32(50),
    min     = cms.untracked.double(0.),
    max     = cms.untracked.double(2.),
)

bTagSequence = cms.Sequence(
    bTagRequirement *
    bTagCounter
)
