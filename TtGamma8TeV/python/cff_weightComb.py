preSelOpt = None

try:
    print "cms_var options: "
    print cms_var
    preSelOpt   = cms_var.get("preSelOpt",preSelOpt)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import FWCore.ParameterSet.Config as cms
from MyPackage.TtGamma8TeV.cfi_weightBTag import *
from MyPackage.TtGamma8TeV.cfi_weightTopPt import *
from MyPackage.TtGamma8TeV.cfi_evtWeightPU import *
from MyPackage.TtGamma8TeV.cfi_weightMCatNLO import *

weightComb = cms.EDProducer("DoubleProduct",
	src=cms.VInputTag(
		cms.InputTag("puWeight","PUWeightTrue"),
		cms.InputTag("bTagWeight"),
		)
	)

weightCombHisto = cms.EDAnalyzer("DoubleValueHisto",
    src = cms.InputTag("weightComb"),
    name = cms.untracked.string("histo"),
    title = cms.untracked.string(";final event weight;events"),
    nbins = cms.untracked.int32(100),
    min = cms.untracked.double(0.),
    max = cms.untracked.double(2.),
)


weightCombSequence=cms.Sequence(
	bTagWeightSequence*
	puWeightSequence
)

if preSelOpt in ("doOverlapRemoval", "go4Whiz"):
	weightComb.src.append(cms.InputTag("topPtWeight"))
	weightCombSequence *= weightTopPtSequence

weightCombSequence*=weightComb
