import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/user/kuessel/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-T/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_6_1_5v6.root',
       '/store/user/kuessel/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-T/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_5_1_5EK.root',
       '/store/user/kuessel/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-T/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_4_2_pEv.root',
       '/store/user/kuessel/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-T/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_3_1_7Tw.root',
       '/store/user/kuessel/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-T/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_2_1_2g1.root',
       '/store/user/kuessel/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tWCh-T/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_1_1_kNO.root' ] );


secFiles.extend( [
               ] )

