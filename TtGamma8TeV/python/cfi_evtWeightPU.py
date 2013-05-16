
import os
path = os.environ["CMSSW_BASE"] + "/src/MyPackage/TtGamma8TeV/data/"

data_dist = "PU_Run2012.root" #"PU_Run2012C-PromptReco-v2.root"


import FWCore.ParameterSet.Config as cms

puWeight=cms.EDProducer("EvtWeightPU", 	
	generatedFile=cms.string(path + "genpuS10.root"),
	dataFile=cms.string(path + data_dist),
	GenHistName=cms.string("pugen"),  
	DataHistName=cms.string("pileup")
)

