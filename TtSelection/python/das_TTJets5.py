import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_68_1_pJG.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_69_1_oVQ.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_6_1_u1W.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_70_1_diJ.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_71_1_Ge9.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_72_1_bIS.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_73_1_neZ.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_74_1_1uM.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_75_1_bC6.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_76_1_jX5.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_77_1_8gZ.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_78_1_mCo.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_79_1_GEa.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_7_1_f1M.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_80_1_gwR.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_81_1_7ye.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_82_1_vfj.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_83_1_DwH.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_84_1_bN0.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_85_1_OMp.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_86_1_0Pb.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_87_1_P6Q.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_88_1_S8P.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_89_1_tMT.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_8_1_xCc.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_90_1_kIm.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_91_1_Brl.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_92_1_psM.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_93_1_E2i.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_94_1_Z6R.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_95_1_jUW.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_96_1_c4h.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_97_1_p8m.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_98_1_5no.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_9_1_G1f.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_99_1_1Xk.root' 
] );


secFiles.extend( [
               ] )

