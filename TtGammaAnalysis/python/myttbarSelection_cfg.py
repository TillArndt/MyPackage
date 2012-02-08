import FWCore.ParameterSet.Config as cms

process = cms.Process('myttbarSel')

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    #'file:/user/scratch/tholen/ttgammaEnrichedPat.root'
    #'/store/user/kuessel/TTJets_TuneZ2_7TeV-madgraph-tauola/YKMCSummer11/mergedTTJetsSummer11_1.root'
    'file:/user/tholen/eventFiles/SynchTopGroup.root'
 #   'file:/user/tholen/eventFiles/ttgamma_whizard_firstShot.root'
 #   'file:/user/tholen/eventFiles/ttgamma_whizard_tmp.root'
 )
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('output/myttbarSelection.root')
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)
#do filtering

####################################################################################
# prepare for patMatching
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#from Configuration.PyReleaseValidation.autoCond import autoCond
process.GlobalTag.globaltag = cms.string('START42_V13::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
import PhysicsTools.PatAlgos.patSequences_cff as patSequence
process.extend(patSequence)
process.patJetCorrFactors.useRho = True

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))

# Output
process.load( "TopQuarkAnalysis.Configuration.patRefSel_outputModule_cff" )
process.out.fileName = "file:/user/tholen/eventFiles/ttgammaRefSel_selected_tmp.root"
process.out.outputCommands = ["keep *"]
process.out.SelectEvents.SelectEvents = ["p"]

# PF2PAT WorkBookJetEnergyCorrections#JetEnCorPFnoPU
process.out.SelectEvents.SelectEvents = ["p"]
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
                        "PrimaryVertexObjectFilter",
			filter = cms.bool(False),
			src = cms.InputTag("offlinePrimaryVertices"),
    			filterParams = cms.PSet(
			        maxZ = cms.double(24.0),
			        minNdof = cms.double(4.0),
		        	maxRho = cms.double(2.0)
						)
                                                  )

import PhysicsTools.PatAlgos.tools.pfTools as pfTools
postfix = "PFlow"
pfTools.usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=True, postfix=postfix)
process.pfPileUpPFlow.Enable = True
process.pfPileUpPFlow.Vertices = 'goodOfflinePrimaryVertices'
process.pfPileUpPFlow.checkClosestZVertex = cms.bool(False)
process.pfJetsPFlow.doAreaFastjet = True
process.pfJetsPFlow.doRhoFastjet = False
process.pfNoTauPFlow.enable = cms.bool(False)
process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron' + postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )

getattr(process,
        "patPF2PATSequence"+postfix).replace(getattr(process,"pfNoElectron"+postfix), 
                                             getattr(process,"pfNoElectron"+postfix)
                                             * process.kt6PFJetsPFlow )
process.patseq = cms.Sequence(    
    process.goodOfflinePrimaryVertices *
    getattr(process, "patPF2PATSequence" + postfix)
    )

####################################################################################
# my selection

# HLT_IsoMu24
import HLTrigger.HLTfilters.hltHighLevel_cfi as hlt
process.myHLTFilt = hlt.hltHighLevel.clone(TriggerResultsTag = "TriggerResults::HLT",
                                           HLTPaths = cms.vstring('HLT_IsoMu24_*'))

# Vertex
process.myVertReq = cms.EDFilter("VertexSelector", 
                                 src = cms.InputTag("goodOfflinePrimaryVertices"), 
                                 cut = cms.string("\
    !isFake && \
    ndof > 4 && \
    abs(z) < 24 && \
    position.Rho < 2.0"
                                                   ), 
                                 filter = cms.bool(True)
                                 )

# About muons
getattr(process,"pfIsolatedMuons"+postfix).combinedIsolationCut = cms.double(0.2)
getattr(process,"patMuons"+postfix).usePV = False  # see TopRefSelSynch
getattr(process,"patMuons"+postfix).embedTrack = cms.bool(True)
getattr(process,"patMuons"+postfix).pvSrc = cms.InputTag("goodOfflinePrimaryVertices")
getattr(process,"selectedPatMuons"+postfix).cut = cms.string('\
    isGlobalMuon && \
    pt > 10. && \
    abs(eta) < 2.5 && \
    ((chargedHadronIso+neutralHadronIso+photonIso) / pt) < 0.2 \
                                                       ')
process.myLooseMuonCounter=cms.EDFilter("PATCandViewCountFilter",
                                         src = cms.InputTag("selectedPatMuons" + postfix),
                                         minNumber = cms.uint32(0),
                                         maxNumber = cms.uint32(1)
                                         )

####################################################################DIFFERENT FROM REFSEL: pt > 20
# one tight muon 
process.myTightPatMuons=cms.EDFilter("PATMuonRefSelector",
                                  src = cms.InputTag("selectedPatMuons" + postfix),
                                  cut = cms.string('\
    isGlobalMuon() && \
    isTrackerMuon() && \
    pt() > 26 && \
    abs(eta) < 2.1 && \
    globalTrack().normalizedChi2() < 10 && \
    innerTrack().numberOfValidHits() > 10 && \
    globalTrack().hitPattern().numberOfValidMuonHits() > 0 && \
    abs(dB()) < 0.02 && \
    ((chargedHadronIso() + neutralHadronIso() + photonIso()) / pt()) < 0.125 && \
    innerTrack().hitPattern().pixelLayersWithMeasurement() >= 1 && \
    numberOfMatches() > 1 \
                                                  '),
                                 checkOverlaps = cms.PSet(
                                                jets = cms.PSet(
                                                    src = cms.InputTag("myGoodJets"),
                                                    deltaR = cms.double(0.3),
                                                    pairCut = cms.string(''),
                                                    checkRecoComponents = cms.bool(False),
                                                    algorithm = cms.string('byDeltaR'),
                                                    preselection = cms.string(''),
                                                    requireNoOverlaps = cms.bool(True)
                                                )
                                            ),
                                  filter = cms.bool(False)
                                  )
process.myTightMuonCounter=cms.EDFilter("PATCandViewCountFilter",
                                         src = cms.InputTag("myTightPatMuons"),
                                         minNumber = cms.uint32(1),
                                         maxNumber = cms.uint32(1)
                                         )


# electron veto
getattr(process,"selectedPatElectrons"+postfix).cut = cms.string('\
    et > 15. && \
    abs(eta) < 2.5 && \
    (chargedHadronIso+neutralHadronIso+photonIso)/et < 0.2 \
')

process.myElectronCounter=cms.EDFilter("PATCandViewCountFilter",
					src = cms.InputTag("selectedPatElectrons" + postfix),
					minNumber = cms.uint32(0),
					maxNumber = cms.uint32(0)
				      	)

# jet selection
process.myGoodJets=cms.EDFilter("PATJetSelector",
                                src = cms.InputTag("patJets" + postfix),
                                cut = cms.string('\
    pt() > 30 && \
    abs(eta()) < 2.4 && \
    numberOfDaughters() > 1 && \
    chargedEmEnergyFraction() < 0.99 && \
    neutralHadronEnergyFraction() < 0.99 && \
    neutralEmEnergyFraction() < 0.99 && \
    chargedHadronEnergyFraction() > 0 && \
    chargedMultiplicity() > 0 \
                                                   '),
                                filter = cms.bool(False)
                                )
process.myGoodJets.checkOverlaps = cms.PSet(
                                                muons = cms.PSet(
                                                    src = cms.InputTag("myTightPatMuons"),
                                                    deltaR = cms.double(0.3),
                                                    pairCut = cms.string(''),
                                                    checkRecoComponents = cms.bool(False),
                                                    algorithm = cms.string('byDeltaR'),
                                                    preselection = cms.string(''),
                                                    requireNoOverlaps = cms.bool(True)
                                                )
                                            )

# min 4 jets
process.myJetCounter=cms.EDFilter("PATCandViewCountFilter",
                                  src = cms.InputTag("myGoodJets"),
                                  minNumber = cms.uint32(4),
                                  maxNumber = cms.uint32(99999)
                                  )

"""
# write out event ids
process.myEventIDTightMuon=cms.EDAnalyzer("MyEventID",
                                          cutname = cms.string("output/myTightPatMuons.log")
                                          )
process.myEventIDLooseMuon=cms.EDAnalyzer("MyEventID",
                                          cutname = cms.string("output/myLoosePatMuons.log")
                                          )
process.myEventIDElectron=cms.EDAnalyzer("MyEventID",
                                         cutname = cms.string("output/myElectronVeto.log")
                                         )
"""

process.load("MyPackage.TtGammaAnalysis.myBTagRequirement_cfi")

process.p = cms.Path(  
                       process.myHLTFilt *
                       process.patseq *
                       ( 
                           process.myVertReq *
                           process.myGoodJets *
                           process.myTightPatMuons * 
                           process.myTightMuonCounter *
                           #process.myEventIDTightMuon *  
                           process.myLooseMuonCounter *
                           #process.myEventIDLooseMuon *
                           process.myElectronCounter *
                           #process.myEventIDElectron *
                           process.myJetCounter
                       ) 
                     )
