import os
import sys

class _MyUtility:
    class ConstError(TypeError): pass
    def __setattr__(self, name, value):
        if self.__dict__.has_key(name):
            #raise self.ConstError, "No dude, you would not _change_ the constant '%s'!"%name
            print "WARNING: constant '{0:>s}' is changed from '{1:>s}' to '{2:>s}'!".format(
                name,
                self.__dict__[name],
                value
            )
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
    def get_ini_file(self) :
        import sys
        return sys.argv[-1]

    def addFileService(self, process):
        self.add_file_service(process)

    def add_file_service(self, process) :
        """
        Creates a TFileService object, which is added to process.
        Takes the argument after cmsRun from sys.argv and uses it as
        filename. Directory will be created.
        """

        import os
        import sys
        import FWCore.ParameterSet.Config as cms

        # search config file name
        argv_index = 0
        basename = "noCmsRunInSysArgv"
        for token in sys.argv :
            argv_index += 1
            if token[-6:-1] == "cmsRu" :
                basename = sys.argv[argv_index][0:-3]
        
        file_service_dir = self.DIR_FILESERVICE
        if basename != "noCmsRunInSysArgv" and not os.path.exists(file_service_dir) :
            os.mkdir(file_service_dir)
        file_service_dir += '/'
        
        process.TFileService = cms.Service("TFileService",
          fileName = cms.string(file_service_dir + os.path.basename(basename + ".root"))
        )
    
sys.modules[__name__] = _MyUtility()
