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

#process.load("MyPackage.TtGammaAnalysis.mcGenPhotonSequence_cfi")

################################################################################
## Selection of events with a hard photon

process.load("MyPackage.TtGammaAnalysis.sequenceHardPhoton_cfi")

process.load("MyPackage.TtGammaAnalysis.sequenceCocPatPhoton_cfi")

# collect all Particles in cone of dR < 0.2
#process.dR20AllOverlaps = cms.EDProcducer("PATPhotonCleaner",
#            src =
                                          
#################################################################################
## Some analyzing


## Path declaration

process.selectionPath = cms.Path(
       process.myBTagRequirement
#     * process.mcGenPhotonSequence
     * process.hardPhotonSequence
     * process.cocPatPhotonSequence 
)

# other paths
process.load("MyPackage.TtGammaAnalysis.pathOverlaps_cff")


