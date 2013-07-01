
puWeightInput = "PU_Run2012_69400.root"
try:
    puWeightInput  = cms_var.get("puWeightInput", puWeightInput)
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"

import os
path = os.environ["CMSSW_BASE"] + "/src/MyPackage/TtGamma8TeV/data/"


import FWCore.ParameterSet.Config as cms

puWeight=cms.EDProducer("EvtWeightPU", 	
	generatedFile=cms.string(path + "genpuS10.root"),
	dataFile=cms.string(path + puWeightInput),
	GenHistName=cms.string("pugen"),  
	DataHistName=cms.string("pileup")
)

