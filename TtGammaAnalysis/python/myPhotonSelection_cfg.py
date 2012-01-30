import FWCore.ParameterSet.Config as cms

process = cms.Process('myPhoSel')

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    #'file:/user/tholen/eventFiles/ttgamma_whizard_2nd_noISR_PatTuple.root'
    'file:/user/tholen/eventFiles/ttgamma_whizard_2nd_noISR_noFSR_PatTuple.root'
    #'file:/user/tholen/eventFiles/ttgamma_Enriched_PatTuple.root'
    #'file:/user/tholen/eventFiles/ttgamma_whizard_firstShot_PatTuple.root'
 )
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('output/myPhotonSelection_2nd_noISR.root')
)

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
                   preselection        = cms.string(""),  # don't preselect the muons
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

# info's from generated Particles 
process.photonsWithGenPart  = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("cocPatPhotons"),
            cut = cms.string('genParticlesSize > 0'),
            filter = cms.bool(False)
            )

process.patPhotonsFromME = cms.EDFilter("PATPhotonSelector",
            src = cms.InputTag("photonsWithGenPart"),
            cut = cms.string('\
    abs(genParticle.mother.pdgId) = 22 \
    && abs(genParticle.mother.mother.daughter(0).pdgId) == 6 \
                               '),
            filter = cms.bool(True)
            )

#################################################################################
## Some analyzing (PATPhotons)

process.patPhotonAnalyzerAll = cms.EDAnalyzer(
    "PATPhotonHistoAnalyzer",
    src = cms.InputTag("photonsWithGenPart"),
    histograms = cms.VPSet(
            cms.PSet(min          = cms.untracked.double(     -250.5),
                     max          = cms.untracked.double(      250.5),
                     nbins        = cms.untracked.int32 (        501),
                     name         = cms.untracked.string( 'motherId'),
                     description  = cms.untracked.string('mother: pdgId;pdgId;count'),
                     plotquantity = cms.untracked.string('genParticle.mother.pdgId')
                     ),        
            cms.PSet(min          = cms.untracked.double(        0.),
                     max          = cms.untracked.double(       500),
                     nbins        = cms.untracked.int32 (       100),
                     name         = cms.untracked.string('pt'),
                     description  = cms.untracked.string('p_{T};p_{T} / GeV;count'),
                     plotquantity = cms.untracked.string('pt')
                     ),
            cms.PSet(min          = cms.untracked.double(      -0.5),
                     max          = cms.untracked.double(      10.5),
                     nbins        = cms.untracked.int32 (        11),
                     name         = cms.untracked.string('NumOverlaps'),
                     description  = cms.untracked.string('Number of overlap jets in #DeltaR = 0.5;no.;count'),
                     plotquantity = cms.untracked.string('overlaps("jets").size')
                     ),
            cms.PSet(min          = cms.untracked.double(      -1.5),
                     max          = cms.untracked.double(      30.5),
                     nbins        = cms.untracked.int32 (        32),
                     name         = cms.untracked.string('overlapsJetsNumConstituents'),
                     description  = cms.untracked.string('Number of overlap jet constituents;no.;count'),
                     lazyParsing  = cms.untracked.bool(True),
                     plotquantity = cms.untracked.string('\
? overlaps("jets").size > 0 ? overlaps("jets")[0].getPFConstituents.size : -1 \
                                                           ')
                     ),
            cms.PSet(min          = cms.untracked.double(        0.),
                     max          = cms.untracked.double(       0.7),
                     nbins        = cms.untracked.int32 (        14),
                     name         = cms.untracked.string('dR(photon, Jet)'),
                     description  = cms.untracked.string('dR(photon, Jet);dR(photon, Jet);count'),
                     plotquantity = cms.untracked.string('\
? overlaps("jets").size > 0 ?\
 deltaR(eta, phi, overlaps("jets")[0].eta, overlaps("jets")[0].phi) : -1 \
                                                           ')
                     ),
            cms.PSet(min          = cms.untracked.double(     -50.5),
                     max          = cms.untracked.double(      50.5),
                     nbins        = cms.untracked.int32 (       101),
                     name         = cms.untracked.string('pdgIdFor1ParticleJets'),
                     description  = cms.untracked.string('pdgId of 1 part. jet constituent;pdgId;count'),
                     lazyParsing  = cms.untracked.bool(True),
                     plotquantity = cms.untracked.string('\
? overlaps("jets").size == 1 && overlaps("jets")[0].getPFConstituents.size == 1 ?\
 overlaps("jets")[0].getPFConstituents[0].pdgId  : -300 \
                                                           ')
                     )
        )
)

process.patPhotonsFromMEAnalyzer = process.patPhotonAnalyzerAll.clone(
        src = cms.InputTag("patPhotonsFromME")
)

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
                     process.photonsWithGenPart *
                     process.patPhotonsFromME *
                     process.patPhotonsFromMEAnalyzer * 
                     process.patPhotonAnalyzerAll 
                     #process.myPhotonAnalyzer
                     )
