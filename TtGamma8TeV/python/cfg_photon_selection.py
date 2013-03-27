
# fetch variables from CmsRunController
runOnMC     = True
legend      = NameError
useMerging  = ""
preSelOpt   = None
puWeight    = None
sample      = ""
try:
    runOnMC     = not cms_var["isData"]
    legend      = cms_var["legend"]
    useMerging  = cms_var.get("useMerging", useMerging)
    preSelOpt   = cms_var.get("preSelOpt",preSelOpt)
    puReweight  = cms_var.get("puWeight", puWeight)
    sample      = cms_var.get("sample", sample)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"
print "<"+__name__+">: Running On MC:", runOnMC
print "<"+__name__+">: Samplename is:", legend


# Regular Config starting here
import FWCore.ParameterSet.Config as cms

if puWeight:
    puWeight = cms.untracked.InputTag("puWeight", puWeight)

process = cms.Process('PhotonSelection')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( '' ),
)
# disable duplicateCheckMode on two2seven
if "two2seven" in sample:
    process.source.duplicateCheckMode = cms.untracked.string("noDuplicateCheck")


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TFILESERVICEmyPhotonSelection.root')
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

# input and presel
process.load("MyPackage.TtGamma8TeV.cfi_cocPatPhotons")
process.load("MyPackage.TtGamma8TeV.cfi_bTagRequirement")
process.load("MyPackage.TtGamma8TeV.cfi_mcTruth")
process.load("MyPackage.TtGamma8TeV.cfi_ttgammaMerging")
#process.load("MyPackage.TtGamma8TeV.cfi_photonUserData")
#process.load("MyPackage.TtGamma8TeV.sequenceTtgammaMerging_cff")
process.photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("widenedCocPatPhotons"),
    cut = cms.string(""),
    filter = cms.bool(False)
)
process.preSel = cms.Sequence(process.bTagRequirement * process.photonInputDummy)
if preSelOpt == "go4Signal":
    process.preSel.replace(
        process.bTagRequirement, 
        process.bTagRequirement 
        * process.ttgammaMerging
        * process.photonsSignalTwo2Seven
        * process.photonsSignalTwo2SevenCounter
    )
if preSelOpt == "go4Noise":
    process.preSel.replace(
        process.bTagRequirement, 
        process.bTagRequirement 
        * process.ttgammaMerging
        * process.photonsSignalTwo2Seven
        * ~process.photonsSignalTwo2SevenCounter
    )
if preSelOpt == "go4Whiz":
    process.preSel.replace(
        process.bTagRequirement,
        process.bTagRequirement
        * process.photonsSignalMEsequence
    )

# Number of Vertices
#process.vertexHisto = cms.EDAnalyzer(
#    "MyVertexCountHisto",
#    src = cms.InputTag("offlinePrimaryVertices"),
#)
#process.vertexHistoGood = process.vertexHisto.clone(
#    src = cms.InputTag("goodOfflinePrimaryVertices"),
#)
#process.vertexHisto1BX = cms.EDAnalyzer(
#    "MyVertexCountHisto",
#    src = cms.InputTag("offlinePrimaryVertices"),
#    weights = cms.untracked.InputTag("puWeight", "Reweight1BX")
#)
#process.vertexHisto3D = process.vertexHisto1BX.clone(
#    weights = cms.untracked.InputTag("puWeight", "Reweight3D")
#)
#process.vertexHistoGood1BX  = process.vertexHisto1BX.clone(
#    src = cms.InputTag("goodOfflinePrimaryVertices"),
#)
#process.vertexHistoGood3D   = process.vertexHistoGood1BX.clone(
#    weights = cms.untracked.InputTag("puWeight", "Reweight3D")
#)

# Path declarations
process.producerPath = cms.Path(
#    process.photonUserData *
    process.widenedCocPatPhotons *
    process.preSel
)

process.selectionPath = cms.Path(
    process.preSel
)

#process.overlapsPath = cms.Path(
#    process.preSel
#    * process.analyzer_Photon
#    * process.analyzer_ET
#)

# schedule
process.schedule = cms.Schedule(
    process.producerPath,
    process.selectionPath,
    #    process.overlapsPath
)

#process.vtxMultPath = cms.Path(
#    process.preSel
#    * process.vertexHisto
#    * process.vertexHistoGood
#    * process.vertexHisto1BX
#    * process.vertexHisto3D
#    * process.vertexHistoGood1BX
#    * process.vertexHistoGood3D
#)
#if puWeight:
#    process.schedule.append(process.vtxMultPath)


####################################################################### ID CUTS
from MyPackage.TtGamma8TeV.cff_photonIDCuts import add_photon_cuts
nMinusOnePaths = add_photon_cuts(process)
for path in nMinusOnePaths:
    process.schedule.append(path)


####################################################################### Cutflow

#process.analyzeSelection=cms.EDAnalyzer(
#    "CheckSelection",
#    processName=cms.string("myPhoSel"),
#    pathNames=cms.vstring("selectionPath")
#)
#if puWeight:
#    process.analyzeSelection.weights = puWeight
#
#from MyPackage.TtGamma8TeV.selectionTool import runSelectionTool
#names=cms.vstring()
#runSelectionTool(process, "selectionPath", names=names)
##put them in correct order not automated yet
#selPathMods = str(process.selectionPath).split("+")
#names=cms.vstring()
#while selPathMods[0] != "photonInputDummy":
#    selPathMods.pop(0)
#for mod in selPathMods:
#    names.append("ModulePath" + mod)
#process.analyzeSelection.pathNames=names
#process.analyzeSelection.processName=cms.string(process.process)
#process.selAnalyze = cms.EndPath(process.analyzeSelection)
#
#for name in names:
#    process.schedule.append(getattr(process,name))
#process.schedule.append(process.selAnalyze)



# TEMPLATE FIT TEMPLATE CREATION
#if runOnMC:
#    process.load("MyPackage.TtGamma8TeV.TemplateCreator")
#    process.templatePath.insert(0, process.preSel)
#    process.schedule.append(process.templatePath)
#else:
#    process.load("MyPackage.TtGamma8TeV.TemplateCreator")
#    process.templatePathData.insert(0, process.preSel)
#    process.schedule.append(process.templatePathData)



