import os, sys
import FWCore.ParameterSet.Config as cms

class _myUtility:
    class ConstError(TypeError): pass
    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            raise self.ConstError, "No dude, you would not _change_ the constant '%s'!"%name
        self.__dict__[name]=value
        
    def __delattr__(self, name):
        if self.__dict__.has_key(name):
            raise self.ConstError, "No dude, you would not _delete_ the constant '%s'!"%name

###########
# constants
###########
    def __init__(self):
        self.DIR_FILESERVICE = "outputFileService"
        self.DIR_LOGS        = "outputLogs"
        self.DIR_CONFS       = "outputConfs"

###########
# functions
###########
    def getIniFile(self) :
        import sys
        return sys.argv[-1]

    def addFileService(self, process) :
        
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
    
sys.modules[__name__] = _myUtility()
