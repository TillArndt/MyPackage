

import FWCore.ParameterSet.Config as cms

# Signal photons for matrix element photons (whizard)
photonsSignalME = cms.EDFilter(
    "GenParticleSelector",
    src = cms.InputTag("genParticles"),
    cut = cms.string('\
    abs(pdgId) == 22 \
    && \
    mother.numberOfDaughters == 7 \
    '),
    filter = cms.bool(False),
)

# some analyzer
photonsSignalMEanalyzer = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("photonsSignalME"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(0.),
            max          = cms.untracked.double(700.),
            nbins        = cms.untracked.int32 (70),
            name         = cms.untracked.string("histo"),
            description  = cms.untracked.string(";E_{T} / GeV;Number of photons"),
            lazyParsing  = cms.untracked.bool(True),
            plotquantity = cms.untracked.string("et"),
        )
    )
)

# Signal photons for ttbar samples
patPhotonsSignal = cms.EDProducer("TTGammaMcSignalMatch",
    patPhotons = cms.InputTag("patPhotons"),
    genSignal = cms.InputTag("ttbarPhotonMerger", "signalPhotons")
)

# A counter: require at least one photon
patPhotonsSignalCounter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("patPhotonsSignal"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    filter = cms.bool(True)
)

photonsSignalMEsequence = cms.Sequence(
    photonsSignalME
    * photonsSignalMEanalyzer
)
