__author__ = 'Heiner Tholen'

import os
import MyPackage.TtGammaAnalysis.MyUtility as util
import MyPackage.TtGammaAnalysis.CmsRunKoolStyle as root_style
from ROOT import TFile, TDirectory, TKey, TH1, THStack, TCanvas
from PyQt4 import QtCore

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

class CmsRunHistoStacker(QtCore.QObject):
    """
    Stacks Histograms produced in cmsRun and stored with TFileService.
    Please checkout run_full_procedure(), from there everything is started.
    If you're a pedestrian, this is the method to call.
    Further on, have a look at __init__(), where all important lists are
    defined.

    TODO: simplify by using one HistoStacker for only one name, not for all.

    >>> util.DIR_FILESERVICE = "test/res"
    >>> qset = QtCore.QSettings("test/res/photonSelection.ini",1)
    >>> crhs = CmsRunHistoStacker(qset)
    >>> crhs.stack_it_all("photonSelection")
    """

    # signals
    message = QtCore.pyqtSignal(str)

    # errors
    class ParseError(Exception): pass
    class InputNotReadyError(Exception): pass

    def __init__(self, qsetting, histo_name = ""):
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
        # TODO: rename 'abbrev' to 'dataset_name'


    def load_histograms(self, histo_stackers):
        """
        Loads histograms from FileService files.

        >>> util.DIR_FILESERVICE = "test/res"
        >>> qset = QtCore.QSettings(util.DIR_FILESERVICE + "/tmp.ini",1)
        >>> qset.setValue("stackedHistos",
        ...               QtCore.QStringList(["DeltaR_jet", "DeltaR_muon"]))
        >>> crhs = CmsRunHistoStacker(qset)
        >>> crhs.load_histograms()
        >>> len(crhs.root_file_names) > 0
        True
        >>> crhs.all_histo_names
        ['DeltaR_jet', 'DeltaR_muon']
        >>> len(crhs.histograms) > 0
        True
        >>> crhs.histograms[0].name
        'DeltaR_jet'
        >>> crhs.histograms[0].abbrev
        'WJets'
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

        output_dir = "collected"
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

        >>> util.DIR_FILESERVICE = "test/res"
        >>> qset = QtCore.QSettings("test/res/photonSelection.ini",1)
        >>> qset.beginGroup("photonSelection")
        >>> crhs = CmsRunHistoStacker(qset)
        >>> crhs.load_histograms()
        >>> crhs.collect_histogram_info()
        >>> crhs.all_legend_entries
        ['WZ + Jets', 'Signal']
        >>> histo = crhs.histograms[0]
        >>> int(histo.lumi)    # int() to avoid double precision errors
        2591
        >>> histo.legend
        'WZ + Jets'
        >>> histo.is_data
        False
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

        >>> util.DIR_FILESERVICE = "test/res"
        >>> qset = QtCore.QSettings("test/res/photonSelection.ini",1)
        >>> qset.beginGroup("photonSelection")
        >>> crhs = CmsRunHistoStacker(qset)
        >>> crhs.load_histograms()
        >>> crhs.collect_histogram_info()
        >>> crhs.merge_histograms()
        >>> len(crhs.histograms)
        9
        >>> len (crhs.merged_histos)
        6
        >>> histo = crhs.merged_histos[0]
        >>> histo is None
        False
        >>> histo.abbrev
        'merged'
        >>> histo.lumi
        2
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

        >>> util.DIR_FILESERVICE = "test/res"
        >>> qset = QtCore.QSettings("test/res/photonSelection.ini",1)
        >>> qset.beginGroup("photonSelection")
        >>> crhs = CmsRunHistoStacker(qset)
        >>> crhs.load_histograms()
        >>> crhs.collect_histogram_info()
        >>> crhs.merge_histograms()
        >>> crhs.make_stacks()
        >>> len(crhs.stacks)
        3
        >>> stack = crhs.stacks[0]
        >>> stack is None
        False
        >>> stack.lumi
        3
        >>> stack.name
        'DeltaR_jet'
        """

        if not len(self.histograms_merged):
            raise self.InputListEmptyError,\
            "self.merged_histos is empty!"

        for is_data in [True, False]:

            stack_wrap = HistogramWrapper(THStack(self.histo_name, ""))
            stack_wrap.is_data = is_data
            stack_wrap.lumi = 0.
            for legend in root_style.get_stacking_order():

                histo_wrap = self.histos_merged_dict[legend]

                # filter by data or not
                if not is_data == histo_wrap.is_data:
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
        Saves finished stacks.
        """

        output_dir = "stacked"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        filename = output_dir + "/" + self.histo_name + "stacked.root"
        file = TFile(filename, "RECREATE")
        file.cd()
        for stack_wrap in self.stacks:
            stack_wrap.histo.Write()
        file.Close()


    def draw_full_plot(self):
        """
        Puts everything together. Data and MC are plotted and saved.
        """

        output_dir = "stacked"
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

        # draw higher first (assuming it's data)
        if histo_data:
            histo_mc.histo.Draw()
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


    def run_full_procedure(self):
        """
        Run all steps to produce and save stacked histograms.
        """

        all_histo_names = self.qsetting.value("stackedHistos").toStringList()

        # create histostackers
        stackers = []
        for name in all_histo_names:
            stackers.append(CmsRunHistoStacker(self.qsetting, str(name)))

        # load all histograms
        self.load_histograms(stackers)

        for s in stackers:
            s.run_procedure()


    def stack_it_all(self, cfg_abbrev):
        """
        Switches self.qsettings to cfg_abbrev, then runs full procedure.
        """

        self.qsetting.beginGroup(cfg_abbrev)
        self.run_full_procedure()
        self.qsetting.endGroup()


if __name__ == '__main__':
    import doctest
    doctest.testmod()