# generated
# on Wed Jan 16 10:02:08 2013
# by cmsrunprocess.py

import __builtin__
__builtin__.cms_var = {'sample': '"MConGRID"', 'isData': False}


from MyPackage.PatTupelizer.myttbarPatTuple_cfg import *

process.source.fileNames = [
    'file:/disk1/tholen/eventFiles/ttbar_testfile.root',
]
process.out.fileName = 'out_patTuple.root'
process.TFileService.fileName = 'out_fs.root'

