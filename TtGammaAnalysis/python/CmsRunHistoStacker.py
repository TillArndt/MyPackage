__author__ = 'Heiner Tholen'

import os
import MyPackage.TtGammaAnalysis.MyUtility as util
import MyPackage.TtGammaAnalysis.CmsRunKoolStyle as root_style
from ROOT import TFile, TDirectory, TKey, TH1, THStack, TCanvas
from MyPackage.TtGammaAnalysis.CmsRunPostProcessor import CmsRunPostProcTool

# Histogram wrapper
class HistogramWrapper:
    def __init__(self, histo, abbrev = ""):
        self.histo      = histo
        self.is_data    = False
        self.name       = histo.GetName()
        self.abbrev     = abbrev
        self.lumi       = -1
        self.legend     = ""

    def __str__(self):
        return ("_____________HistogramWrapper____________"
            + "\nis data:" + str(self.is_data)
            + "\nname   :" + self.name
            + "\nabbrev :" + self.abbrev
            + "\nlumi   :" + str(self.lumi)
            + "\nlegend :" + str(self.legend)
        )

class CmsRunHistoStacker(CmsRunPostProcTool):
    """
    Stacks Histograms produced in cmsRun and stored with TFileService.
    Please checkout run_full_procedure(), from there everything is started.
    If you're a pedestrian, this is the method to call.
    Further on, have a look at __init__(), where all important lists are
    defined.
    """

    # errors
    class ParseError(Exception): pass
    class InputNotReadyError(Exception): pass

    def __init__(self, qsetting, histo_name = ""):
        """
        Constructor. Reminder: One HistoStacker instance is only responsible
        for one tpye of histogram (according to histo_name)
        """

        super(CmsRunHistoStacker, self).__init__()
        self.qsetting             = qsetting
        self.histo_name           = histo_name
        self.all_legend_entries   = []
        self.histograms           = []
        self.histograms_merged    = []
        self.histos_merged_dict   = dict()
        self.stacks               = []
        # TODO: kill these definitions,
        # create lists in functions,
        # check for needed lists in functions

        # see if histo-stacking can be bypassed
        stacked_histos = qsetting.value("stackedHistos", "None").toString()
        if str(stacked_histos) == "None":
            self.tool_enabled = False


    def load_histograms(self, histo_stackers):
        """
        Loads histograms from FileService files.
        """

        # get filenames
        import os
        import fnmatch
        root_file_names = []
        for root, dirs, files in os.walk(util.DIR_FILESERVICE):
            for filename in fnmatch.filter(files, '*.root'):
                root_file_names.append(os.path.join(root, filename))

        # walk over files
        for filename in root_file_names:
            file = TFile.Open(filename)
            abbrev = os.path.basename(filename)[0:-5]

            #walk over folders in file
            for folder_key in file.GetListOfKeys():

                # only Directories contain the histograms
                if not folder_key.IsFolder():
                    continue

                # walk over histograms
                for histo_key in folder_key.ReadObj().GetListOfKeys():

                    # loop over stackers and add histo to the right one
                    for stacker in histo_stackers:

                        if not stacker.histo_name == histo_key.GetName():
                            continue

                        histo = histo_key.ReadObj()
                        wrapper = HistogramWrapper(histo, abbrev)
                        stacker.histograms.append(wrapper)


    def all_to_root_file(self):
        """
        Collects all histograms of same name into root files with the name of
        the histograms. Stores into "collected"
        """

        output_dir = util.DIR_PLOTS + "/collected"
        if not os.path.exists(util.DIR_PLOTS):
            os.mkdir(util.DIR_PLOTS)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        filename = output_dir + "/" + self.histo_name + ".root"
        file = TFile(filename, "RECREATE")
        file.cd()
        for histo_wrap in self.histograms:
            histo_wrap.histo.Write(histo_wrap.abbrev)
        file.Close()


    def collect_histogram_info(self):
        """
        Takes infos for qsettings-object and puts to histograms in
        self.histograms.
        """

        if not len(self.histograms):
            raise self.InputNotReadyError, \
            "self.histograms is empty!"

        qset = self.qsetting
        for histo in self.histograms[:]:
            qset.beginGroup(histo.abbrev)

            # check if dataset is disabled
            if str(qset.value("enable").toString()) == "False":
                self.message.emit(
                    self,
                    "INFO: (HistoStacker) Dataset " + histo.abbrev
                    + "is disabled. Skipping!"
                )
                self.histograms.remove(histo)
                continue

            # no lumi, no histogram
            if qset.contains("lumi"):
                histo.lumi, parse_ok = qset.value("lumi", 0.).toDouble()
                if histo.lumi == 0. or not parse_ok:
                    self.histograms.remove(histo)
                    raise self.ParseError, \
                    "Parsing of lumi value failed for " + histo.abbrev
            else:
                self.message.emit(
                    self,
                    "INFO: (HistoStacker) Dataset " + histo.abbrev
                    + "has no lumi entry. Skipping!"
                )
                self.histograms.remove(histo)
                continue

            # data or not?
            histo.is_data = qset.value("isData", False).toBool()

            # legend entry (if not given, takes histo.abbrev)
            legend_entry = str(qset.value("legend", histo.abbrev).toString())
            histo.legend = legend_entry

            # add legend entry only once
            if not self.all_legend_entries.count(legend_entry):
                self.all_legend_entries.append(legend_entry)

            qset.endGroup() # histo.abbrev


    def scale_mc_to_lumi(self):
        """
        Scales MC histograms to match data luminosity.
        """

        # calculate data lumi
        lumi_data = 0.
        for histo_wrap in self.histograms:

            if histo_wrap.is_data:
                lumi_data += histo_wrap.lumi

        # Apply to mc
        for histo_wrap in self.histograms:

            if not histo_wrap.is_data:
                scale_factor = lumi_data / histo_wrap.lumi
                histo_wrap.histo.Scale(scale_factor)
                histo_wrap.lumi *= scale_factor


    def merge_histograms(self):
        """
        Merges histograms from self.histograms with same 'name' and 'legend'
        string. Scales by luminosity first. Appends them to self.merged_histos.
        """

        if not len(self.all_legend_entries):
            raise self.InputNotReadyError,\
            "self.all_legend_entries is empty!"

        for legend_entry in self.all_legend_entries:

            for is_data in [True, False]:

                merged_hist = None
                for histo_wrap in self.histograms:

                    # search for same legend entry
                    if not histo_wrap.legend == legend_entry:
                        continue

                    # search for mc / data
                    if not is_data == histo_wrap.is_data:
                        continue

                    # merge (or create to merge later)
                    if not merged_hist:
                        merged_hist = HistogramWrapper(
                            histo_wrap.histo.Clone(),
                            histo_wrap.abbrev
                        )
                        merged_hist.lumi = histo_wrap.lumi
                        merged_hist.legend = legend_entry
                        merged_hist.is_data = histo_wrap.is_data

                    else:
                        merged_hist.histo.Add(histo_wrap.histo)
                        merged_hist.abbrev = "merged"

                        # add data lumi, but not mc (different processes)
                        if is_data:
                            merged_hist.lumi += histo_wrap.lumi

                if merged_hist is not None:
                    self.histograms_merged.append(merged_hist)
                    self.histos_merged_dict[merged_hist.legend] = merged_hist


    def make_merged_pretty(self):
        """
        Gives the merged histograms a nice finish. Applies color, set's the
        Title appropriatly. That stuff...
        """

        for histo_wrap in self.histograms_merged:

            histo = histo_wrap.histo
            if histo_wrap.is_data:
                histo.SetMarkerStyle(8)
                histo.SetMarkerSize(1.2)
                histo.SetMarkerColor(1)
            else:
                histo.SetMarkerSize(0.5)
                histo.SetFillColor(
                    root_style.get_fill_color(histo_wrap.legend)
                )

            histo.SetTitle(histo_wrap.legend)


    def make_stacks(self):
        """
        Makes stacked histograms from merged histograms.
        Takes histograms from self.merged_histos.
        Appends stack to self.stacks.
        """

        if not len(self.histograms_merged):
            raise self.InputListEmptyError,\
            "self.merged_histos is empty!"

        for is_data in [True, False]:

            stack_wrap = HistogramWrapper(THStack(self.histo_name, ""))
            stack_wrap.is_data = is_data
            stack_wrap.lumi = 0.
            order = root_style.get_stacking_order()
            for legend in order:

                if not self.histos_merged_dict.has_key(legend):
                    self.message.emit(
                        self,
                        "WARNING no merged histos for legendentry '"
                        + legend
                        + "', histoname '"
                        + self.histo_name
                        + "'"
                    )
                    continue

                histo_wrap = self.histos_merged_dict[legend]

                # distinguinsh data / mc
                if not histo_wrap.is_data == is_data:
                    continue

                stack_wrap.histo.Add(histo_wrap.histo)
                stack_wrap.x_axis = histo_wrap.histo.GetXaxis().GetTitle()
                stack_wrap.y_axis = histo_wrap.histo.GetYaxis().GetTitle()
                if is_data:
                    stack_wrap.lumi += histo_wrap.lumi
                elif stack_wrap.lumi == 0.:
                    stack_wrap.lumi = histo_wrap.lumi

            if stack_wrap.histo :
                self.stacks.append(stack_wrap)


    def save_stacks(self):
        """
        Saves finished stacks. No canvases...
        """

        output_dir = util.DIR_PLOTS + "/stacks"
        if not os.path.exists(util.DIR_PLOTS):
            os.mkdir(util.DIR_PLOTS)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        filename = output_dir + "/" + self.histo_name + "_stacked.root"
        file = TFile(filename, "RECREATE")
        file.cd()
        for stack_wrap in self.stacks:
            stack_wrap.histo.Write()
        file.Close()


    def draw_full_plot(self):
        """
        Puts everything together. Data and MC are plotted and saved.
        """

        output_dir = util.DIR_PLOTS + "/final"
        if not os.path.exists(util.DIR_PLOTS):
            os.mkdir(util.DIR_PLOTS)
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        canvas = TCanvas(self.histo_name, self.histo_name)
        canvas.SetLogy(True)
        histo_data = None
        histo_mc   = None
        for stack_wrap in self.stacks:

            if stack_wrap.is_data:
                histo_data = stack_wrap
            else:
                histo_mc   = stack_wrap

            #print "Name :", self.histo_name, "Data: ", stack_wrap.is_data, "Lumi: ", stack_wrap.lumi

        # draw mc first, then data
        if histo_data:
            histo_mc.histo.Draw()
            histo_mc.histo.GetXaxis().SetLabelSize(0.052)
            histo_mc.histo.GetXaxis().SetTitle(histo_data.x_axis)
            histo_mc.histo.GetYaxis().SetTitle(histo_data.y_axis)

            if histo_mc:
                histo_data.histo.Draw("sameE1")

        # build legend
        canvas.BuildLegend(0.7, 0.59, 0.92, 0.88)

        # save canvas
        filename = output_dir + "/" + self.histo_name
        canvas.SaveAs(filename + ".root")
        #canvas.SaveAs(filename + ".png")
        #canvas.SaveAs(filename + ".pdf")


    def run_procedure(self):
        """
        Runs procedure for own histo_name. Does not load histograms itself.
        """

        if not len(self.histograms):
            self.message.emit(
                self,
                "WARNING: No histograms to stack for "
                + self.name
            )
            return

        self.all_to_root_file()
        self.collect_histogram_info()
        self.scale_mc_to_lumi()
        self.merge_histograms()
        self.make_merged_pretty()
        self.make_stacks()
        self.save_stacks()
        self.draw_full_plot()


    def start(self, process):
        """
        Run all steps to produce and save stacked histograms.
        """

        # only when all finished
        if type(process) != list:
            return

        self.started.emit(self)
        all_histo_names = self.qsetting.value("stackedHistos").toStringList()

        # create histostackers
        stackers = []
        for name in all_histo_names:
            stakker = CmsRunHistoStacker(self.qsetting, str(name))
            stakker.message.connect(self.message)
            stackers.append(stakker)

        # load all histograms
        self.load_histograms(stackers)

        for s in stackers:
            s.run_procedure()

        self.finished.emit(self)


if __name__ == '__main__':
    import doctest
    doctest.testmod()