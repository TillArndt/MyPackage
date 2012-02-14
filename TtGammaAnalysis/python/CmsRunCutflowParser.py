__author__ = 'Heiner Tholen'

import os
import MyPackage.TtGammaAnalysis.MyUtility as util
from MyPackage.TtGammaAnalysis.CmsRunProcess import CmsRunProcess
from PyQt4 import QtCore

class CmsRunCutflowParser(QtCore.QObject):
    """
    Does cutflow parsing from cmsRun logfiles.
    Searches for keys 'parsePaths' and 'parseModules' in section of a cfg_file
    in qsettings-object. Both keys should contain corresponding path- and
    modulenames.
    """

    # signals
    trigger_report_empty = QtCore.pyqtSignal(CmsRunProcess)
    no_logfile           = QtCore.pyqtSignal(CmsRunProcess)
    message              = QtCore.pyqtSignal(str)


    def __init__(self, qsetting):
        super(CmsRunCutflowParser, self).__init__()
        self.qsetting = qsetting


    def read_trigger_report(self, abbrev):
        """
        Reads all lines starting with 'TrigReport' from logfile.
        Stores into self.trigger_report
        """
        
        self.trigger_report = []

        filename = util.DIR_LOGS +"/" + abbrev + ".log"
        if not os.path.exists(filename):
            return False

        file = open(filename, "r")
        for line in file.__iter__():
            if line[0:10] == "TrigReport":
                self.trigger_report.append(line)
        file.close()
        return True


    def get_block(self, starting_line):
        """
        Finds block corresponding to starting_line from self.trigger_report.
        """

        # find starting index
        index_start = 0
        while self.trigger_report[index_start].count(starting_line) == 0:
            index_start += 1
        index_start += 2

        # find last index
        index_end = index_start
        while self.trigger_report[index_end].count("-------") == 0:
            index_end += 1

        return self.trigger_report[index_start:index_end]


    def add_group(self, qsetting, line):
        """
        Begins new group for path in qsetting.

        >>> line = 'TrigReport     1    0       1548        696        852          0 photonsWithTightID'
        >>> from PyQt4 import QtCore          
        >>> qset = QtCore.QSettings('res/tmp.ini',1)
        >>> cp = CmsRunCutflowParser(qset)
        >>> cp.add_group(qset, line)
        >>> for key in qset.allKeys():
        ...     print key
        ... 
        photonsWithTightID/Failed
        photonsWithTightID/Passed
        photonsWithTightID/Visited
        >>> qset.value('photonsWithTightID/Failed').toInt()
        (852, True)
        """
        
        tokens = line.split()
        qsetting.beginGroup(tokens[-1])
        qsetting.setValue("Visited", tokens[3])
        qsetting.setValue("Passed", tokens[4])
        qsetting.setValue("Failed", tokens[5])
        qsetting.endGroup()


    def parse_cutflow(self, abbrev, process = None):
        """
        Parses Message Logger output in cmsRun logfile.
        Writes cutflow into qsettings.
        qsetting should be at base level.
        abbrev is the abbrev in qsetting.
        """
        qset = self.qsetting

        # get lists (QStringList)
        parse_paths = qset.value("parsePaths", "None").toStringList()
        parse_modules = qset.value("parseModules", "None").toStringList()

        # convert to pythonic lists
        parse_paths_list = [str(l) for l in parse_paths]
        parse_modules_list = [str(l) for l in parse_modules]

        self.message.emit("parsing paths  : " + str(parse_paths_list))
        self.message.emit("parsing modules: " + str(parse_modules_list))

        if parse_paths_list == ["None"]:
            return

        # read trigger report from logfile
        if not self.read_trigger_report(abbrev):
            self.no_logfile.emit(process)
            return
        
        if not len(self.trigger_report):
           self.trigger_report_empty.emit(process)
           return
        
        path_summary = self.get_block(
            "TrigReport ---------- Path   Summary -----------"
        )

        qset.beginGroup(abbrev)
        qset.beginGroup("cutflow")
        for path_line in path_summary:
            tokens = path_line.split()
            if (parse_paths_list == ["All"]
                or parse_paths.contains(tokens[-1])):

                # add path itself to qset
                self.add_group(qset, path_line)

                qset.beginGroup(tokens[-1])
                path_header = ("TrigReport ---------- Modules in Path: "
                               + tokens[-1]
                               + " ------------")
                path_modules = self.get_block(path_header)

                for module_line in path_modules:
                    tokens_mod = module_line.split()
                    if (parse_modules_list == ["All"]
                        or parse_modules.contains(tokens_mod[-1])):
                
                        # add modules in path to qset
                        self.add_group(qset, module_line)

                qset.endGroup() #tokens[-1]

        qset.endGroup() # "cutflow"
        qset.endGroup() # abbrev
        

    def parse_cutflow_process(self, process):
        self.qsetting.beginGroup(process.qsetting_base_group)
        self.parse_cutflow(process.name)
        self.qsetting.endGroup()


    def sync_qsetting(self):
        self.qsetting.sync()


if __name__ == '__main__':
    import doctest
    doctest.testmod()