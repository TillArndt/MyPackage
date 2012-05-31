
runOnMC = True
try:
    runOnMC = not crc_var["isData"]
except NameError:
    print "<myttbarPatTuple_cfg>: crc_var not in __builtin__!"
print "<myttbarPatTuple_cfg>: Running On MC:", runOnMC




from MyPackage.PatTupelizer.myttbarSelection_cfg import *

#remove cleaning (later done in photon selection)
from PhysicsTools.PatAlgos.tools.coreTools import *
removeCleaning(process)

# output commands
process.out.outputCommands.append("keep *_*hoton*_*_*")
process.out.outputCommands.append("keep *_*Pat*_*_*")
process.out.outputCommands.append("keep *_*pat*_*_*")
process.out.outputCommands.append("keep *_myGoodJets_*_*")
process.out.outputCommands.append("drop *_*_*_PAT")
process.out.outputCommands.append("keep *_*ffline*_*_*")
if runOnMC:
    process.out.outputCommands.append("keep *_*genParticle*_*_*")

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

#photonMatch resolve by best Quality
process.photonMatchPFlow.resolveByMatchQuality = cms.bool(True)

#add pileUpInfo
from MyPackage.PatTupelizer.pileUpWeights_cfi import get_weights
process.puWeight = get_weights("/net/data_cms/institut_3b/tholen/pileUpReweight/")
process.p.replace(process.myHLTFilt, process.myHLTFilt * process.puWeight)
process.out.outputCommands.append("keep *_addPileupInfo*_*_*")
process.out.outputCommands.append("keep *_puWeight_*_*")

#add patPhotons
process.out.outputCommands.append("keep *_patPhotons*_*_*")
if runOnMC:
    process.p.replace(process.photonMatchPFlow, process.photonMatchPFlow * process.patPhotonsPFlow)
else:
    process.load("PhysicsTools.PatAlgos.producersLayer1.photonProducer_cfi")
    process.patPhotonsPFlow = process.patPhotons.clone(
        addGenMatch = cms.bool(False)
    )
    process.p.replace(process.pfAllPhotonsPFlow, process.pfAllPhotonsPFlow * process.patPhotonsPFlow)

#require one b-tag
process.load("MyPackage.PatTupelizer.myBTagRequirement_cfi")
process.p.replace(process.myJetCounter, process.myJetCounter * process.myBTagRequirement)
