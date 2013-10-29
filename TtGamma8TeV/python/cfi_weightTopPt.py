preSelOpt = None
try:
    print "cms_var options: "
    print cms_var
    preSelOpt = cms_var.get("preSelOpt",preSelOpt)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"


import FWCore.ParameterSet.Config as cms


topPtTTbar          = cms.EDProducer("TopPtProducer")
topPtWeight         = cms.EDProducer("TopPtWeight")
topPtHistoVanilla   = cms.EDAnalyzer("TopPtHisto")
topPtHistoWeighted  = cms.EDAnalyzer("TopPtHisto",
    weights = cms.untracked.InputTag("topPtWeight"),
)
if preSelOpt == "go4Whiz":
    topPtTTbar.two2fiveMode = cms.untracked.bool(True)

topPtWeightHisto    = cms.EDAnalyzer("DoubleValueHisto",
    src     = cms.InputTag("topPtWeight"),
    name    = cms.untracked.string("histo"),
    title   = cms.untracked.string(";top quark pt weight;events"),
    nbins   = cms.untracked.int32(100),
    min     = cms.untracked.double(0.),
    max     = cms.untracked.double(2.),
)

weightTopPtSequence = cms.Sequence(
    topPtTTbar
    * topPtWeight
    * topPtHistoVanilla
    * topPtHistoWeighted
    * topPtWeightHisto
)

