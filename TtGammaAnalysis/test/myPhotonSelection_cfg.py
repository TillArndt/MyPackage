import FWCore.ParameterSet.Config as cms

process = cms.Process('myPhoSel')

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
      'file:/user/tholen/eventFiles/ttgamma_Enriched_PatTuple.root'
      #'file:/user/tholen/eventFiles/ttgamma_whizard_firstShot_PatTuple.root'
 )
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('output/myPhotonSelection.root')
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

#max num of events processed
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

#################################################################################
## Selection of events with a hard photon               

# large pt ...
process.myLargePtPhotons = cms.EDFilter("PATPhotonSelector",
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

# cross object clean against jets
process.cocPatPhotons = cms.EDProducer("PATPhotonCleaner",
            src = cms.InputTag("myLargePtPhotons"), 
            preselection = cms.string(''),
            
            # overlap checking configurables
            checkOverlaps = cms.PSet(
                jets = cms.PSet(
                   src       = cms.InputTag("patJetsPFlow"),
                   algorithm = cms.string("byDeltaR"),
                   preselection        = cms.string(""),  # don't preselect the muons
                   deltaR              = cms.double(0.5),
                   checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
                   pairCut             = cms.string(""),
                   requireNoOverlaps   = cms.bool(False),
                ),
            ),
            finalCut = cms.string(''),
)

#dummy to remove coc fails
process.removeCocFails = cms.EDFilter("PATCandViewCountFilter",
            src = cms.InputTag("cocPatPhotons"),
            minNumber = cms.uint32(1),
            maxNumber = cms.uint32(9999)
            )

process.photonsWithTightID = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("cocPatPhotons"),
            cut = cms.string('photonID("PhotonCutBasedIDTight")'),
            filter = cms.bool(True)
            )

# info's from generated Particles 
process.photonsWithGenPart  = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("cocPatPhotons"),
            cut = cms.string('genParticlesSize > 0'),
            filter = cms.bool(True)
            )

process.photonsGenEXTRA = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonsWithGenPart"),
            cut = cms.string('abs(genParticle.mother.pdgId) == 6'),
            filter = cms.bool(True)
            )


#################################################################################
## Some analyzing

process.patPhotonAnalyzer = cms.EDAnalyzer(
    "PATPhotonHistoAnalyzer",
    src = cms.InputTag("photonsGenEXTRA"),
    histograms = cms.VPSet(
            cms.PSet(min          = cms.untracked.double(     -250.5),
                     max          = cms.untracked.double(      250.5),
                     nbins        = cms.untracked.int32 (        501),
                     name         = cms.untracked.string( 'motherId'),
                     description  = cms.untracked.string('motherId;x-axis;y-axis'),
                     plotquantity = cms.untracked.string('genParticle.mother.pdgId')
                     ),        
            cms.PSet(min          = cms.untracked.double(        0.),
                     max          = cms.untracked.double(       500),
                     nbins        = cms.untracked.int32 (       250),
                     name         = cms.untracked.string('genPart_Pt'),
                     description  = cms.untracked.string(        ''),
                     plotquantity = cms.untracked.string('genParticle.pt')
                     ),        
            cms.PSet(min          = cms.untracked.double(        0.),
                     max          = cms.untracked.double(       500),
                     nbins        = cms.untracked.int32 (       250),
                     name         = cms.untracked.string('Pt'),
                     description  = cms.untracked.string(        ''),
                     plotquantity = cms.untracked.string('pt')
                     ),
            cms.PSet(min          = cms.untracked.double(      -0.5),
                     max          = cms.untracked.double(       5.5),
                     nbins        = cms.untracked.int32 (         6),
                     name         = cms.untracked.string('overlaps.size'),
                     description  = cms.untracked.string(        ''),
                     plotquantity = cms.untracked.string('overlaps("jets").size')
                     ),
            cms.PSet(min          = cms.untracked.double(       0.5),
                     max          = cms.untracked.double(      30.5),
                     nbins        = cms.untracked.int32 (        30),
                     name         = cms.untracked.string('overlapsJetsNumConstituents'),
                     description  = cms.untracked.string(        ''),
                     lazyParsing  = cms.untracked.bool(True),
                     plotquantity = cms.untracked.string('overlaps("jets")[0].getPFConstituents.size')
                     ),
            cms.PSet(min          = cms.untracked.double(        0.),
                     max          = cms.untracked.double(         1),
                     nbins        = cms.untracked.int32 (        10),
                     name         = cms.untracked.string('dR(photon, Jet)'),
                     description  = cms.untracked.string(        ''),
                     plotquantity = cms.untracked.string('deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi)')
                     )
        )
)

process.myPhotonAnalyzer = cms.EDAnalyzer("MyPhotonAnalyzer",
                     src = cms.InputTag("photonsGenEXTRA")
                     )

#################################################################################
## Path declaration

process.p = cms.Path(process.myLargePtPhotons *
                     process.myLargePtPhotonCounter *
                     process.cocPatPhotons *
                     process.removeCocFails *
                     #process.photonsWithTightID *
                     process.photonsWithGenPart *
                     process.photonsGenEXTRA *
                     process.patPhotonAnalyzer *
                     process.myPhotonAnalyzer
                     )
