
from MyPackage.TtGammaAnalysis.myttbarPatTuple_cfg import *

#input
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:/user/tholen/eventFiles/ttgamma_whizard_noISR_noFSR.root'
 )
)

process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_whizard_noISR_noFSR_PatTuple.root"



