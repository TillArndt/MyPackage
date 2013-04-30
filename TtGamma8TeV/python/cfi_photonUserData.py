

import FWCore.ParameterSet.Config as cms

photonUserData = cms.EDProducer("MyPhotonUserDataAdder",
	srcPhoton = cms.InputTag(cms_var["photonsource"]),
	srcJet4rho = cms.InputTag(""), ################### get kt6pf jet for rho 
	srcElectron = cms.InputTag("patElectronsTR"),
	srcConversion = cms.InputTag("vector<reco::Conversion>", "pfPhotonTranslator", "pfphot"),
	srcBeamSpot = cms.InputTag("offlineBeamSpot"),
        srcVertices = cms.InputTag("offlinePrimaryVertices"),
        srcPFColl = cms.InputTag("particleFlow")
)

