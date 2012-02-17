__author__ = 'Heiner Tholen'

import os
from PyQt4 import QtCore
#from MyPackage.TtGammaAnalysis.CmsRunProcess import CmsRunProcess
#from MyPackage.TtGammaAnalysis.CmsRunController import CmsRunController

class CmsRunMonitor(QtCore.QObject):
    """
    CmsRunProcess monitoring. As of now, stuff is only printed to
    console.
    """
    def __init__(self):
        super(CmsRunMonitor, self).__init__()
        self.error_logs_opened = 0


    def proc_enqueued(self, process):
        print "process enqueued:   cmsRun ", process.conf_file_name


    def proc_started(self, process):
        print "process started :   cmsRun ", process.conf_file_name


    def proc_finished(self, process):
        print "process finished:   cmsRun ", process.conf_file_name


    def proc_failed(self, process):
        print "process FAILED  :   cmsRun ", process.conf_file_name
        if not self.error_logs_opened:
            print "_____________________________________________cmsRun logfile"
            os.system("cat " + process.log_file_name)
            self.error_logs_opened += 1


    def parser_error(self, process):
        if not process: # killed by sigint
            return
        print "ERROR parsing output of process " + process.name


    def all_finished(self):
        print "All processes finished"


    def message(self, string):
        print string


    def connect_controller(self, controller):
        controller.process_enqueued.connect(self.proc_enqueued)
        controller.process_started.connect(self.proc_started)
        controller.process_finished.connect(self.proc_finished)
        controller.process_failed.connect(self.proc_failed)
        controller.all_finished.connect(self.all_finished)


    def connect_parser(self, parser):
        parser.trigger_report_empty.connect(self.parser_error)
        parser.no_logfile.connect(self.parser_error)
        parser.message.connect(self.message)
