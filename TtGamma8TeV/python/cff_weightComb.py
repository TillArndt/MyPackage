preSelOpt = None
runOnMC   = True

try:
    preSelOpt   = cms_var.get("preSelOpt",preSelOpt)
    runOnMC     = not cms_var["is_data"]
except NameError:
    pass

import FWCore.ParameterSet.Config as cms
from MyPackage.TtGamma8TeV.cfi_weightBTag import *
from MyPackage.TtGamma8TeV.cfi_weightTopPt import *
from MyPackage.TtGamma8TeV.cfi_weightPU import *
from MyPackage.TtGamma8TeV.cfi_weightTrig import *
from MyPackage.TtGamma8TeV.cfi_weightMCatNLO import *

weightComb = cms.EDProducer("DoubleProduct",
    src = cms.VInputTag(
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


weightCombSequence = cms.Sequence(
    bTagWeightSequence *
    puWeightSequence
)

if preSelOpt in ("doOverlapRemoval", "go4Whiz","MadG_Signal"):
    weightComb.src.append(cms.InputTag("topPtWeight"))
    weightCombSequence *= weightTopPtSequence

if runOnMC:
    weightComb.src.append(cms.InputTag("trigWeight"))
    weightCombSequence *= trigWeightSequence

weightCombSequence *= weightComb
weightCombSequence *= weightCombHisto
