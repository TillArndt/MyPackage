import FWCore.ParameterSet.Config as cms
import MyPackage.TtGammaAnalysis.MyUtility as util

process = cms.Process('myPhoSel')
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring( '' )
)

util.addFileService(process)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

#max num of events processed
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

# what should have been done in patTuple:
process.load("MyPackage.TtGammaAnalysis.myBTagRequirement_cfi")

################################################################################
## Everything that runs on the genParticle collection

process.load("MyPackage.TtGammaAnalysis.mcGenPhotonSequence_cfi")

################################################################################
## Selection of events with a hard photon               

# large pt ...
process.myLargePtPhotons = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("patPhotonsPFlow"),
            cut = cms.string('\
    pt > 30 \
    && abs(eta) < 2.1 \
                              '),
            filter = cms.bool(True)
)

# require tight Photon ID
process.photonsWithTightID = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("myLargePtPhotons"),
            cut = cms.string('photonID("PhotonCutBasedIDTight")'),
            filter = cms.bool(True)
)

# cross object clean
process.cocPatPhotons = cms.EDProducer("PATPhotonCleaner",
            src = cms.InputTag("photonsWithTightID"), 
            preselection = cms.string(''),
            
            # overlap checking configurables
            checkOverlaps = cms.PSet(
                jets = cms.PSet(
                   src                 = cms.InputTag("myGoodJets"),
                   algorithm           = cms.string("byDeltaR"),
                   preselection        = cms.string(""),  # don't preselect the jets
                   deltaR              = cms.double(1.0), # if > 0.5: make many jets overlapping
                   checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
                   pairCut             = cms.string(""),
                   requireNoOverlaps   = cms.bool(False),
                ),
                muons = cms.PSet(
                   src                 = cms.InputTag("myTightPatMuons"),
                   algorithm           = cms.string("byDeltaR"),
                   preselection        = cms.string(""),  # don't preselect the jets
                   deltaR              = cms.double(1.0), # if > 0.5: make many jets overlapping
                   checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
                   pairCut             = cms.string(""),
                   requireNoOverlaps   = cms.bool(False),
            ),
            finalCut = cms.string(''),
)

# dummy to remove coc fails
process.removeCocFails = cms.EDFilter("PATCandViewCountFilter",
            src = cms.InputTag("cocPatPhotons"),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(9999)
)

# collect all Particles in cone of dR < 0.2
#process.dR20AllOverlaps = cms.EDProcducer("PATPhotonCleaner",
#            src =
                                          
#################################################################################
## Some analyzing

process.load("MyPackage.TtGammaAnalysis.mcTruthSequence_cfi")

process.analyzer_dRPhotonFromME = cms.EDAnalyzer("MyPhotonAnalyzer",
                     src = cms.InputTag("photonsFromME")
)

process.analyzer_dRPhotonFromElsewhere = process.analyzer_dRPhotonFromME.clone(
                     src = cms.InputTag("photonsFromElsewhere")
)
## Path declaration

process.p = cms.Path(process.myBTagRequirement
#                     * process.mcGenPhotonSequence
                     * process.myLargePtPhotons 
                     * process.photonsWithTightID 
                     * process.cocPatPhotons 
                     * process.removeCocFails 
                     * process.mcTruthSequence
                     * process.analyzer_dRPhotonFromME
                     * process.analyzer_dRPhotonFromElsewhere  
#                     * process.myPhotonAnalyzer
)
