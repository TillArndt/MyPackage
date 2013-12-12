puWeightInput = "PU_Run2012_69400.root"
try:
    puWeightInput  = cms_var.get("puWeightInput", puWeightInput)
except NameError:
    pass

import os
path = os.environ["CMSSW_BASE"] + "/src/MyPackage/TtGamma8TeV/data/"

import FWCore.ParameterSet.Config as cms

puWeight = cms.EDProducer("EvtWeightPU",
	generatedFile   = cms.string(path + "genpuS10.root"),
	dataFile        = cms.string(path + puWeightInput),
	GenHistName     = cms.string("pugen"),
	DataHistName    = cms.string("pileup"),
    weights         = cms.untracked.InputTag(""),
)


puWeightHisto = cms.EDAnalyzer("DoubleValueHisto",
    src = cms.InputTag("puWeight","PUWeightTrue"),
    name = cms.untracked.string("histo"),
    title = cms.untracked.string(";PU Weight ;events"),
    nbins = cms.untracked.int32(100),
    min = cms.untracked.double(0.),
    max = cms.untracked.double(2.),
)

puWeightSequence = cms.Sequence(
	puWeight*
	puWeightHisto
)
