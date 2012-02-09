import FWCore.ParameterSet.Config as cms

# large pt ...
myLargePtPhotons = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("patPhotonsPFlow"),
            cut = cms.string('\
    pt > 30 \
    && abs(eta) < 2.1 \
                              '),
            filter = cms.bool(True)
)

# require tight Photon ID
photonsWithTightID = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("myLargePtPhotons"),
            cut = cms.string('photonID("PhotonCutBasedIDTight")'),
            filter = cms.bool(True)
)

hardPhotonSequence = cms.Sequence(
    myLargePtPhotons
    * photonsWithTightID
)
