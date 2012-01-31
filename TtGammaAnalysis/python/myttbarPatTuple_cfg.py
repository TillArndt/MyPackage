
from MyPackage.TtGammaAnalysis.myttbarSelection_cfg import *

import MyPackage.TtGammaAnalysis.myUtility as myUtil
myUtil.addFileService(process)

#remove cleaning (later done in photon selection)
from PhysicsTools.PatAlgos.tools.coreTools import *
removeCleaning(process)

# output commands
process.out.outputCommands.append("keep *_*hoton*_*_*")
process.out.outputCommands.append("keep *_*Pat*_*_*")
process.out.outputCommands.append("keep *_*pat*_*_*")
process.out.outputCommands.append("keep *_myGoodJets_*_*")
process.out.outputCommands.append("drop *_*_*_PAT")
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

#require one b-tag
