import FWCore.ParameterSet.Config as cms
import sys, os

def addFileService(process) :
    
    # search config file name
    argvIndex = 0
    basename = "noCmsRunInSysArgv"
    for token in sys.argv :
        argvIndex += 1
        if token[-6:-1] == "cmsRu" :
            basename = sys.argv[argvIndex][0:-3]

    fileServiceDir = "outputFileService"
    if basename != "noCmsRunInSysArgv" and not os.path.exists(fileServiceDir) :
        os.mkdir(fileServiceDir)
    fileServiceDir += '/'
    
    process.TFileService = cms.Service("TFileService",
      fileName = cms.string(fileServiceDir + os.path.basename(basename + ".root"))
    )
