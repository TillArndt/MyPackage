import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff import *

two2sevenMerger = cms.EDFilter(
    "Two2SevenMerger",
    ptCut = cms.double(10.),
    drCut = cms.double(0.1)
)

ttgammaMergingSequence = cms.Sequence(makeGenEvt * two2sevenMerger)
