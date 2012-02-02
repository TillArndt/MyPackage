

import sys, os
from PyQt4 import QtCore
import MyPackage.TtGammaAnalysis.myUtility as util

class cmsRunProcess(QtCore.QProcess):
    def __init__(self, name):
        super(cmsRunProcess, self).__init__()

        # set all surroundings
        self.setWorkingDirectory(os.getcwd())
        self.setEnvironment(QtCore.QProcess.systemEnvironment())
        self.setProcessChannelMode(1)
        self.setStandardOutputFile(util.DIR_LOGS + "/" + name + ".log")
        if not os.path.exists(util.DIR_LOGS):
            os.mkdir(util.DIR_LOGS)
        self.name = name
        self.exe = "cmsRun"
        self.confFileName = util.DIR_CONFS + "/" + name + ".py"

    def prepareRunConf(self, qsetting):
        
        confLines = [] # collect lines of confFile

        # starting statement
        import time
        confLines.append("# generated")
        confLines.append("# on " + time.ctime())
        confLines.append("# by cmsRunController.py")
        confLines.append("# using " + util.getIniFile())
        confLines.append("")
        
        # do import statement
        confLines.append(
            "from "
            + qsetting.value("cfgFile").toString()
            + " import *"
        )
        confLines.append("")

        # do input filename statements
        qsetting.beginGroup(self.name)
        confLines.append("process.source.fileNames = [")
        qsetting.beginGroup("eventInput")
        directory = qsetting.value("dir").toString()
        filenames = qsetting.value("files").toStringList()
        for filename in filenames:
            confLines.append("    '"
                             + directory + "/"
                             + filename + "',")
        qsetting.endGroup()        
        confLines.append("]")

        # do output filename statements
        if (qsetting.contains("eventOutput")
            and qsetting.value("eventOutput").toString() != ""):
            confLines.append(
                "process.out.fileName = '"
                + qsetting.value("eventOutput").toString()
                + "'"
            )

        # fileService statement
        confLines.append(
            "process.TFileService.fileName = '"
            + util.DIR_FILESERVICE + "/"
            + self.name + ".root'"
        )
        confLines.append("")

        # add extra lines
        # (not implemented yet)

        # go back to base level
        qsetting.endGroup()
        
        # write out file
        if not os.path.exists(util.DIR_CONFS):
            os.mkdir(util.DIR_CONFS)
        confFile = open(self.confFileName, "w")
        for line in confLines:
            confFile.write(line + "\n")
        confFile.close()

    def start(self):
        super(cmsRunProcess, self).start(self.exe, [self.confFileName])
