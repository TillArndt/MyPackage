### added by yvi

import FWCore.ParameterSet.Config as cms

DataMCCompPhotons = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag(cms_var["photonsource"]),
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
DataMCPhotonCheck=cms.EDAnalyzer("checkObject",
	bTagAlgorithm=cms.string("blabla"),
	srcObjects=cms.InputTag(cms_var["photonsource"]), 
	objectType=cms.string("patPhoton")
)
DataMCJetCheck=cms.EDAnalyzer("checkObject",
	bTagAlgorithm=cms.string("blabla"),
	srcObjects=cms.InputTag(cms_var["jetsource"]), 
	objectType=cms.string("patJet")
)
DataMCMuonCheck=cms.EDAnalyzer("checkObject",
	bTagAlgorithm=cms.string("blabla"),
	srcObjects=cms.InputTag(cms_var["muonsource"]), 
	objectType=cms.string("patMuon")
)


