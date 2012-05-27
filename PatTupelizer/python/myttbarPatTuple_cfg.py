
try:
    runOnMC = not crc_var["runOnData"]
except NameError:
    print "<myttbarPatTuple_cfg>: crc_var not in __builtin__!"
    runOnMC = True
except KeyError:
    print "<myttbarPatTuple_cfg>: crc_var declared, but no key 'runOnData'"
    runOnMC = True
print "<myttbarPatTuple_cfg>: Running On MC:", runOnMC




from MyPackage.TtGammaAnalysis.myttbarSelection_cfg import *

#remove cleaning (later done in photon selection)
from PhysicsTools.PatAlgos.tools.coreTools import *
removeCleaning(process)

# output commands
process.out.outputCommands.append("keep *_*hoton*_*_*")
process.out.outputCommands.append("keep *_*Pat*_*_*")
process.out.outputCommands.append("keep *_*pat*_*_*")
process.out.outputCommands.append("keep *_myGoodJets_*_*")
process.out.outputCommands.append("drop *_*_*_PAT")
if runOnMC:
    process.out.outputCommands.append("keep *_*genParticle*_*_*")

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

#photonMatch resolve by best Quality
process.photonMatchPFlow.resolveByMatchQuality = cms.bool(True)

#add pileUpInfo
import YKuessel.TopCharge.weights_cfi as weights
weights.puWeight.weights = '/user/tholen/eventFiles/pileUpReweight/TopCharge/Weight3D_2.root'
weights.puWeight.PUInputFileMC = '/user/tholen/eventFiles/pileUpReweight/MC_ReweightInput.root'
weights.puWeight.PUInputFileData = '/user/tholen/eventFiles/pileUpReweight/pileupFiles4_6fb/Merged2_PileupTruth_FineBin_4_6_fb.root'
weights.puWeight.PUInputFileDataBX1 = '/user/tholen/eventFiles/pileUpReweight/pileupFiles_1BXOption/Merged_Pileup_4_6_fb.root'
process.extend(weights)
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
process.load("MyPackage.TtGammaAnalysis.myBTagRequirement_cfi")
process.p.replace(process.myJetCounter, process.myJetCounter * process.myBTagRequirement)
