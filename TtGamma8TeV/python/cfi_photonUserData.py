

import FWCore.ParameterSet.Config as cms

photonUserData = cms.EDProducer("MyPhotonUserDataAdder",
	srcPhoton = cms.InputTag("patPhotonsPF"),
	srcJet4rho = cms.InputTag(""), ################### get kt6pf jet for rho 
	srcElectron = cms.InputTag("patElectronsPF"),
	srcConversion = cms.InputTag("vector<reco::Conversion>", "pfPhotonTranslator", "pfphot"),
	srcBeamSpot = cms.InputTag("offlineBeamSpot")
)

