#!/net/software_cms/slc5_amd64_gcc434/cms/cmssw/CMSSW_4_2_8/external/slc5_amd64_gcc434/bin/python
#!/afs/cern.ch/cms/slc5_amd64_gcc434/cms/cmssw/CMSSW_4_2_8/external/slc5_amd64_gcc434/bin/python

"""
This program manages cmsRun processes. It reads run information
from *.ini configuration files and starts cmsRun with proper
parameters.

author: Heiner Tholen
"""

import signal
import sys
import os
import getopt
from PyQt4 import QtCore
import MyPackage.TtGammaAnalysis.MyUtility as util
from MyPackage.TtGammaAnalysis.CmsRunController import CmsRunController
from MyPackage.TtGammaAnalysis.CmsRunMonitor import CmsRunMonitor
from MyPackage.TtGammaAnalysis.CmsRunProcess import CmsRunProcess
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

    letters  = 'c:s:'
    opts, extraparams = getopt.getopt(sys.argv[1:], letters)

    # instantiations for both, single tool and normal run
    qset = QtCore.QSettings(util.get_ini_file(),1)
    crp = CmsRunCutflowParser(qset)
    crh = CmsRunHistoStacker(qset)

    # single tools only
    for opt, value in opts:
        #if opt == "-c":
             #cutflow parser stuff

        if opt == "-s":
            crh.stack_it_all(value)


    if len(opts):
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
    main()
    
