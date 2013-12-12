
import FWCore.ParameterSet.Config as cms

filterJER = cms.EDFilter("FilterJER",
    src = cms.InputTag("selectedPatJetsForAnalysis"),
    cut1 = cms.double(55.),
    cut2 = cms.double(45.),
    cut3 = cms.double(35.),
    cut4 = cms.double(20.),
)