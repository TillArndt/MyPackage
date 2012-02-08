
from PyQt4 import QtCore
from MyPackage.TtGammaAnalysis.CmsRunProcess import CmsRunProcess
from MyPackage.TtGammaAnalysis.CmsRunController import CmsRunController


class CmsRunMonitor(QtCore.QObject):
    """
    CmsRunProcess monitoring. As of now, stuff is only printed to
    console.
    """
    def __init__(self):
        super(CmsRunMonitor, self).__init__()


    def proc_enqueued(self, process):
        print "process enqueued:   cmsRun ", process.conf_file_name


    def proc_started(self, process):
        print "process started :   cmsRun ", process.conf_file_name


    def proc_finished(self, process):
        print "process finished:   cmsRun ", process.conf_file_name


    def proc_failed(self, process):
        print "process FAILED  :   cmsRun ", process.conf_file_name


    def all_finished(self):
        print "All processes finished"

    def connect_controller(self, controller):
        controller.process_enqueued.connect(self.proc_enqueued)
        controller.process_started.connect(self.proc_started)
        controller.process_finished.connect(self.proc_finished)
        controller.process_failed.connect(self.proc_failed)
        controller.all_finished.connect(self.all_finished)

