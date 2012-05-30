
# fetch variables from CmsRunController
runOnMC = True
legend  = NameError
try:
    runOnMC = not crc_var["isData"]
    legend  = crc_var["legend"]
except NameError:
    print "<myPhotonSelection_cfg>: crc_var not in __builtin__!"
print "<myPhotonSelection_cfg>: Running On MC:", runOnMC
print "<myPhotonSelection_cfg>: Samplename is:", legend



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

# input dummy
process.photonInputDummy = cms.EDFilter("PATPhotonSelector",
    src = cms.InputTag("patPhotonsPFlow"),
    cut = cms.string(""),
    filter = cms.bool(False)
)

# Selection of events with a hard photon
process.load("MyPackage.TtGammaAnalysis.sequenceHardPhoton_cfi")
process.load("MyPackage.TtGammaAnalysis.sequenceCocPatPhoton_cfi")


# EventIDPrinter (not added to Path, do this in extraCode!)
# TODO add EventIDPrinter to top/tools
process.eventIDPrinter = cms.EDAnalyzer("EventIDPrinter")

# analyze bump in pt spectrum around 100 GeV
process.load("MyPackage.TtGammaAnalysis.analyzerBump_cfi")

# Path declaration
process.selectionPath = cms.Path(
      process.photonInputDummy
#    * process.analyzer_Bump
    * process.hardPhotonSequence
    * process.cocPatPhotonSequence
)

# other paths
process.load("MyPackage.TtGammaAnalysis.pathOverlaps_cff")
process.load("MyPackage.TtGammaAnalysis.sequenceTtgammaMerging_cff")

# schedule
process.schedule = cms.Schedule(
    process.selectionPath,
    process.overlapsPath
)

# ttbar background
if legend == "Semi-#mu t#bart":
    process.selectionPath.insert(0, process.ttgammaMergingSequence)
    process.overlapsPath.insert(0, process.ttgammaMergingSequence)
