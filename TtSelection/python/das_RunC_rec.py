import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_10_1_W7F.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_13_1_BKY.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_14_1_NtW.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_15_1_zNV.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_11_1_dx6.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_12_1_fa2.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_1_1_Ama.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_2_1_CFn.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_3_1_qFW.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_4_1_XML.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_16_1_qtl.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_17_1_IJw.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_18_1_ogj.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_8_1_ILC.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_9_1_mGw.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_19_1_1s2.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_5_1_95y.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_6_1_exe.root',
       '/store/user/kuessel/SingleMu/YK_Data_MARCH13_Run2012C-EcalRecover_11Dec2012/19af216898ffab2d778b64a20c13268c/SynchSelMuJets_7_1_AIV.root' ] );


secFiles.extend( [
               ] )

