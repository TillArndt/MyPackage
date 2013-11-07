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
    '',
]
process.out.fileName = 'out_patTuple.root'
process.TFileService.fileName = 'fileservice.root'

