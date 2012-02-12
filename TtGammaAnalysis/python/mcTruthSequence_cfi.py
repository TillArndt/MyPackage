import FWCore.ParameterSet.Config as cms

# unified input to sequence
mcTruthInputModule = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("cocPatPhotons"),
            cut = cms.string(""),
            filter = cms.bool(False)
)

# photons with a gen particle assigned (before detector sim)
photonsWithGenPart  = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("mcTruthInputModule"),
            cut = cms.string('genParticlesSize > 0'),
            filter = cms.bool(False)
)

# photon coming from matrix element
photonsFromME = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonsWithGenPart"),
            cut = cms.string('\
    abs(genParticle.mother.pdgId) = 22 \
    && abs(genParticle.mother.mother.daughter(0).pdgId) == 6 \
                               '),
            filter = cms.bool(False)
)

# photon NOT from matrix element
photonsFromElsewhere = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("mcTruthInputModule"),
            cut = cms.string('\
    genParticlesSize == 0 \
    || abs(genParticle.mother.pdgId) != 22 \
    || abs(genParticle.mother.mother.daughter(0).pdgId) != 6 \
                               '),
            filter = cms.bool(False)
)


analyzer_dRPhotonFromME = cms.EDAnalyzer("MyPhotonAnalyzer",
                     src = cms.InputTag("photonsFromME")
)

analyzer_dRPhotonFromElsewhere = cms.EDAnalyzer("MyPhotonAnalyzer",
                     src = cms.InputTag("photonsFromElsewhere")
)


mcTruthSequence = cms.Sequence(
      mcTruthInputModule
    * photonsWithGenPart
    * photonsFromME 
    * photonsFromElsewhere
    * analyzer_dRPhotonFromME
    * analyzer_dRPhotonFromElsewhere
) 
