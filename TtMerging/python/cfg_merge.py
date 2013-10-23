

from FWCore.ParameterSet import Config as cms


process = cms.Process("MERGE")
process.load('FWCore.MessageService.MessageLogger_cfi')
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('TFILESERVICE_cfg_merge.root')
)

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


#TODO: require photon candidate with ET > 20 GeV and abs(eta) < 1.5 or so!!

#process.load("Configuration.Geometry.GeometryIdeal_cff")
#process.load("MagneticField.Engine.uniformMagneticField_cfi")
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V23::All', '')


process.load("MyPackage.TtGamma8TeV.cfi_photonUserData")
#process.photonUserData.srcPhoton = "patPhotonsAllMatch"
process.p += process.photonUserDataSequence


process.InputEventCount = cms.EDProducer("EventCountProducer")
process.OutputEventCount = cms.EDProducer("EventCountProducer")
process.p.insert(0, process.InputEventCount)
process.p += process.OutputEventCount


process.schedule = cms.Schedule(
    process.p,
    process.outPath
)

