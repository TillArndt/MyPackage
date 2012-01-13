
from UserCode.HTholen.myttbarSelection_cfg import *

 #input
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:/user/tholen/eventFiles/ttgamma_whizard_firstShot.root'
 )
)

#output
process.TFileService = cms.Service("TFileService",
  fileName = cms.string('output/MakeMyttbarTuple.root')
)

process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_whizard_firstShot_PatTuple.root"
process.out.outputCommands.append("keep *_*hoton*_*_*")
process.out.outputCommands.append("keep *_*Pat*_*_*")
process.out.outputCommands.append("keep *_*pat*_*_*")
#process.out.outputCommands.append("keep *_patPhotons*_*_*")

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(99999999))

#photonMatch resolve by best Quality
process.photonMatchPFlow.resolveByMatchQuality = cms.bool(True)

#aadd userfunction for num of mothers
process.patPhotonsPFlow.userData.userFunctions = cms.vstring('genParticle.numberOfMothers')
process.patPhotonsPFlow.userData.userFunctionLabels = cms.vstring('numMothers')

#add userfunction for pdgid of mother
process.patPhotonsPFlow.userData.userFunctions = cms.vstring('genParticle.mother.pdgId')
process.patPhotonsPFlow.userData.userFunctionLabels = cms.vstring('motherId')

#add patPhotons 
process.p.replace(process.photonMatchPFlow, process.photonMatchPFlow * process.patPhotonsPFlow)


