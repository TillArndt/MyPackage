import FWCore.ParameterSet.Config as cms

process = cms.Process("EnrichmentCenter")

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
#    'file:/user/scratch/tholen/patRefSel_muJets_50_1_oJk.root'
     '/store/user/kuessel/TTJets_TuneZ2_7TeV-madgraph-tauola/YKMCSummer11/mergedTTJetsSummer11_1.root'
  )
)

process.TFileService = cms.Service("TFileService",
  fileName = cms.string('output/makeEnrichedSample.root')
)

process.load("FWCore.MessageService.MessageLogger_cfi")
#process.MessageLogger = cms.Service("MessageLogger")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

process.myTopGenPhotons=cms.EDFilter("GenParticleRefSelector",
                                  src = cms.InputTag("genParticles"),
                                  cut = cms.string('pdgId()==22 && numberOfMothers()>0 && abs(mother(0).pdgId())==6'),
                                  filter = cms.bool(False)
                                  )

process.topGenPhotCounter = cms.EDFilter(
      "PATCandViewCountFilter"
      , src = cms.InputTag("myTopGenPhotons")
      , minNumber = cms.uint32( 1 )
      , maxNumber = cms.uint32( 999999 )
      )

process.load( "TopQuarkAnalysis.Configuration.patRefSel_outputModule_cff" )
# output file name
process.out.fileName = "/user/tholen/eventFiles/ttgamma_Enriched.root"
# clear event selection
process.out.outputCommands = ["keep *"]

process.out.SelectEvents.SelectEvents = ["p"]

process.p = cms.Path( process.myTopGenPhotons *
                      process.topGenPhotCounter  
                    )

process.outpath = cms.EndPath(process.out)





