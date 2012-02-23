__author__ = 'tholen'

import FWCore.ParameterSet.Config as cms


# record pt before cutting
analyzer_Bump = cms.EDAnalyzer(
    "PATPhotonHistoAnalyzer",
    src = cms.InputTag("photonInputDummy"),
    #weights = cms.untracked.InputTag("puWeight", "Reweight1BX"),
    histograms = cms.VPSet(
        cms.PSet(
            min          = cms.untracked.double(       -0.5),
            max          = cms.untracked.double(        9.5),
            nbins        = cms.untracked.int32 (         10),
            name         = cms.untracked.string( 'genParticleSize'),
            description  = cms.untracked.string(';number of genParticles;number of photons'),
            plotquantity = cms.untracked.string('\
            genParticlesSize \
            '),
        ),
        cms.PSet(
            min          = cms.untracked.double(          0),
            max          = cms.untracked.double(        700),
            nbins        = cms.untracked.int32 (         70),
            name         = cms.untracked.string( 'PhotonEnergyWithGenPart'),
            description  = cms.untracked.string(';E_#gamma;number of photons with genPart'),
            plotquantity = cms.untracked.string('\
            ? genParticlesSize ? energy : -1\
            '),
        ),
        cms.PSet(
            min          = cms.untracked.double(          0),
            max          = cms.untracked.double(        700),
            nbins        = cms.untracked.int32 (         70),
            name         = cms.untracked.string( 'PhotonEnergyNoGenPart'),
            description  = cms.untracked.string(';E_#gamma;number of photons without genPart'),
            plotquantity = cms.untracked.string('\
            ? genParticlesSize ? -1 : energy\
            '),
        ),
    )
)
