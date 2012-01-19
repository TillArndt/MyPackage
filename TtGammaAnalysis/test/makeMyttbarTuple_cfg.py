
from MyPackage.TtGammaAnalysis.myttbarSelection_cfg import *

 #input
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    #'file:/user/tholen/eventFiles/ttgamma_whizard_firstShot.root'
    #'file:/user/tholen/eventFiles/ttgamma_Enriched.root'
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_10_1_4un.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_11_1_GOu.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_12_1_Iik.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_13_2_Ayq.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_14_2_Je5.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_1_1_k0f.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_2_1_0kk.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_3_1_Tzr.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_4_1_QXV.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_5_2_M0z.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_6_1_3kO.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_7_1_3e3.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_8_1_AEd.root', 
'file:/user/tholen/eventFiles/ttgammaEnrichedFromGrid/ttgammaEnriched_9_1_FRo.root',  
 )
)

#output
process.TFileService = cms.Service("TFileService",
  fileName = cms.string('output/MakeMyttbarTuple.root')
)

#remove cleaning (later done in photon selection)
from PhysicsTools.PatAlgos.tools.coreTools import *
removeCleaning(process)

#process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_whizard_firstShot_PatTuple.root"
process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_Enriched_PatTuple.root"
process.out.outputCommands.append("keep *_*hoton*_*_*")
process.out.outputCommands.append("keep *_*Pat*_*_*")
process.out.outputCommands.append("keep *_*pat*_*_*")
process.out.outputCommands.append("keep *_*genParticle*_*_*")
#process.out.outputCommands.append("keep *_patPhotons*_*_*")

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

#photonMatch resolve by best Quality
process.photonMatchPFlow.resolveByMatchQuality = cms.bool(True)

#add userfunction for num of mothers
#process.patPhotonsPFlow.userData.userFunctions = cms.vstring('genParticle.numberOfMothers')
#process.patPhotonsPFlow.userData.userFunctionLabels = cms.vstring('numMothers')

#add userfunction for pdgid of mother
#process.patPhotonsPFlow.userData.userFunctions = cms.vstring('genParticle.mother.pdgId')
#process.patPhotonsPFlow.userData.userFunctionLabels = cms.vstring('motherId')

#add patPhotons 
process.p.replace(process.photonMatchPFlow, process.photonMatchPFlow * process.patPhotonsPFlow)



