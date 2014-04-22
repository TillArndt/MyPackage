
import FWCore.ParameterSet.Config as cms

photonUserData = cms.EDProducer("MyPhotonUserDataAdder",
    srcPhoton = cms.InputTag("patPhotons"),
    srcKt6pfRho = cms.InputTag("kt6PFJets", "rho"),
    srcElectron = cms.InputTag("gsfElectrons"),
    srcConversion = cms.InputTag("vector<reco::Conversion>", "pfPhotonTranslator", "pfphot"),
    srcBeamSpot = cms.InputTag("offlineBeamSpot"),
    srcVertices = cms.InputTag("offlinePrimaryVertices"),
    srcPFColl = cms.InputTag("particleFlow")
)

photonUserDataLargestPdgId = cms.EDProducer("MyPhotonUserDataLargestPdgId",
    srcPhoton = cms.InputTag("photonUserData"),
)

photonUserDataSCFootRm = cms.EDProducer("MyPhotonUserDataSCFootRm",
    srcPhoton = cms.InputTag("photonUserData"),
)


photonUserDataSequence = cms.Sequence(
    photonUserData *
    photonUserDataSCFootRm *
    photonUserDataLargestPdgId
)
