# generated
# on Wed Jan 16 10:02:08 2013
# by cmsrunprocess.py

import __builtin__
__builtin__.cms_var = {'sample': '"DATAonGRID"', 'is_data': True}


from MyPackage.PatTupelizer.myttbarPatTuple_cfg import *

process.source.fileNames = [
    'file:/disk1/tholen/eventFiles/fromGrid20130207/testData.root',
]
process.out.fileName = 'out_patTuple.root'
process.out.outputCommands.insert(0, "keep *_*_*_RECO")
process.out.outputCommands.insert(0, "keep *_*_*_HLT")
process.out.outputCommands.insert(0, "keep *_*Jet*_*_*")
process.TFileService.fileName = 'out_fs.root'

process.p.remove(process.step0a)




