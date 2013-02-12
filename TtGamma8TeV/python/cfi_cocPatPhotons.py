

import FWCore.ParameterSet.Config as cms

#PRODUCERS
# cross object clean
cocPatPhotons = cms.EDProducer("PATPhotonCleaner",
    src = cms.InputTag("largeEtPhotons"),
    preselection = cms.string(''),

    # overlap checking configurables
    checkOverlaps = cms.PSet(
        jets = cms.PSet(
            src                 = cms.InputTag("selectedPatJetsPF"),
            algorithm           = cms.string("byDeltaR"),
            preselection        = cms.string(""),  # don't preselect the jets
            deltaR              = cms.double(0.5), # if > 0.5: make many jets overlapping
            checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
            pairCut             = cms.string(""),
            requireNoOverlaps   = cms.bool(True),
        ),
        muons = cms.PSet(
            src                 = cms.InputTag("goodPatMuonsPF"),
            algorithm           = cms.string("byDeltaR"),
            preselection        = cms.string(""),
            deltaR              = cms.double(0.5),
            checkRecoComponents = cms.bool(False),
            pairCut             = cms.string(""),
            requireNoOverlaps   = cms.bool(True),
        ),
    ),
    finalCut = cms.string(''),
)

widenedCocPatPhotons = cocPatPhotons.clone(
    src = "patPhotonsPF"
)
widenedCocPatPhotons.checkOverlaps.jets.deltaR = 50000.0
widenedCocPatPhotons.checkOverlaps.muons.deltaR = 50000.0
widenedCocPatPhotons.checkOverlaps.jets.requireNoOverlaps = False
widenedCocPatPhotons.checkOverlaps.muons.requireNoOverlaps = False