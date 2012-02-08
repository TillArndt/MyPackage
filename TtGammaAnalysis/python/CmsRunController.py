
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from MyPackage.TtGammaAnalysis.CmsRunProcess import CmsRunProcess
import MyPackage.TtGammaAnalysis.MyUtility as util


class CmsRunController(QtCore.QObject):
    def __init__(self):
        super(CmsRunController, self).__init__()
        self.waiting_pros = []
        self.running_pros = []
        self.finished_pros = []
        self.failed_pros = []


    #signal emited when lists are changed
    process_enqueued = QtCore.pyqtSignal(CmsRunProcess)
    process_started = QtCore.pyqtSignal(CmsRunProcess)
    process_finished = QtCore.pyqtSignal(CmsRunProcess)
    process_failed = QtCore.pyqtSignal(CmsRunProcess)
    all_finished = QtCore.pyqtSignal()


    def setup_processes(self, qsetting):
        """
        CmsRunProcesses are set up, and filled into self.waiting_pros
        CmsRunProcess.prepareRunConf(qsettings) is called for every
        process.
        """

        if len(self.waiting_pros) > 0: #setup has been done already
            return 
        
        self.qsetting = qsetting

        #load all cfg file setups
        cfg_file_abbrevs = qsetting.childGroups()
        for cfg_file in cfg_file_abbrevs:
            if qsetting.value(cfg_file + "/enable").toBool():
                qsetting.beginGroup(cfg_file)

                #load all cmsRun starts
                cmsRun_conf_abbrevs = qsetting.childGroups()
                for cmsRun_conf in cmsRun_conf_abbrevs:
                    if qsetting.value(cmsRun_conf + "/enable").toBool():
                        process = CmsRunProcess(cmsRun_conf)
                        process.prepare_run_conf(qsetting)
                        self.waiting_pros.append(process)
                        self.process_enqueued.emit(process)
                qsetting.endGroup()
                self.waiting_pros.append("CfgFileEnd") #mark cfg file end


    def start_processes(self):
        """
        Starts the qued processes.
        
        >>> qset = QtCore.QSettings("fakeFile.ini", 1)
        >>> crc = CmsRunController(qset)
        >>> crc.waiting_pros.append(CmsRunProcess("someName"))
        >>> crc.start_processes()
        >>> len(crc.waiting_pros)
        0
        >>> len(crc.running_pros)
        1
        """

        #block until cfg file is fully done
        if len(self.waiting_pros) > 0 and self.waiting_pros[0] == "CfgFileEnd":
            if len(self.running_pros) > 0:
                return
            else:
                self.waiting_pros.pop(0)
                self.start_processes
        
        #check if launch is possible
        num_proc, parse_ok = self.qsetting.value("maxProcesses", 2).toInt()
        if not parse_ok:
            num_proc = 2
        if len(self.waiting_pros) == 0 or len(self.running_pros) >= num_proc:
            return

        #now start processing
        process = self.waiting_pros.pop(0)
        process.finished.connect(self.finish_processes)
        process.start()
        self.running_pros.append(process)
        self.process_started.emit(process)

        #recursively
        self.start_processes()

    def finish_processes(self):
        """
        Remove finished processes from self.running_pros

        >>> qset = QtCore.QSettings("fakeFile.ini", 1)
        >>> crc = CmsRunController(qset)
        >>> crc.running_pros.append(CmsRunProcess("someName"))
        >>> crc.finish_processes()
        >>> len(crc.running_pros)
        0
        >>> len(crc.finished_pros)
        1
        >>> len(crc.failed_pros)
        0
        >>> crc.finished_pros[0].close()
        """

        for process in self.running_pros[:]:
            if process.state() == 0:
                self.running_pros.remove(process)
                if process.exitCode() == 0:
                    self.finished_pros.append(process)
                    self.process_finished.emit(process)                    
                else:
                    self.failed_pros.append(process)
                    self.process_failed.emit(process)

        #see if there is new processes to start
        self.start_processes()

        if len(self.running_pros) == 0:
            self.all_finished.emit()


    def abort_all_processes(self):
        """
        Waiting processes are dropped,
        running processes are terminated.
        """

        self.waiting_pros = []
        for process in self.running_pros:
            process.terminate()



if __name__ == '__main__':
    import doctest
    doctest.testmod()
