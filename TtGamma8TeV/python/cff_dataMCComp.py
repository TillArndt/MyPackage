### added by yvi

jetsource  = "selectedPatJetsForAnalysis"
muonsource = "tightmuons"
try:
    jetsource = cms_var.get("jetsource", jetsource)
    muonsource = cms_var.get("muonsource", muonsource)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

DataMCCompPhotonsTrue = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("widenedCocPatPhotons"),
    weights = cms.untracked.InputTag("puWeight", "PUWeightTrue"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(700.),
            nbins        = cms.untracked.int32 (70),
            name         = cms.untracked.string("EtPhotons"),
            description  = cms.untracked.string(";E_{T} / GeV;Number of photons"),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string("et"),
        ),
        cms.PSet(
            min          = cms.untracked.double(-3.),
            max          = cms.untracked.double(3.),
            nbins        = cms.untracked.int32 (70),
            name         = cms.untracked.string("etaPhotons"),
            description  = cms.untracked.string(";#eta;Number of photons"),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string("eta"),
        )
    )
)
#DataMCCompPhotons = DataMCCompPhotonsTrue.clone(
#    weights = cms.untracked.InputTag("puWeight", "PUWeight")
#)
#
#WeightsCheckTrue = cms.EDAnalyzer("checkCorrs",
#    srcPUWeight = cms.InputTag("puWeight", "PUWeightTrue"),
#    srcBTagWeight = cms.InputTag("dummy"),
#    srcVertices = cms.InputTag("goodOfflinePrimaryVertices")
#)
#WeightsCheck = WeightsCheckTrue.clone(
#    srcPUWeight = cms.InputTag("puWeight", "PUWeight")
#)

DataMCPhotonCheckTrue = cms.EDAnalyzer("checkObject",
    srcPUWeight = cms.InputTag("puWeight", "PUWeightTrue"),
	bTagAlgorithm = cms.string("blabla"),
	srcObjects = cms.InputTag("widenedCocPatPhotons"),
	objectType =cms.string("patPhoton")
)
#DataMCPhotonCheck = DataMCPhotonCheckTrue.clone(
#    srcPUWeight=cms.InputTag("puWeight", "PUWeight")
#)

DataMCJetCheckTrue = cms.EDAnalyzer("checkObject",
    srcPUWeight = cms.InputTag("puWeight", "PUWeightTrue"),
	bTagAlgorithm = cms.string("combinedSecondaryVertexBJetTags"),
	srcObjects = cms.InputTag(jetsource),
	objectType = cms.string("patJet")
)
#DataMCJetCheck = DataMCJetCheckTrue.clone(
#    srcPUWeight = cms.InputTag("puWeight", "PUWeight")
#)

DataMCMuonCheckTrue = cms.EDAnalyzer("checkObject",
    srcPUWeight = cms.InputTag("puWeight", "PUWeightTrue"),
	bTagAlgorithm = cms.string("blabla"),
	srcObjects = cms.InputTag(muonsource),
	objectType = cms.string("patMuon")
)
#DataMCMuonCheck = DataMCMuonCheckTrue.clone(
#    srcPUWeight = cms.InputTag("puWeight", "PUWeight")
#)

dataMCSequence = cms.Sequence(
#    WeightsCheck *
#    DataMCMuonCheck *
#    DataMCJetCheck *
#    DataMCPhotonCheck *
#    DataMCCompPhotons *
#    WeightsCheckTrue *
    DataMCMuonCheckTrue *
    DataMCJetCheckTrue *
    DataMCPhotonCheckTrue *
    DataMCCompPhotonsTrue
)