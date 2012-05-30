import FWCore.ParameterSet.Config as cms


# record pt before cutting
analyzer_PT = cms.EDAnalyzer(
    "PATPhotonHistoAnalyzer",
    src = cms.InputTag("photonInputDummy"),
    weights = cms.untracked.InputTag("puWeight", "Reweight1BX"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(         0.),
            max          = cms.untracked.double(        500),
            nbins        = cms.untracked.int32 (         50),
            name         = cms.untracked.string( 'photonPT'),
            description  = cms.untracked.string(';photon p_{T} / GeV;number of photons'),
            plotquantity = cms.untracked.string('pt'),
        )
    )
)

# large pt ...
myLargePtPhotons = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonInputDummy"),
            cut = cms.string('\
    pt > 20 \
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
      analyzer_PT
    * myLargePtPhotons
    * photonsWithTightID
)
