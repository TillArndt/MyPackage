
import FWCore.ParameterSet.Config as cms


DataMCJetCheckTrue = cms.EDAnalyzer("checkObject",
    srcPUWeight = cms.InputTag("weightComb"),
	bTagAlgorithm = cms.string("combinedSecondaryVertexBJetTags"),
	srcObjects = cms.InputTag("selectedPatJetsForAnalysis20"),
	objectType = cms.string("patJet")
)

DataMCMuonCheckTrue = cms.EDAnalyzer("checkObject",
    srcPUWeight = cms.InputTag("weightComb"),
	bTagAlgorithm = cms.string("blabla"),
	srcObjects = cms.InputTag("tightmuons"),
	objectType = cms.string("patMuon")
)

dataMCSequence = cms.Sequence(
    DataMCMuonCheckTrue *
    DataMCJetCheckTrue
)
