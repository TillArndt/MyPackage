import FWCore.ParameterSet.Config as cms

myBTagRequirement = cms.EDFilter(
    "PATJetRefSelector",
    src = cms.InputTag("myGoodJets"),
    cut = cms.string('bDiscriminator("combinedSecondaryVertexBJetTags") > 0.679'),
    filter = cms.bool(True)
)


