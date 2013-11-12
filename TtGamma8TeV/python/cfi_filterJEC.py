
runOnMC     = True

try:
    runOnMC     = not cms_var["is_data"]
except NameError:
    print "<"+__name__+">: cms_var not in __builtin__!"
print "<"+__name__+">: Running On MC:", runOnMC


import FWCore.ParameterSet.Config as cms

import os
path = os.environ["CMSSW_BASE"] + "/src/MyPackage/TtGamma8TeV/data/"

if runOnMC:
    path += "Summer13_V4_MC_Uncertainty_AK5PFchs.txt"
else:
    path += "Summer13_V4_DATA_Uncertainty_AK5PFchs.txt"

filterJEC = cms.EDFilter("FilterJEC",
    src = cms.InputTag("selectedPatJetsForAnalysis"),
    uncertFile = cms.string(path),
    cut1 = cms.double(55.),
    cut2 = cms.double(45.),
    cut3 = cms.double(35.),
    cut4 = cms.double(20.),
)