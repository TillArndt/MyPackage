import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_9_1_5sM.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_8_1_nFZ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_7_1_zyQ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_6_1_fVW.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_5_1_YyY.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_56_1_wTn.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_55_1_ZcJ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_54_1_oAX.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_53_2_Fip.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_52_2_BiO.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_51_1_Tc2.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_50_2_Leo.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_4_1_UHH.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_49_1_Vcq.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_48_2_5fH.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_47_1_1Nr.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_46_1_jlh.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_45_1_vKQ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_44_1_3dM.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_43_1_pVZ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_42_1_3fj.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_41_1_0na.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_40_1_MGJ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_3_1_9wi.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_39_1_ilo.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_38_1_3d1.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_37_1_fXM.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_36_1_bUl.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_35_2_aRA.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_34_2_6Oa.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_33_1_R5M.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_32_2_ykZ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_31_1_kuw.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_30_1_AJ1.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_2_1_wWD.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_29_1_y2n.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_28_1_LAL.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_27_1_QvC.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_26_1_6SF.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_25_2_HOd.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_24_2_0wc.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_23_1_9Q9.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_22_1_fLT.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_21_2_7Kc.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_20_2_4HE.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_1_1_DdQ.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_19_1_BPo.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_18_1_URP.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_17_1_Y0r.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_16_1_V8L.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_15_1_T14.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_14_1_N2W.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_13_1_Y13.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_12_1_dMb.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_11_1_vum.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-24Aug/3e77678f9957d8c04841a5ada06d2b48/SynchSelMuJets_10_1_xqM.root' ] );


secFiles.extend( [
               ] )

