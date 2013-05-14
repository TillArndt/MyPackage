
import FWCore.ParameterSet.Config as cms


puWeight=cms.EDProducer("EvtWeightPU", 	
	generatedFile=cms.string("/user/kuessel/CMSSW/Synch/CMSSW_5_3_8_patch3/src/MyPackage/TtGamma8TeV/data/genpuS10.root"),
	dataFile=cms.string("/user/kuessel/CMSSW/Synch/CMSSW_5_3_8_patch3/src/MyPackage/TtGamma8TeV/data/PU_Run2012C-PromptReco-v2.root"),
	GenHistName=cms.string("pugen"),  
	DataHistName=cms.string("pileup")
)
