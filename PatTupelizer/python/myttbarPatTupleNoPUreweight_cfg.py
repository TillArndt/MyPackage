
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
process.out.outputCommands.append("keep *_*ddPileupInfo*_*_*")
process.out.outputCommands.append("keep *_*ertex*_*_*")
process.out.outputCommands.append("keep *_*eight*_*_*")


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

#some extra matching
process.photonMatchOthersPFlow = process.photonMatchPFlow.clone(
    mcPdgId     = cms.vint32(13, 21, 11, 1,2,3,4,5,6,
                            221,                        # eta 
                            211,                        # pion 
                             15,                        # tau       
                            311,                        # K 0
                            421,                        # D 0      
                            411,                        # D         
                            113,                        # rho 
                            223,                        # omega
                            333,                        # phi       
                            423,                        # D*(2007)  
                            111),                       # pion 0
    mcStatus    = cms.vint32(1),
    checkCharge = cms.bool(False),
    resolveAmbiguities = cms.bool(True), 
    resolveByMatchQuality = cms.bool(True),
    maxDeltaR = cms.double(0.2), 
    maxDPtRel = cms.double(1)
)


process.photonMatchAllPFlow = process.photonMatchOthersPFlow.clone(
    mcPdgId     = cms.vint32(22,
                            13, 21, 11, 1,2,3,4,5,6,
                            221,                        # eta 
                            211,                        # pion 
                             15,                        # tau       
                            311,                        # K 0
                            421,                        # D 0      
                            411,                        # D         
                            113,                        # rho 
                            223,                        # omega
                            333,                        # phi       
                            423,                        # D*(2007)  
                            111),                       # pion 0
)

process.patPhotonsOthersMatchPFlow = process.patPhotonsPFlow.clone(
    genParticleMatch = cms.InputTag("photonMatchOthersPFlow")
)

process.patPhotonsAllMatchPFlow = process.patPhotonsPFlow.clone(
    genParticleMatch = cms.InputTag("photonMatchAllPFlow")
)

if runOnMC:
    process.p.replace(
        process.patPhotonsPFlow, 
        process.patPhotonsPFlow 
        * process.photonMatchOthersPFlow 
        * process.photonMatchAllPFlow
        * process.patPhotonsOthersMatchPFlow 
        * process.patPhotonsAllMatchPFlow
    )

#process.schedule = cms.Schedule(process.p, process.vtxMultPath)
