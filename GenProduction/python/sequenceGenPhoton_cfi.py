import FWCore.ParameterSet.Config as cms

photonsME = cms.EDFilter(
    "GenParticleSelector",
    src=cms.InputTag("genParticles"),
    filter=cms.bool(False),
    cut=cms.string('\
    pdgId = 22 \
    && numberOfMothers \
    && abs(mother.daughter(0).pdgId) == 6 \
    '),
)

photonsTopShower = photonsME.clone(
    cut=cms.string('\
    pdgId = 22 \
    && numberOfMothers \
    && abs(mother.pdgId) == 6 \
    ')
)

photonsBottomShower = photonsME.clone(
    cut=cms.string('\
    pdgId = 22 \
    && numberOfMothers \
    && abs(mother.pdgId) == 5 \
    ')
)

photonsWBosonShower = photonsME.clone(
    cut=cms.string('\
    pdgId = 22 \
    && numberOfMothers \
    && abs(mother.pdgId) == 24 \
    ')
)

photonsOther = photonsME.clone(
    cut=cms.string('\
    pdgId = 22 \
    && ((numberOfMothers \
    && abs(mother.daughter(0).pdgId) != 6 \
    && abs(mother.daughter(0).pdgId) != 5 \
    && abs(mother.daughter(0).pdgId) != 24 \
    ) || !numberOfMothers ) \
    ')
)

genPhotonSequence = cms.Sequence(
      photonsME
    * photonsTopShower
    * photonsBottomShower
    * photonsWBosonShower
    * photonsOther
)

