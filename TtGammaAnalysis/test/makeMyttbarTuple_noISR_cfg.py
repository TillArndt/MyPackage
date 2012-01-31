
from MyPackage.TtGammaAnalysis.myttbarPatTuple_cfg import *

#input
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring(
    'file:/user/tholen/eventFiles/ttgamma_whizard_noISR.root'
 )
)

process.out.fileName = "file:/user/tholen/eventFiles/ttgamma_whizard_noISR_PatTuple.root"



