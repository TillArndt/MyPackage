import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_52_1_Uxi.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_53_1_iZx.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_54_1_NmL.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_5_1_zgS.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_6_1_aO1.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_7_1_Q8U.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_8_1_qhq.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_9_1_IWM.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_10_1_ZKQ.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_11_1_m18.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_12_1_I1J.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_13_1_siF.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_14_1_mFF.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_15_1_Lmi.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_16_1_aEE.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_18_1_J09.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_19_1_Gcs.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_1_1_lO0.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_21_1_Ghy.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_22_1_TFM.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_23_1_5Yp.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_24_1_n85.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_25_1_WBk.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_26_1_ywi.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_27_1_ahg.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_29_1_sa6.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_2_1_thI.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_30_1_gEV.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_31_1_0DX.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_33_1_TmR.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_17_1_HGm.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_20_1_lIu.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_36_1_zjq.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_37_1_tOZ.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_38_1_QN3.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_39_1_q5N.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_3_1_CoL.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_40_1_ovg.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_41_1_tkF.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_42_1_deW.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_43_1_lAO.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_44_1_yg3.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_28_1_hba.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_46_1_W3i.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_47_1_KQe.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_32_1_h2n.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_48_1_2wC.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_34_1_5bm.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_49_1_XKW.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_35_1_RTS.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_4_1_g8a.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_50_1_fAu.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_45_1_UqU.root',
       '/store/user/kuessel/MuHad/YK_Data_MARCH13_Run2012A-recover-06Aug2012/f6ab651872844fcfc8a3d70d6328c513/SynchSelMuJets_51_1_kC4.root' ] );


secFiles.extend( [
               ] )

