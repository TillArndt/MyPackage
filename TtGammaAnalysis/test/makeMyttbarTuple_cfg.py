
from MyPackage.TtGammaAnalysis.myttbarPatTuple_cfg import *

#input
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:/user/tholen/eventFiles/ttgamma_whizard_43.root'
    #'file:/user/tholen/eventFiles/ttgamma_whizard.root'
    #'file:/user/tholen/eventFiles/ttgamma_whizard_noISR.root'
    #'file:/user/tholen/eventFiles/ttgamma_whizard_noISR_noFSR.root'
    #'file:/user/tholen/eventFiles/ttgamma_Enriched.root'
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_10_1_4un.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_11_1_GOu.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_12_1_Iik.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_13_2_Ayq.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_14_2_Je5.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_1_1_k0f.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_2_1_0kk.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_3_1_Tzr.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_4_1_QXV.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_5_2_M0z.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_6_1_3kO.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_7_1_3e3.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_8_1_AEd.root', 
    #'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_9_1_FRo.root',  
 )
)

#process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_Enriched_PatTuple.root"
process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_whizard_43_PatTuple.root"
#process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_whizard_noISR_noFSR_PatTuple.root"
#process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_whizard_noISR_PatTuple.root"



