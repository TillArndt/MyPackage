import FWCore.ParameterSet.Config as cms
import MyPackage.TtGammaAnalysis.myUtility as myUtility

process = cms.Process('myPhoSel')
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring( '' )
)

myUtility.addFileService(process)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

#max num of events processed
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

#################################################################################
## Everything that runs on the genParticle collection

process.genPhotonsFromME = cms.EDFilter("GenParticleSelector",
            src = cms.InputTag("genParticles"),
            cut = cms.string('\
    abs(pdgId) == 22 && numberOfMothers > 0 && abs(mother.daughter(0).pdgId) == 6\
                               '),
            filter = cms.bool(False)
            )

process.genParticleAnalyzer = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("genParticles"),
    histograms = cms.VPSet(
            cms.PSet(min          = cms.untracked.double(       -0.5),
                     max          = cms.untracked.double(        2.5),
                     nbins        = cms.untracked.int32 (          3),
                     name         = cms.untracked.string('MotherPdg6'),
                     description  = cms.untracked.string('Directly from Top;- no meaning -;count'),
                     lazyParsing  = cms.untracked.bool(True),
                     plotquantity = cms.untracked.string('\
? abs(pdgId) == 22 && abs(mother.pdgId) == 6 ? 1 : -2')
                     ),
            cms.PSet(min          = cms.untracked.double(       -0.5),
                     max          = cms.untracked.double(        2.5),
                     nbins        = cms.untracked.int32 (          3),
                     name         = cms.untracked.string('MotherDaughterPdg6'),
                     description  = cms.untracked.string('Where mother.daughter(0) is Top;- no meaning -;count'),
                     lazyParsing  = cms.untracked.bool(True),
                     plotquantity = cms.untracked.string('\
? abs(pdgId) == 22 && abs(mother.daughter(0).pdgId) == 6 ? 1 : -2')
                     )
    )
)

#################################################################################
## Selection of events with a hard photon               

# large pt ...
process.myLargePtPhotons = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("patPhotonsPFlow"),
            cut = cms.string('\
    pt > 12 \
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

# cross object clean against jets
process.cocPatPhotons = cms.EDProducer("PATPhotonCleaner",
            src = cms.InputTag("photonsWithTightID"), 
            preselection = cms.string(''),
            
            # overlap checking configurables
            checkOverlaps = cms.PSet(
                jets = cms.PSet(
                   src       = cms.InputTag("myGoodJets"),
                   algorithm = cms.string("byDeltaR"),
                   preselection        = cms.string(""),  # don't preselect the jets
                   deltaR              = cms.double(0.5), # if > 0.5: make many jets overlapping
                   checkRecoComponents = cms.bool(False), # don't check if they share some AOD object ref
                   pairCut             = cms.string(""),
                   requireNoOverlaps   = cms.bool(False),
                ),
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

process.myPhotonAnalyzer = cms.EDAnalyzer("MyPhotonAnalyzer",
                     src = cms.InputTag("photonsGenEXTRA")
                     )

#################################################################################
## Path declaration

process.p = cms.Path(#process.genPhotonsFromME *
                     #process.genParticleAnalyzer *
                     process.myLargePtPhotons *
                     process.photonsWithTightID *
                     process.cocPatPhotons *
                     process.removeCocFails *
                     process.mcTruthSequence
                     #process.myPhotonAnalyzer
                     )
