

import sys, os
from PyQt4 import QtCore
import MyPackage.TtGammaAnalysis.MyUtility as util

class CmsRunProcess(QtCore.QProcess):
    """
    This class host a cmsRun process.
    Output is streamed into logfile.

    """
    
    def __init__(self, name):        
        super(CmsRunProcess, self).__init__()

        # set all surroundings
        self.setWorkingDirectory(os.getcwd())
        self.setEnvironment(QtCore.QProcess.systemEnvironment())
        self.setProcessChannelMode(1)
        self.setStandardOutputFile(util.DIR_LOGS + "/" + name + ".log")
        if not os.path.exists(util.DIR_LOGS):
            os.mkdir(util.DIR_LOGS)
        self.name = name
        self.exe = "cmsRun"
        self.conf_file_name = util.DIR_CONFS + "/" + name + ".py"

    def prepare_run_conf(self, qsetting):
        """
        Takes all infos about the cmsRun to be started from the
        qsettings object and builds a configuration file with
        python code, which is passed to cmsRun.
        Conf-Dir might be created. Conf-file stored in it.
        """
        
        conf_lines = [] # collect lines of confFile

        # starting statement
        import time
        conf_lines.append("# generated")
        conf_lines.append("# on " + time.ctime())
        conf_lines.append("# by cmsRunController.py")
        conf_lines.append("# using " + util.get_ini_file())
        conf_lines.append("")
        
        # do import statement
        conf_lines.append(
            "from "
            + qsetting.value("cfgFile").toString()
            + " import *"
        )
        conf_lines.append("")

        qsetting.beginGroup(self.name) # switch to process specific part

        # do input filename statements
        qsetting.beginGroup("eventInput")        
        if qsetting.contains("files") or qsetting.contains("abbrevs"):
            conf_lines.append("process.source.fileNames = [")
            directory = qsetting.value("dir").toString()
            if len(directory) > 0 and directory[-1] is not "/":
                directory.append("/")
            filenames = qsetting.value("files").toStringList()
            for filename in filenames:
                conf_lines.append("    '" + directory
                                  + filename + "',")
            conf_lines.append("]")
        qsetting.endGroup() #eventInput

        # do output filename statements
        if (qsetting.contains("eventOutput")
            and qsetting.value("eventOutput").toString() != ""):
            conf_lines.append(
                "process.out.fileName = '"
                + qsetting.value("eventOutput").toString()
                + "'"
            )

        # fileService statement
        conf_lines.append(
            "process.TFileService.fileName = '"
            + util.DIR_FILESERVICE + "/"
            + self.name + ".root'"
        )
        conf_lines.append("")

        # add extra lines
        conf_lines.append("#extraCode:")
        conf_lines.append(qsetting.value("extraCode","").toString())
 
        qsetting.endGroup() # self.name (process specific part)
        
        # write out file
        if not os.path.exists(util.DIR_CONFS):
            os.mkdir(util.DIR_CONFS)
        conf_file = open(self.conf_file_name, "w")
        for line in conf_lines:
            conf_file.write(line + "\n")
        conf_file.close()

    def start(self):
        super(CmsRunProcess, self).start(self.exe, [self.conf_file_name])
