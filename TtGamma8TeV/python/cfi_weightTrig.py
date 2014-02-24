import FWCore.ParameterSet.Config as cms


#trigWeight = cms.EDProducer("TopTriggerWeight",
#    uncertMode = cms.untracked.int32(0),
#)


import os

path = os.environ["CMSSW_BASE"] + "/src/MyPackage/TtGamma8TeV/data/"
path += "SingleMuonTriggerEfficiencies_eta2p1_Run2012ABCD_v5trees.root"

trigWeight = cms.EDProducer("IsoMuTrigWeight",
    sfFile = cms.string(path),
    uncertMode = cms.untracked.int32(0),
)

trigWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src = cms.InputTag("trigWeight"),
    name = cms.untracked.string("histo"),
    title = cms.untracked.string(";trigger weight;events"),
    nbins = cms.untracked.int32(100),
    min = cms.untracked.double(0.),
    max = cms.untracked.double(2.),
)

trigWeightSequence = cms.Sequence(
    trigWeight *
    trigWeightHisto
)