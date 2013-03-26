

import FWCore.ParameterSet.Config as cms

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

photonsSignalMEsequence = cms.Sequence(
    photonsSignalME
    * photonsSignalMEanalyzer
)

# photon coming from matrix element
# photonsSignalTwo2Five = cms.EDProducer("TTGammaMcSignalMatch",
#     src = cms.InputTag("patPhotonsPF")
#     is2to5 = cms.untracked.bool(True)
# )

photonsSignalTwo2Seven = cms.EDProducer("TTGammaMcSignalMatch",
    src = cms.InputTag("widenedCocPatPhotons"),
    is2to5 = cms.untracked.bool(True)
)

photonsSignalTwo2SevenCounter = cms.EDFilter("PATCandViewCountFilter",
    src = cms.InputTag("photonsSignalTwo2Seven"),
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    filter = cms.bool(True)
)


