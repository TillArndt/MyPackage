import FWCore.ParameterSet.Config as cms

# photon coming from matrix element
photonsSignal = cms.EDFilter(
    "PATPhotonSelector",
    src = cms.InputTag("patPhotonsPFlow"),
    cut = cms.string('\
    genParticlesSize > 0\
    && \
    (\
        abs(genParticle.mother.pdgId) = 6 \
        ||\
        (\
            abs(genParticle.mother.pdgId) =  22 \
            && \
            (\
                abs(genParticle.mother.mother.daughter(0).pdgId) == 6 \
                || abs(genParticle.mother.mother.pdgId) == 6\
            )\
        )\
    )\
    '),
    filter = cms.bool(True)
)

