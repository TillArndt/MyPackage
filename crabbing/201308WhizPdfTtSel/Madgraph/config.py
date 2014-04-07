# generated
# on Fri May 31 15:13:54 2013
# by cmsrunprocess.py

import __builtin__
__builtin__.cms_var = {
    'isData'     : False, 
    'skim'       : False, 
    'btag'       : False, 
    'procName'   : 'PAT',
    'globalTag'  : 'START53_V23',
}

from MyPackage.TtSelection.yv_config import *

process.source.fileNames = [
    'file:/afs/cern.ch/work/t/tarndt/private/Test/CMSSW_5_3_15/src/MyPackage/crabbing/201308WhizPdfTtSel/Madgraph/out_STEP2_1_1_2e0.root',
]
process.out.fileName = 'out_patTuple.root'
process.TFileService.fileName = 'fileservice.root'

