import FWCore.ParameterSet.Config as cms

# cross object clean
cocPatPhotons = cms.EDProducer("PATPhotonCleaner",
            src = cms.InputTag("photonsWithTightID"), 
            preselection = cms.string(''),
            
            # overlap checking configurables
            checkOverlaps = cms.PSet(
                jets = cms.PSet(
                   src                 = cms.InputTag("myGoodJets"),
                   algorithm           = cms.string("byDeltaR"),
                   preselection        = cms.string(""),  # don't preselect the jets
                   deltaR              = cms.double(0.5), # if > 0.5: make many jets overlapping
                   checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
                   pairCut             = cms.string(""),
                   requireNoOverlaps   = cms.bool(True),
                ),
                muons = cms.PSet(
                   src                 = cms.InputTag("myTightPatMuons"),
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

# dummy to remove coc fails
removeCocFails = cms.EDFilter(
            "PATCandViewCountFilter",
            src = cms.InputTag("cocPatPhotons"),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(9999)
)

cocPatPhotonSequence = cms.Sequence(
    cocPatPhotons
    * removeCocFails
)
