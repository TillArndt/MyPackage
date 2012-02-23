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
    message           = QtCore.pyqtSignal(QtCore.QObject, str)
    all_finished      = QtCore.pyqtSignal(list)

    def __init__(self):
        super(CmsRunController, self).__init__()
        self.waiting_pros  = []
        self.running_pros  = []
        self.finished_pros = []
        self.failed_pros   = []


    def setup_processes(self, qsetting, try_reuse = False):
        """
        CmsRunProcesses are set up, and filled into self.waiting_pros
        CmsRunProcess.prepareRunConf(qsettings) is called for every
        process.
        """

        if len(self.waiting_pros): #setup has been done already
            return 

        # preparation
        self.qsetting = qsetting
        enable_by_default = qsetting.value("enableByDefault",
                                           True).toBool()

        #load all cmsRun starts
        cmsRun_conf_abbrevs = qsetting.childGroups()
        cmsRun_conf_abbrevs.removeAll(QtCore.QString("fileSets"))

        # loop over runs
        for cmsRun_conf in cmsRun_conf_abbrevs:

            # check for enabled
            if not qsetting.value(cmsRun_conf + "/enable",
                                  enable_by_default).toBool():
                continue

            # create processes
            process = CmsRunProcess(cmsRun_conf, try_reuse)
            process.message.connect(self.message)
            process.prepare_run_conf(qsetting)
            self.waiting_pros.append(process)
            self.process_enqueued.emit(process)


    def start_processes(self):
        """
        Starts the qued processes.
        """

        # check if launch is possible
        num_proc, parse_ok = self.qsetting.value("maxNumProcesses", 2).toInt()
        if not parse_ok:
            self.message.emit(self, "ERROR maxNumProcesses not parseable! Using 2.")
            num_proc = 2
        if len(self.waiting_pros) == 0:
            return
        if len(self.running_pros) >= num_proc:
            return

        # now start processing
        process = self.waiting_pros.pop(0)
        process.finished.connect(self.finish_processes)
        process.start()
        self.running_pros.append(process)
        self.process_started.emit(process)

        # recursively
        self.start_processes()


    def finish_processes(self):
        """
        Remove finished processes from self.running_pros.
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

        # see if there is new processes to start
        self.start_processes()

        if not len(self.running_pros):
            self.all_finished.emit(self.finished_pros)


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
from MyPackage.TtGammaAnalysis.CmsRunPostProcessor import CmsRunPostProcessor

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

    letters  = 'r'
    opts, extraparams = getopt.getopt(sys.argv[1:], letters)

    try_reuse_results = False
    for opt, value in opts:

        if opt == "-r":
            try_reuse_results = True

    # settings
    qset = QtCore.QSettings(util.get_ini_file(),1)
    try_reuse_results =\
        qset.value("tryReuseResults", try_reuse_results).toBool()

    # app, monitor
    app = QtCore.QCoreApplication(sys.argv)
    crm = CmsRunMonitor()

    # controller
    crc = CmsRunController()
    crm.connect_controller(crc)

    # post processor
    crpp = CmsRunPostProcessor()
    crc.process_finished.connect(crpp.start)
    crc.all_finished.connect(crpp.start)

    # cutflow parser
    crp = CmsRunCutflowParser(qset)
    crm.connect_post_processing_tool(crp)
    crpp.add_tool(crp)

    # histo stakker
    crh = CmsRunHistoStacker(qset)
    crm.connect_post_processing_tool(crh)
    crpp.add_tool(crh)

    # SIGINT handler
    sig_handler = SigintHandler(crc)
    signal.signal(signal.SIGINT, sig_handler.handle)

    # connect for quiting (all other finishing connections before)
    crc.all_finished.connect(app.quit)

    # GO!
    crc.setup_processes(qset, try_reuse_results)
    crc.start_processes()
    return app.exec_()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
