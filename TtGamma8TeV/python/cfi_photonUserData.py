
photonsource = "patPhotons"
try:
    photonsource = cms_var.get("photonsource", photonsource)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms

photonUserData = cms.EDProducer("MyPhotonUserDataAdder",
	srcPhoton = cms.InputTag(photonsource),
	srcJet4rho = cms.InputTag(""), ################### get kt6pf jet for rho 
	srcElectron = cms.InputTag("patElectronsTR"),
	srcConversion = cms.InputTag("vector<reco::Conversion>", "pfPhotonTranslator", "pfphot"),
	srcBeamSpot = cms.InputTag("offlineBeamSpot"),
        srcVertices = cms.InputTag("offlinePrimaryVertices"),
        srcPFColl = cms.InputTag("particleFlow")
)

