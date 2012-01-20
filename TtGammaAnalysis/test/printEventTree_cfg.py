import FWCore.ParameterSet.Config as cms
import sys

process = cms.Process('DumpEventTree')

process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
      'file:' + sys.argv[2]
 )
)

#max num of events processed
numEvents = 1
if len(sys.argv) > 3 :
    numEvents = int(sys.argv[3])
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(numEvents))

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#from Configuration.PyReleaseValidation.autoCond import autoCond
process.GlobalTag.globaltag = cms.string('START42_V13::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load( "SimGeneral.HepPDTESSource.pythiapdt_cfi" )


process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src =cms.InputTag( "genParticles" ),
                                   printP4 = cms.untracked.bool( True ),
                                   printIndex = cms.untracked.bool(True),
                                   printStatus = cms.untracked.bool(True)
                                   )


process.p = cms.Path(process.printTree)


