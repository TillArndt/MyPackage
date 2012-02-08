import FWCore.ParameterSet.Config as cms

genPhotonsFromME = cms.EDFilter("GenParticleSelector",
            src = cms.InputTag("genParticles"),
            cut = cms.string('\
    abs(pdgId) == 22 && numberOfMothers > 0 && abs(mother.daughter(0).pdgId) == 6\
                               '),
            filter = cms.bool(False)
            )

genParticleAnalyzer = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("genParticles"),
    histograms = cms.VPSet(
            cms.PSet(min          = cms.untracked.double(       -0.5),
                     max          = cms.untracked.double(        2.5),
                     nbins        = cms.untracked.int32 (          3),
                     name         = cms.untracked.string('MotherPdg6'),
                     description  = cms.untracked.string('Directly from Top;- no meaning -;count'),
                     lazyParsing  = cms.untracked.bool(True),
                     plotquantity = cms.untracked.string('\
? abs(pdgId) == 22 && abs(mother.pdgId) == 6 ? 1 : -2')
                     ),
            cms.PSet(min          = cms.untracked.double(       -0.5),
                     max          = cms.untracked.double(        2.5),
                     nbins        = cms.untracked.int32 (          3),
                     name         = cms.untracked.string('MotherDaughterPdg6'),
                     description  = cms.untracked.string('Where mother.daughter(0) is Top;- no meaning -;count'),
                     lazyParsing  = cms.untracked.bool(True),
                     plotquantity = cms.untracked.string('\
? abs(pdgId) == 22 && abs(mother.daughter(0).pdgId) == 6 ? 1 : -2')
                     )
    )
)

mcGenPhotonSequence = cms.Sequence(
    genPhotonsFromME
    * genParticleAnalyzer
)
