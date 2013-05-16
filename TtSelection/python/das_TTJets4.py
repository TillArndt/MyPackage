import FWCore.ParameterSet.Config as cms

maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
source = cms.Source ("PoolSource",fileNames = readFiles, secondaryFileNames = secFiles)
readFiles.extend( [
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_30_1_vay.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_31_1_svB.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_32_1_cvk.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_33_1_1W3.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_34_1_dGJ.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_35_1_Nzc.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_36_1_wmp.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_37_1_0C1.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_38_1_b78.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_39_1_eJI.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_3_1_Yhx.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_40_1_1Fl.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_41_1_XY0.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_42_1_dEl.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_43_1_qRo.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_44_1_0zw.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_45_1_fcK.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_46_1_LCB.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_47_1_sw0.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_48_1_NrY.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_49_1_5BQ.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_4_1_4gp.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_50_1_Rbe.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_51_1_QTO.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_52_1_nTv.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_53_1_7Sz.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_54_1_oJX.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_55_1_Eji.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_56_1_O26.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_57_1_yhP.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_58_1_Y5f.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_59_1_QJj.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_5_1_q50.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_60_1_DzK.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_61_1_Dfa.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_62_1_Av1.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_63_1_Zdv.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_64_1_e9U.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_65_1_KYj.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_66_1_43H.root',
       
'/store/user/kuessel/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/YK_MC_MARCH13_TTbar/accebdcbeca2810af478d8af2493d41f/SynchSelMuJets_67_1_Kuf.root',
] );


secFiles.extend( [
               ] )

