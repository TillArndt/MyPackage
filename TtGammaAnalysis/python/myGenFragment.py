
from Configuration.Generator.PythiaUESettings_cfi import *
generator = cms.EDFilter("Pythia6HadronizerFilter",
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(0.254),
    comEnergy = cms.double(7000.0),
    PythiaParameters = cms.PSet(
        pythiaUESettingsBlock,
        processParameters = cms.vstring('MSEL=0         ! User defined processes',
                        'PMAS(5,1)=4.4   ! b quark mass',
                        'PMAS(6,1)=173.1 ! t quark mass',
                        'MSTJ(1)=1       ! Fragmentation/hadronization on or off',
                        'MSTP(61)=0      ! parton ISR on or off',                                                     'MSTP(71)=0      ! parton FSR on or off'),
        # This is a vector of ParameterSet names to be read, in this order
        parameterSets = cms.vstring('pythiaUESettings',
            'processParameters')
    )
)

