#!/net/software_cms/slc5_amd64_gcc434/cms/cmssw/CMSSW_4_2_8/external/slc5_amd64_gcc434/bin/python

"""
This program manages cmsRun processes. It reads run information
from *.ini configuration files and starts cmsRun with proper
parameters.

author: Heiner Tholen
"""

import signal
import sys
import os
from PyQt4 import QtCore
import MyPackage.TtGammaAnalysis.MyUtility as util
from MyPackage.TtGammaAnalysis.CmsRunController import CmsRunController
from MyPackage.TtGammaAnalysis.CmsRunMonitor import CmsRunMonitor
from MyPackage.TtGammaAnalysis.CmsRunProcess import CmsRunProcess

class SigintHandler:
    def __init__(self, cmsRunController):
        self.cmsRunController = cmsRunController

    def handle(self, signal_int, frame):
        if signal_int is signal.SIGINT:
            self.cmsRunController.abort_all_processes()


def main():
    app = QtCore.QCoreApplication(sys.argv)
    qset = QtCore.QSettings(util.get_ini_file(),1)
    crc = CmsRunController()
    crc.setup_processes(qset)
    sig_handler = SigintHandler(crc)
    signal.signal(signal.SIGINT, sig_handler.handle)
    crc.all_finished.connect(app.quit)
    crm = CmsRunMonitor()
    crm.connect_controller(crc)
    crc.start_processes()
    return app.exec_()
    

if __name__ == '__main__':
    main()
    
