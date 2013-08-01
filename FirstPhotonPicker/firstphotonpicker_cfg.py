import FWCore.ParameterSet.Config as cms

FirstPhotonPicker = cms.EDProducer('FirstPhotonPicker',
    src = cms.InputTag("MyPatPhotonCollection"),
)
