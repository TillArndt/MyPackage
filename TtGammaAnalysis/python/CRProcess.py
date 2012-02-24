__author__ = 'Heiner Tholen'

import time
import os
from PyQt4 import QtCore
import MyPackage.TtGammaAnalysis.MyUtility as util

class CRProcess(QtCore.QProcess):
    """
    This class hosts a cmsRun process.
    Output is streamed into logfile.
    """

    message = QtCore.pyqtSignal(QtCore.QObject, str)

    def __init__(self, name, try_reuse_old_data = False):
        super(CRProcess, self).__init__()

        self.name               = name
        self.exe                = "cmsRun"
        self.log_file_name      = util.DIR_LOGS + "/" + str(name) + ".log"
        self.conf_file_name     = util.DIR_CONFS + "/" + str(name) + ".py"
        self.service_file_name  = util.DIR_FILESERVICE\
                                 + "/" + str(name) + ".root"
        self.info_file_name     = util.DIR_PROCESS_INFO + "/" + str(name) + ".log"
        self.try_reuse_old_data = try_reuse_old_data
        self.reused_old_data    = False
        self.sig_int            = False

        # set all surroundings
        self.setWorkingDirectory(os.getcwd())
        self.setEnvironment(QtCore.QProcess.systemEnvironment())
        self.setProcessChannelMode(1)
        self.setStandardOutputFile(self.log_file_name)
        if not os.path.exists(util.DIR_LOGS):
            os.mkdir(util.DIR_LOGS)
        self.finished.connect(self.write_process_info_file)


    def prepare_run_conf(self, qsetting):
        """
        Takes all infos about the cmsRun to be started from the
        qsettings object and builds a configuration file with
        python code, which is passed to cmsRun on calling start().
        Conf-Dir might be created. Conf-file stored in it.
        """

        if self.try_reuse_old_data and self.check_reuse_possible():
            return

        conf_lines = [] # collect lines of confFile

        # starting statement
        conf_lines.append("# generated")
        conf_lines.append("# on " + time.ctime())
        conf_lines.append("# by CRController.py")
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


    def write_process_info_file(self, exit_code):
        """
        Writes start and endtime as well as exitcode to the process info file.
        If self.sigint is true, deletes old file and does not write anything.
        """

        self.time_end = time.ctime()

        # on SIGINT do not write the process info
        if self.sig_int:
            return

        # on reuse, do also not overwrite file
        if self.reused_old_data:
            return

        # collect lines to be written at once
        info_lines = []
        info_lines.append("Start   :" + self.time_start)
        info_lines.append("End     :" + self.time_end)
        info_lines.append("Exitcode:" + str(exit_code))

        # write out
        if not os.path.exists(util.DIR_PROCESS_INFO):
            os.mkdir(util.DIR_PROCESS_INFO)
        file = open(self.info_file_name, "w")
        for line in info_lines:
            file.write(line + "\n")
        file.close()


    def check_reuse_possible(self):
        """
        Checks if log, conf and file service files are present and if the
        process was finished successfully before. If yes returns True,
        because the previous results can be used again.
        """

        if not os.path.exists(self.log_file_name):
            return False
        if not os.path.exists(self.conf_file_name):
            return False
        if not os.path.exists(self.service_file_name):
            return False
        if not os.path.exists(self.info_file_name):
            return False

        # search tokens
        # TODO: Think about tokens for PostProcessing, is it needed?
        exit_code_good = False
        info_file = open(self.info_file_name, "r")
        for line in info_file.readlines():
            tokens = line.split(":")
            if tokens[0] == "Exitcode" and not int(tokens[1]):
                exit_code_good = True
        info_file.close()

        if exit_code_good:
            return True
        else:
            return False


    def start(self):
        """
        Start cmsRun with conf-file. If self.try_reuse is True and reuse is
        possible, just calls 'cmsRun --help' and pipes output to /dev/null.
        """

        self.time_start =  time.ctime()

        if self.try_reuse_old_data and self.check_reuse_possible():
            self.setStandardOutputFile("/dev/null")
            self.reused_old_data = True
            self.message.emit(self, "INFO reusing data for " + self.name)
            super(CRProcess, self).start(self.exe, ["--help"])
        else:
            if os.path.exists(self.info_file_name):
                os.remove(self.info_file_name)
            super(CRProcess, self).start(self.exe, [self.conf_file_name])


    def terminate(self):
        """
        Overwrites terminate method, set's flag for infofile first, then calls
        terminate.
        """

        self.sig_int = True
        super(CRProcess,self).terminate()