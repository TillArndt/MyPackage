
runOnMC = True
fastsim_workaround = False
try:
    runOnMC            = not cms_var["is_data"]
    fastsim_workaround = "two2seven" in cms_var.get("sample")
except NameError:
    print "<myttbarPatTuple_cfg>: cms_var not in __builtin__!"
print "<myttbarPatTuple_cfg>: Running On MC:", runOnMC




from MyPackage.PatTupelizer.patRefSel_muJets_cfg import *

#remove cleaning (later done in photon selection)
from PhysicsTools.PatAlgos.tools.coreTools import *
removeCleaning(process)

# output commands
process.out.outputCommands.append("keep *_*hoton*_*_*")
process.out.outputCommands.append("keep *_*Pat*_*_*")
process.out.outputCommands.append("keep *_*pat*_*_*")
process.out.outputCommands.append("keep *_*ffline*_*_*")
if runOnMC:
    process.out.outputCommands.append("keep *_*genParticle*_*_*")

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

#photonMatch resolve by best Quality
process.photonMatchPF.resolveByMatchQuality = cms.bool(True)

#add pileUpInfo
#from MyPackage.PatTupelizer.pileUpWeights_cfi import get_weights
#process.puWeight = get_weights("/net/data_cms/institut_3b/tholen/pileUpReweight/")
#process.p.replace(process.myHLTFilt, process.myHLTFilt * process.puWeight)
process.out.outputCommands.append("keep *_*ddPileupInfo*_*_*")
process.out.outputCommands.append("keep *_*eight*_*_*")

# Number of Vertices test
process.vertexHisto1BX = cms.EDAnalyzer(
    "MyVertexCountHisto",
    src = cms.InputTag("offlinePrimaryVertices"),
    weights = cms.untracked.InputTag("puWeight", "Reweight1BX")
)
process.vertexHisto3D       = process.vertexHisto1BX.clone(
    weights = cms.untracked.InputTag("puWeight", "Reweight3D")
)
process.vertexHistoGood1BX  = process.vertexHisto1BX.clone(
    src = cms.InputTag("goodOfflinePrimaryVertices"),
)
process.vertexHistoGood3D   = process.vertexHistoGood1BX.clone(
    weights = cms.untracked.InputTag("puWeight", "Reweight3D")
)

process.vtxMultSeq = cms.Sequence(
    process.vertexHisto1BX
    * process.vertexHisto3D
    * process.vertexHistoGood1BX
    * process.vertexHistoGood3D
)
#process.p += process.vtxMultSeq
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TFILESERVICEmyPatTupelizer.root')
)

#add patPhotons
process.out.outputCommands.append("keep *_patPhotons*_*_*")
if runOnMC:
    process.p.replace(process.photonMatchPF, process.photonMatchPF * process.patPhotonsPF)
else:
    process.load("PhysicsTools.PatAlgos.producersLayer1.photonProducer_cfi")
    process.patPhotonsPF = process.patPhotons.clone(
        addGenMatch = cms.bool(False)
    )
    process.p.replace(process.pfAllPhotonsPF, process.pfAllPhotonsPF * process.patPhotonsPF)

#some extra matching
process.photonMatchOthersPF = process.photonMatchPF.clone(
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


process.photonMatchAllPF = process.photonMatchOthersPF.clone(
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

process.patPhotonsOthersMatchPF = process.patPhotonsPF.clone(
    genParticleMatch = cms.InputTag("photonMatchOthersPF")
)

process.patPhotonsAllMatchPF = process.patPhotonsPF.clone(
    genParticleMatch = cms.InputTag("photonMatchAllPF")
)

if runOnMC:
    process.p.replace(
        process.patPhotonsPF, 
        process.patPhotonsPF 
        * process.photonMatchOthersPF 
        * process.photonMatchAllPF
        * process.patPhotonsOthersMatchPF 
        * process.patPhotonsAllMatchPF
    )

#process.schedule = cms.Schedule(process.p, process.vtxMultPath)
 
process.p.remove(process.patMETsPF)


# temporary workaround (NEED BETTER FASTSIM):
if fastsim_workaround:
    # original: HLT_IsoMu20_eta2p1_TriCentralPFJet30_v2
    process.step0a.triggerConditions = ["HLT_IsoMu20_eta2p1_v7"]
    # remove HCAL noise filter
    process.p.remove(process.HBHENoiseFilter)



