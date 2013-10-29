# fetch variables from CmsRunController
runOnMC     = True
legend      = ""
sample      = ""

try:
    print "cms_var options: "
    print cms_var
    runOnMC     = not cms_var["is_data"]
    legend      = cms_var["legend"]
    sample      = cms_var.get("sample", sample)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"
print "<"+__name__+">: Running On MC:", runOnMC
print "<"+__name__+">: Samplename is:", sample


import FWCore.ParameterSet.Config as cms

process = cms.Process('SignalTemplate')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring( '' ),
    noEventSort = cms.untracked.bool( True ),
    inputCommands = cms.untracked.vstring(
        'keep *',
        'drop *_conditionsInEdm_*_*',
        'drop *_logErrorTooManyClusters_*_*',
    )
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TFILESERVICE_cfg_templateDatDrvSig.root')
)

import FWCore.MessageService.MessageLogger_cfi as logger
logger.MessageLogger.cerr.FwkReport.reportEvery = 100
logger.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.extend(logger)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.load("MyPackage.TtGamma8TeV.cff_templateDatDrvSig")

process.p = cms.Path(
    process.signalTemplateSequence
)

if runOnMC:
    process.p += process.signalTemplateTruthSequence

