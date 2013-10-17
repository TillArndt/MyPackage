import FWCore.ParameterSet.Config as cms

process = cms.Process("PrintTriggers")

# source-file liegt in AC
process.source = cms.Source("PoolSource",
                                 fileNames = cms.untracked.vstring(
    #ttbar no trigger:
   '/store/user/geenen/PAT3X/TTBar_10TeV_Pythia_Incl_M160/geenen/TTbar_Pythia-Incl_Mtop160.MC_31X_V3-v1_GEN-SIM-RECO_AcIIIb_PAT/TTbar_Pythia-Incl_Mtop160.MC_31X_V3-v1_GEN-SIM-RECO_AcIIIb_PAT/9d7674f570118a1edfce11f22b7ecf9b/TTbar_Pythia-Incl_M160_MC_31X_V3-v1_GEN-SIM-RECO.Pat.AcIIIb_49.root' #'/store/user/geenen/PAT3X/TTBar_10TeV_Reco/geenen/TTbar/TTbar_Summer09-MC_31X_V3-v1_GEN-SIM-RECO_AcIIIb_PAT/1c5ad755866ee3e258519d854f0a71b7/TTbar_Summer09-MC_31X_V3-v1_GEN-SIM-RECO.Pat.AcIIIb_32.root'
    #DY Ele15:
    #'/store/user/geenen/PAT3X/Zee_10TeV_SD_Ele15/geenen/Zee/Zee_Summer09-MC_31X_V3_SD_Ele15-v1_GEN-SIM-RECO_Zee_10TeV_SD_Ele15_AcIIIb_PAT/1c5ad755866ee3e258519d854f0a71b7/Zee_Summer09-MC_31X_V3_SD_Ele15-v1_GEN-SIM-RECO_Zee_10TeV_SD_Ele15.Pat.AcIIIb_14.root',
    #DY Mu9:
    #'/store/user/geenen/PAT3X/Zmumu_10TeV_SD_Mu9/geenen/Zmumu/Zmumu_Summer09-MC_31X_V3_SD_Mu9-v1_GEN-SIM-RECO_Zmumu_10TeV_SD_Mu9_AcIIIb_PAT/1c5ad755866ee3e258519d854f0a71b7/Zmumu_Summer09-MC_31X_V3_SD_Mu9-v1_GEN-SIM-RECO_Zmumu_10TeV_SD_Mu9.Pat.AcIIIb_1.root'
                                 )
                            )

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.printIt = cms.EDAnalyzer('PrintTriggersReco',
    triggerResults    = cms.InputTag("TriggerResults","","HLT")
)

process.p = cms.Path(process.printIt)
