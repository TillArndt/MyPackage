__author__ = 'Heiner Tholen'

import os
from PyQt4 import QtCore

class CmsRunMonitor(QtCore.QObject):
    """
    CRProcess monitoring. As of now, stuff is only printed to
    console.
    """
    def __init__(self):
        super(CmsRunMonitor, self).__init__()
        self.error_logs_opened = 0


    def proc_enqueued(self, process):
        print "INFO process enqueued:   cmsRun ", process.conf_file_name


    def proc_started(self, process):
        print "INFO process started :   cmsRun ", process.conf_file_name


    def proc_finished(self, process):
        print "INFO process finished:   cmsRun ", process.conf_file_name


    def proc_failed(self, process):
        print "WARNING process FAILED  :   cmsRun ", process.conf_file_name
        if not self.error_logs_opened:
            print "_____________________________________________cmsRun logfile"
            os.system("cat " + process.log_file_name)
            self.error_logs_opened += 1


    def all_finished(self):
        print "INFO All processes finished"


    def message(self, sender, string):
        print string + " (" + str(type(sender)) + ")"


    def connect_controller(self, controller):
        controller.process_enqueued.connect(self.proc_enqueued)
        controller.process_started.connect(self.proc_started)
        controller.process_finished.connect(self.proc_finished)
        controller.process_failed.connect(self.proc_failed)
        controller.all_finished.connect(self.all_finished)
        controller.message.connect(self.message)


    def connect_post_processing_tool(self, tool):
        tool.message.connect(self.message)
