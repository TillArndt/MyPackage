import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/user/kuessel/T_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-T/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_1_1_BC1.root' ] );


secFiles.extend( [
               ] )

