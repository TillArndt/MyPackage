import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff import *

two2sevenMerger = cms.EDFilter(
    "Two2SevenMerger",
    ptCut = cms.double(10.),
    drCut = cms.double(0.1),
    is2to7 = cms.untracked.bool(True),
    legPtCut = cms.untracked.double(10.),
    filter = cms.bool(True)
)

ttgammaMergingSequence = cms.Sequence(makeGenEvt * two2sevenMerger)
