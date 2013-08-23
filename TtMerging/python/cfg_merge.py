

from FWCore.ParameterSet import Config as cms


process = cms.Process("MERGE")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(""))
process.p = cms.Path()
process.out = cms.OutputModule( "PoolOutputModule",
    outputCommands = cms.untracked.vstring( 'drop *' ),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    fileName=cms.untracked.string("merged.root")
)
from MyPackage.TtMerging.kept_collections import kept_collections
process.out.outputCommands += kept_collections
process.outPath = cms.EndPath(process.out)

sample = ""
try:
    sample = cms_var.get("sample", sample)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"
if "whiz" in sample:
    process.load("MyPackage.TtGamma8TeV.cfi_photonUserData")
    process.photonUserData.srcPhoton = "patPhotonsAllMatch"
    process.p += process.photonUserDataSequence


def add_with_counter(name):
    process.p += getattr(process, name)
    counter = cms.EDProducer("EventCountProducer")
    setattr(process, "EvtCnt" + name, counter)
    process.p += counter

process.BTagJet = cms.EDFilter("PATCandViewCountFilter",
    maxNumber = cms.uint32(10000),
    src = cms.InputTag("selectedPatJetsForAnalysisBTag"),
    minNumber = cms.uint32(1)
)
add_with_counter("BTagJet")


process.InputEventCount = cms.EDProducer("EventCountProducer")
process.OutputEventCount = cms.EDProducer("EventCountProducer")
process.p.insert(0, process.InputEventCount)
process.p += process.OutputEventCount


process.schedule = cms.Schedule(
    process.p,
    process.outPath
)
