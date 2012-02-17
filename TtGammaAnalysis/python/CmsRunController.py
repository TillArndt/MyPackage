__author__ = 'Heiner Tholen'

from PyQt4 import QtCore
from MyPackage.TtGammaAnalysis.CmsRunProcess import CmsRunProcess


class CmsRunController(QtCore.QObject):
    """
    Generates, starts and finishes CmsRunProcesses.
    """

    #signal emited when lists are changed
    process_enqueued  = QtCore.pyqtSignal(CmsRunProcess)
    process_started   = QtCore.pyqtSignal(CmsRunProcess)
    process_finished  = QtCore.pyqtSignal(CmsRunProcess)
    process_failed    = QtCore.pyqtSignal(CmsRunProcess)
    cfg_file_finished = QtCore.pyqtSignal(str)
    all_finished      = QtCore.pyqtSignal()


    def __init__(self):
        super(CmsRunController, self).__init__()
        self.waiting_pros  = []
        self.running_pros  = []
        self.finished_pros = []
        self.failed_pros   = []


    def setup_processes(self, qsetting):
        """
        CmsRunProcesses are set up, and filled into self.waiting_pros
        CmsRunProcess.prepareRunConf(qsettings) is called for every
        process.
        """

        if len(self.waiting_pros): #setup has been done already
            return 
        
        self.qsetting = qsetting

        #load all cfg file setups
        cfg_file_abbrevs = qsetting.childGroups()
        for cfg_file in cfg_file_abbrevs:
            if qsetting.value(cfg_file + "/enable", True).toBool():
                qsetting.beginGroup(cfg_file)

                #load all cmsRun starts
                enable_by_default = qsetting.value("enableByDefault",
                                                   True).toBool()
                cmsRun_conf_abbrevs = qsetting.childGroups()
                cmsRun_conf_abbrevs.removeAll(QtCore.QString("fileSets"))
                for cmsRun_conf in cmsRun_conf_abbrevs:
                    if qsetting.value(cmsRun_conf + "/enable",
                                      enable_by_default).toBool():
                        process = CmsRunProcess(cmsRun_conf)
                        process.prepare_run_conf(qsetting)
                        self.waiting_pros.append(process)
                        self.process_enqueued.emit(process)
                qsetting.endGroup()

                # mark cfg file end
                self.waiting_pros.append("CfgFileEnd " + str(cfg_file))


    def start_processes(self):
        """
        Starts the qued processes.

        >>> crc = CmsRunController()
        >>> crc.qsetting = QtCore.QSettings('fakeFile.ini', 1) # fake
        >>> crc.waiting_pros.append(CmsRunProcess("someName"))
        >>> crc.waiting_pros.append("CfgFileEnd the_cfg_file")
        >>> crc.start_processes()
        >>> len(crc.waiting_pros)
        1
        >>> len(crc.running_pros)
        1
        >>> crc.running_pros = []
        >>> crc.start_processes()
        >>> len(crc.waiting_pros)
        0
        >>> len(crc.running_pros)
        0
        """

        # on cfg file end, block until it's fully done
        if (len(self.waiting_pros) > 0 and
            str(self.waiting_pros[0]).split()[0] == "CfgFileEnd"):
            if len(self.running_pros) > 0:
                return
            else:
                cfg_end_token = self.waiting_pros.pop(0)
                self.cfg_file_finished.emit(cfg_end_token.split()[-1])
                self.start_processes()
        
        #check if launch is possible
        num_proc, parse_ok = self.qsetting.value("maxNumProcesses", 2).toInt()
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

        >>> crc = CmsRunController()
        >>> crc.qsetting = QtCore.QSettings('fakeFile.ini', 1) # fake
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


import signal
import sys
import getopt
from PyQt4 import QtCore
import MyPackage.TtGammaAnalysis.MyUtility as util
from MyPackage.TtGammaAnalysis.CmsRunMonitor import CmsRunMonitor
from MyPackage.TtGammaAnalysis.CmsRunCutflowParser import CmsRunCutflowParser
from MyPackage.TtGammaAnalysis.CmsRunHistoStacker import CmsRunHistoStacker

class SigintHandler:
    def __init__(self, controller):
        self.controller = controller

    def handle(self, signal_int, frame):
        if signal_int is signal.SIGINT:
            self.controller.abort_all_processes()


def main():
    """
    Main...
    """

    letters  = 'n:s:'
    opts, extraparams = getopt.getopt(sys.argv[1:], letters)

    # instantiations for both, single tool and normal run
    qset = QtCore.QSettings(util.get_ini_file(),1)
    crp = CmsRunCutflowParser(qset)
    crh = CmsRunHistoStacker(qset)

    # single tools only
    no_process_setup = False
    no_cmsRun_execute = False
    for opt, value in opts:

        if opt == "-s":
            no_process_setup = True
            crh.stack_it_all(value)

        if opt == "-n":
            no_cmsRun_execute = True

    if no_process_setup:
        return 0

    # normal run from here on
    app = QtCore.QCoreApplication(sys.argv)

    crc = CmsRunController()
    crc.setup_processes(qset)

    # cutflow parser
    crc.process_finished.connect(crp.parse_cutflow_process)
    crc.all_finished.connect(crp.sync_qsetting)
    crc.all_finished.connect(app.quit)

    # histo stakker
    crc.cfg_file_finished.connect(crh.stack_it_all)

    crm = CmsRunMonitor()
    crm.connect_controller(crc)
    crm.connect_parser(crp)

    sig_handler = SigintHandler(crc)
    signal.signal(signal.SIGINT, sig_handler.handle)

    crc.start_processes()
    return app.exec_()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
