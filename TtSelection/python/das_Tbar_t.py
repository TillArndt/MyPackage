import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_14_1_A0U.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_11_1_yp9.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_12_1_sDO.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_13_1_WKR.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_16_1_qsv.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_15_1_xGu.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_17_1_OHh.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_1_1_BpH.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_18_1_wmm.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_19_1_lfT.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_9_1_Woq.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_20_1_ZnY.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_8_1_xKm.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_4_1_hug.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_7_1_Wsb.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_21_1_TiK.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_6_1_I1J.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_2_1_NUC.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_5_1_3M1.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_3_1_1LN.root',
       '/store/user/kuessel/Tbar_t-channel_TuneZ2star_8TeV-powheg-tauola/YK_MC_MARCH13_SingleTop-tCh-Tbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_10_1_E0U.root' ] );


secFiles.extend( [
               ] )

