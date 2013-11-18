runOnMC     = True

try:
    runOnMC     = not cms_var["is_data"]
except NameError:
    pass

import FWCore.ParameterSet.Config as cms

from MyPackage.TtGamma8TeV.cfi_bTagRequirement import *
from MyPackage.TtGamma8TeV.cfi_trigger import *

preSel = cms.Sequence(
    bTagSequence
)

if not runOnMC: # run trigger on data
    preSel *= triggerSelection

