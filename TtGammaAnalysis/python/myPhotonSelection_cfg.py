
# fetch variables from CmsRunController
runOnMC     = True
legend      = NameError
useMerging  = False
go4Signal   = False
go4Noise    = False
on2to3whiz  = False
puReweight  = ""
try:
    runOnMC     = not crc_var["isData"]
    legend      = crc_var["legend"]
    useMerging  = crc_var.get("useMerging", useMerging)
    go4Signal   = crc_var.get("go4Signal",go4Signal)
    go4Noise    = crc_var.get("go4Noise",go4Noise)
    puReweight  = crc_var.get("puReweight", puReweight)
    sample      = crc_var.get("sample")
    if sample == "ttgamma_whizard" or sample == "ttgamma_whizard_43":
        on2to3whiz = True
except NameError:
    print "<"+__name__+">: crc_var not in __builtin__!"
print "<"+__name__+">: Running On MC:", runOnMC
print "<"+__name__+">: Samplename is:", legend


import FWCore.ParameterSet.Config as cms

process = cms.Process('myPhoSel')
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring( 'file:/net/data_cms/institut_3b/tholen/subsamples_Background/semiMuonBG.root' )
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TFILESERVICEmyPhotonSelection.root')
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

# input and presel
process.load("MyPackage.TtGammaAnalysis.sequenceHardPhoton_cfi")
process.load("MyPackage.TtGammaAnalysis.sequenceCocPatPhoton_cfi")
process.load("MyPackage.TtGammaAnalysis.pathOverlaps_cff")
process.load("MyPackage.PatTupelizer.myBTagRequirement_cfi")
process.load('MyPackage.TtGammaAnalysis.sequenceMcTruth_cfi')
process.load("MyPackage.TtGammaAnalysis.sequenceTtgammaMerging_cff")
process.photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("widenedCocPatPhotons"),
    cut = cms.string(""),
    filter = cms.bool(False)
)
process.preSel = cms.Sequence(process.myBTagRequirement * process.photonInputDummy)
if go4Signal:
    process.preSel.replace(process.myBTagRequirement, process.myBTagRequirement * process.photonsSignal)
if go4Noise:
    process.preSel.replace(process.myBTagRequirement, process.myBTagRequirement * ~process.photonsSignal)
if useMerging:
    process.preSel.insert(0, process.ttgammaMergingSequence)



# Number of Vertices
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


# Path declarations
process.producerPath = cms.Path(
    process.widenedCocPatPhotons
    * process.preSel
    #* process.largeEtPhotons
    #* process.cocPatPhotons
)

process.selectionPath = cms.Path(
    process.preSel
    #* process.largeEtFilter
    #* process.cocFilter
)

process.overlapsPath = cms.Path(
    process.preSel
    * process.analyzer_Photon
    * process.analyzer_ET
)

process.vtxMultPath = cms.Path(
    process.preSel
    * process.vertexHisto1BX
    * process.vertexHisto3D
    * process.vertexHistoGood1BX
    * process.vertexHistoGood3D
)

from MyPackage.TtGammaAnalysis.photonIDcuts_cff import add_photon_cuts
nMinusOnePaths = add_photon_cuts(process)

##############
#
# Cutflow
#
##############

process.analyzeSelection=cms.EDAnalyzer(
    "CheckSelection",
    processName=cms.string("myPhoSel"),
    pathNames=cms.vstring("selectionPath"),
    weights=cms.untracked.InputTag("puWeight", puReweight)
)

from MyPackage.TtGammaAnalysis.selectionTool import runSelectionTool
names=cms.vstring()
runSelectionTool(process, "selectionPath", names=names)
#put them in correct order not automated yet
selPathMods = str(process.selectionPath).split("+")
names=cms.vstring()
while selPathMods[0] != "photonInputDummy":
    selPathMods.pop(0)
for mod in selPathMods:
    names.append("ModulePath" + mod)
process.analyzeSelection.pathNames=names
process.analyzeSelection.processName=cms.string(process.process)
process.selAnalyze = cms.EndPath(process.analyzeSelection)


##############

# schedule
process.schedule = cms.Schedule(
    process.producerPath,
    process.selectionPath,
    process.overlapsPath,
)
if not on2to3whiz:
    process.schedule.append(process.vtxMultPath)

for path in nMinusOnePaths:
    process.schedule.append(path)

for name in names:
    process.schedule.append(getattr(process,name))
process.schedule.append(process.selAnalyze)


# DATA!
if not runOnMC:
    # TODO add EventIDPrinter to top/tools
    process.eventIDPrinter = cms.EDAnalyzer("EventIDPrinter")
    process.selectionPath.replace(
        process.cocFilter,
        process.cocFilter * process.eventIDPrinter
    )

