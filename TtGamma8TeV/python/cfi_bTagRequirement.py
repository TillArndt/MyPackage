

import FWCore.ParameterSet.Config as cms

bTagRequirement = cms.EDFilter(
    "PATJetRefSelector",
    src = cms.InputTag("selectedPatJetsForAnalysis20"),
    cut = cms.string('bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679'),
    filter = cms.bool(False)
)

bTagCounter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("bTagRequirement"),
    maxNumber = cms.uint32(10000),
    minNumber = cms.uint32(1)
)

bTagSequence = cms.Sequence(
    bTagRequirement *
    bTagCounter
)