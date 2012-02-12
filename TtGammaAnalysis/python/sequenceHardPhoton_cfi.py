import FWCore.ParameterSet.Config as cms

# input dummy
photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("patPhotonsPFlow"),
    cut = cms.string(""),
    filter = cms.bool(False)
)

# record pt before cutting
analyzer_PT = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("photonInputDummy"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(         0.),
            max          = cms.untracked.double(        500),
            nbins        = cms.untracked.int32 (         50),
            name         = cms.untracked.string( 'photonPT'),
            description  = cms.untracked.string('photonPT;photon p_{T};number of photons'),
            plotquantity = cms.untracked.string('pt'),
        )
    )
)

# large pt ...
myLargePtPhotons = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonInputDummy"),
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
      photonInputDummy
    * analyzer_PT
    * myLargePtPhotons
    * photonsWithTightID
)
