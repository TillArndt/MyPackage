

#max num of events processed
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#from Configuration.PyReleaseValidation.autoCond import autoCond
process.GlobalTag.globaltag = cms.string('START42_V13::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load( "SimGeneral.HepPDTESSource.pythiapdt_cfi" )


process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src =cms.InputTag( "genParticles" ),
                                   printP4 = cms.untracked.bool( True ),
                                   printIndex = cms.untracked.bool(False)
                                   )

