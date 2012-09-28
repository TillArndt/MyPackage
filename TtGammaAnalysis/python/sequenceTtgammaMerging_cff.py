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
two2sevenMergingSequence = cms.Sequence(makeGenEvt * two2sevenMerger)

two2fiveMerger = cms.EDFilter(
    "Two2FiveMerger",
    ptCut = cms.double(10.),
    drCut = cms.double(0.1),
    is2to5 = cms.untracked.bool(True),
    legPtCut = cms.untracked.double(10.),
    filter = cms.bool(True)
)
two2fiveMergingSequence = cms.Sequence(makeGenEvt * two2fiveMerger)

two2threeMerger = two2fiveMerger.clone(
    is2to5 = cms.untracked.bool(False)
)
two2threeMergingSequence = cms.Sequence(makeGenEvt * two2threeMerger)