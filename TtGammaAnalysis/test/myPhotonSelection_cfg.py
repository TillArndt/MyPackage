import FWCore.ParameterSet.Config as cms

process = cms.Process('myPhoSel')

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
      'file:/user/tholen/eventFiles/ttgamma_whizard_firstShot_PatTuple.root'
 )
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('output/myttbarSelection.root')
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

#################################################################################
## Selection of events with a hard photon               

process.myLargePtPhotons = cms.EDFilter("PATPhotonRefSelector",
                                        src = cms.InputTag("patPhotonsPFlow"),
                                        cut = cms.string('\
    pt > 15 \
    && abs(eta) < 2.1 \
                                                          '),
                                        filter = cms.bool(False)
                                        )
process.myLargePtPhotonCounter = cms.EDFilter("PATCandViewCountFilter",
                                              src = cms.InputTag("myLargePtPhotons"),
                                              minNumber = cms.uint32(1),
                                              maxNumber = cms.uint32(9999)
                                              )

process.myPhotonAnalyser = cms.EDAnalyzer(
    "PATPhotonHistoAnalyzer",
    src = cms.InputTag("myLargePtPhotons"),
    histograms = cms.VPSet(
            cms.PSet(min          = cms.untracked.double(     -50.5),
                     max          = cms.untracked.double(      50.5),
                     nbins        = cms.untracked.int32 (       101),
                     name         = cms.untracked.string('motherId'),
                     description  = cms.untracked.string(        ''),
                     plotquantity = cms.untracked.string('genParticle.mother.pdgId')
                     )        
        )
)



#################################################################################
## Path declaration

process.p = cms.Path(process.myLargePtPhotons *
                     process.myLargePtPhotonCounter *
                     process.myPhotonAnalyser
                     )
