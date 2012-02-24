__author__ = 'Heiner Tholen'

import os
import MyPackage.TtGammaAnalysis.MyUtility as util
import MyPackage.TtGammaAnalysis.CmsRunKoolStyle as style
from MyPackage.TtGammaAnalysis.CRPostProcessor import CmsRunPostProcTool
from ROOT import TH1D, TFile, TDirectory

class CmsRunCutflowParser(CmsRunPostProcTool):
    """
    Does cutflow parsing from cmsRun logfiles.
    Searches for keys 'parsePaths' and 'parseModules' in section of a cfg_file
    in qsettings-object. Both keys should contain corresponding path- and
    modulenames.
    """


    def __init__(self, qsetting):
        super(CmsRunCutflowParser, self).__init__()
        self.qsetting                       = qsetting
        self.write_cutflow_to_qsetting      = False
        self.write_cutflow_to_histo_files   = True

        # see if cutflow parsing can be bypassed
        parse_paths = qsetting.value("cutflowParsePaths", "None").toString()
        if str(parse_paths) == "None":
            self.tool_enabled = False


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


    def add_qsettings_group(self, line):
        """
        Begins new group for path in qsetting.
        """

        if not self.write_cutflow_to_qsetting:
            return

        qset = self.qsetting
        tokens = line.split()
        qset.beginGroup(tokens[-1])
        qset.setValue("Visited", tokens[3])
        qset.setValue("Passed", tokens[4])
        qset.setValue("Failed", tokens[5])
        qset.endGroup()


    def begin_cutflow_histo(self, line):
        """
        Books ROOT histogram for filling cutflow.
        """

        if not self.write_cutflow_to_histo_files:
            return

        tokens = line.split()
        self.cutflow_histo = TH1D(
            "cutflow_" + tokens[-1],
            ";cutflow step;number of passed events",
            3, 0, 3
        )
        self.cutflow_histo.SetBit(TH1D.kCanRebin);
        self.cutflow_histo.SetStats(0);


    def fill_cutflow_histo(self, line):
        """
        Fills cutflow values into histogram.
        """

        if not self.cutflow_histo:
            return

        tokens = line.split()
        pretty_name = style.get_pretty_name(tokens[-1])
        self.cutflow_histo.Fill(pretty_name, float(tokens[4]))


    def end_cutflow_histo(self):
        """
        Saves cutflow histo
        """

        if not self.cutflow_histo:
            return

        file = TFile.Open(self.process.service_file_name, "UPDATE")
        file_dir = file.mkdir("cutflow")
        file_dir.cd()
        self.cutflow_histo.Write()
        file.Close()
        del self.cutflow_histo


    def write_confirmation(self, summary_string):
        """
        Puts summary_string to process info file.
        """

        file = open(self.process.info_file_name, "a")
        file.write("Cutflow :" + summary_string + "\n")
        file.close()


    def parse_cutflow(self, abbrev):
        """
        Parses Message Logger output in cmsRun logfile.
        Writes cutflow into qsettings.
        qsetting should be at base level.
        abbrev is the abbrev in qsetting.
        """
        qset = self.qsetting

        # get lists (QStringList)
        parse_paths = qset.value(\
            "cutflowParsePaths", "None").toStringList()
        parse_modules = qset.value(\
            "cutflowParseModules", "None").toStringList()

        # convert to pythonic lists
        parse_paths_list = [str(l) for l in parse_paths]
        parse_modules_list = [str(l) for l in parse_modules]

        if parse_paths_list == ["None"]:
            return

        self.message.emit(\
            self, "INFO parsing paths  : " + str(parse_paths_list))
        self.message.emit(\
            self, "INFO parsing modules: " + str(parse_modules_list))

        # read trigger report from logfile
        if not self.read_trigger_report(abbrev):
            self.message.emit(
                self,
                "ERROR no logfile found for "
                + self.process.name
            )
            return
        
        if not len(self.trigger_report):
           self.message.emit(
               self,
               "ERROR trigger report empty for "
               + self.process.name
           )
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

                # add path itself to qset, book histogram
                self.add_qsettings_group(path_line)
                self.begin_cutflow_histo(path_line)

                qset.beginGroup(tokens[-1]) # path
                path_header = ("TrigReport ---------- Modules in Path: "
                               + tokens[-1]
                               + " ------------")
                path_modules = self.get_block(path_header)

                for module_line in path_modules:
                    tokens_mod = module_line.split()
                    if (parse_modules_list == ["All"]
                        or parse_modules.contains(tokens_mod[-1])):
                
                        # add modules in path
                        self.add_qsettings_group(module_line)
                        self.fill_cutflow_histo(module_line)

                qset.endGroup() #tokens[-1] (path)
                self.end_cutflow_histo()

        qset.endGroup() # "cutflow"
        qset.endGroup() # abbrev

        self.write_confirmation("OK")
        

    def sync_qsetting(self):
        """
        Writes out cutflow data to qsettings file.
        """

        if self.write_cutflow_to_qsetting:
            self.qsetting.sync()


    def start(self, process):
        """
        Overload  of parse_cutflow for process objects.
        """

        # all processes are finished
        if type(process) == list:
            self.sync_qsetting()
            return

        # only when really running
        if process.reused_old_data:
            return

        self.started.emit(self)

        self.process = process
        self.parse_cutflow(process.name)
        del self.process

        self.finished.emit(self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()