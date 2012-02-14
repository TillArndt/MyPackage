__author__ = 'Heiner Tholen'

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

    def __init__(self, qsetting):
        super(CmsRunHistoStacker, self).__init__()
        self.qsetting           = qsetting
        self.root_file_names    = []
        self.all_histo_names    = []
        self.all_legend_entries = []
        self.histograms         = []
        self.merged_histos      = []
        self.stacks             = []


    def load_histograms(self):
        """
        Loads histograms from FileService files.
        Histogram tree is sorted this way in self.histograms:
            {'histoname': {'basename (of file)': TH1 reference}}

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
        for root, dirs, files in os.walk(util.DIR_FILESERVICE):
            for filename in fnmatch.filter(files, '*.root'):
                self.root_file_names.append(os.path.join(root, filename))

        # setup self.histograms with names
        all_histo_names = self.qsetting.value("stackedHistos", "None").toStringList()
        self.all_histo_names = [str(h) for h in all_histo_names]

        # walk over files
        for filename in self.root_file_names:
            file = TFile.Open(filename)
            abbrev = os.path.basename(filename)[0:-5]

            #walk over folders in file
            for folder_key in file.GetListOfKeys():

                # only Directories contain the histograms
                if not folder_key.IsFolder():
                    continue

                # walk over histograms
                for histo_key in folder_key.ReadObj().GetListOfKeys():

                    histname = histo_key.GetName()

                    # only stacked ones are treated
                    if not all_histo_names.contains(histname):
                        continue

                    histo = histo_key.ReadObj()
                    wrapper = HistogramWrapper(histo, abbrev)
                    self.histograms.append(wrapper)


    def collect_histogram_info(self):
        """
        Takes infos for qsettings-object and puts to histograms in self.histograms.

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

            # no lumi, no histogram
            if qset.contains("lumi"):
                histo.lumi, parse_ok = qset.value("lumi", 0.).toDouble()
                if histo.lumi == 0. or not parse_ok:
                    self.histograms.remove(histo)
                    raise self.ParseError, \
                    "Parsing of lumi value failed for " + histo.abbrev
            else:
                self.histograms.remove(histo)
                continue

            # data or not?
            histo.is_data = qset.value("isData", False).toBool()

            # legend entry (if not given, takes histo.abbrev)
            legend_entry = str(qset.value("legend", histo.abbrev).toString())
            histo.legend = legend_entry

            if not self.all_legend_entries.count(legend_entry):
                self.all_legend_entries.append(legend_entry)

            qset.endGroup() # histo.abbrev


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

        for histo_name in self.all_histo_names:

            for legend_entry in self.all_legend_entries:

                for is_data in [True, False]:

                    merged_hist = None
                    for histo_wrap in self.histograms:


                        # search for same legend entry
                        if not histo_wrap.name == histo_name:
                            continue

                        # search for same legend entry
                        if not histo_wrap.legend == legend_entry:
                            continue

                        # search for mc / data
                        if not is_data == histo_wrap.is_data:
                            continue

                        # scale by lumi first
                        histo_wrap.histo.Scale(1/histo_wrap.lumi)

                        # merge
                        if not merged_hist:
                            merged_hist = HistogramWrapper(
                                histo_wrap.histo.Clone(),
                                histo_wrap.abbrev
                            )
                            merged_hist.lumi = 1
                            merged_hist.legend = legend_entry

                        else:
                            merged_hist.histo.Add(histo_wrap.histo)
                            merged_hist.lumi += 1
                            merged_hist.abbrev = "merged"

                    if merged_hist is not None:
                        self.merged_histos.append(merged_hist)


    def make_merged_pretty(self):
        """
        Gives the merged histograms a nice finish. Applies color, set's the
        Title appropriatly. That stuff...
        """

        for histoWrap in self.merged_histos:

            histo = histoWrap.histo
            if histoWrap.is_data:
                histo.SetMarkerSize(1.2)
                histo.SetMarkerColor(1)
            else:
                histo.SetFillColor(
                    root_style.get_fill_color(histoWrap.legend)
                )

            histo.SetTitle(histoWrap.legend)


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

        if not len(self.merged_histos):
            raise self.InputListEmptyError,\
            "self.merged_histos is empty!"

        for histo_name in self.all_histo_names:

            for is_data in [True, False]:

                stack_wrap = HistogramWrapper(
                    THStack(histo_name, histo_name)
                )
                stack_wrap.is_data = is_data
                stack_wrap.lumi = 0
                for histo_wrap in self.merged_histos:

                    # filter by name
                    if not histo_name == histo_wrap.name:
                        continue

                    # filter by data or not
                    if not is_data == histo_wrap.is_data:
                        continue

                    stack_wrap.histo.Add(histo_wrap.histo)
                    stack_wrap.lumi += histo_wrap.lumi

                if stack_wrap.lumi > 0:
                    self.stacks.append(stack_wrap)


    def save_stacks(self):
        """
        Saves finished stacks.
        """

        file = TFile(util.DIR_FILESERVICE + "/stackedHistos.root", "RECREATE")
        file.cd()
        for stack_wrap in self.stacks:
            stack_wrap.histo.Write()
        file.Close()


    def draw_full_plot(self):
        """
        Puts everything together. Data and MC are plotted and saved.
        """

        for histo_name in self.all_histo_names:

            canvas = TCanvas(histo_name, histo_name)
            hist_data = None
            hist_mc   = None
            for stack_wrap in self.stacks:

                # filter by name
                if not histo_name == stack_wrap.name:
                    continue

                if stack_wrap.is_data:
                    hist_data = stack_wrap
                else:
                    hist_mc   = stack_wrap

            # draw higher first (assuming it's data)
            if hist_data:
                hist_data.histo.Draw("E1")
                if hist_mc:
                    hist_mc.histo.Draw("same")
            filename = util.DIR_FILESERVICE + "/" + histo_name
            canvas.SaveAs(filename + ".root")
            canvas.SaveAs(filename + ".png")


    def run_full_procedure(self):
        """
        Run all steps to produce and save stacked histograms.
        """

        self.load_histograms()
        self.collect_histogram_info()
        self.merge_histograms()
        self.make_merged_pretty()
        self.make_stacks()
        self.save_stacks()
        self.draw_full_plot()


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