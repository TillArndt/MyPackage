
import MyPackage.TtGammaAnalysis.MyUtility as util
from ROOT import TFile, TDirectory, TKey, TH1, THStack
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
    """

    # signals
    message = QtCore.pyqtSignal(str)

    # errors
    class ParseError(Exception): pass

    def __init__(self, qsetting):
        super(CmsRunHistoStacker, self).__init__()
        self.qsetting           = qsetting
        self.root_file_names    = []
        self.all_histo_names    = []
        self.all_legend_entries = []
        self.histograms         = []
        self.merged_histos      = []


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

            if self.all_legend_entries.count(legend_entry) == 0:
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
        >>> len(crhs.merged_histos)
        6
        >>> #histo = crhs.merged_histos[0]
        >>> #histo.abbrev
        'merged'
        """

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
                            merged_hist.abbrev = "merged"

                        else:
                            merged_hist.histo.Add(histo_wrap.histo)
                            merged_hist.lumi += 1

                    if merged_hist != None:
                        self.merged_histos.append(merged_hist)


    def make_merged_pretty(self):
        """
        Gives the merged histograms a nice finish. Applies color, set's the
        Title appropriatly. That stuff...
        """

        for index, histoWrap in enumerate(self.merged_histos):

            # This is arbitrary. Kool Kolors later...
            histoWrap.histo.SetFillColor(3 + index)
            histoWrap.histo.SetTitle(histoWrap.legend)


    def make_stacks(self):
        """
        Makes one stacked histogram, weighted by luminosity.
        Takes histograms from self.merged_histos.
        Appends stack to self.stacks.
        """

        for histo_name in self.all_histo_names:

            for is_data in [True, False]:

                stack = THStack()
                for legend_entry in self.all_legend_entries:

                    for histo in self.merged_histos:
                        pass

                        stack.Add(histo)


    def make_all_stacks(self):
        """
        Makes all stacked histograms.

        >>> util.DIR_FILESERVICE = "test/res"
        >>> qset = QtCore.QSettings("test/res/tmp.ini")
        >>> qset.setValue("stackedHistos",
        ...               QtCore.QStringList(["DeltaR_jet", "DeltaR_muon"]))
        >>> crhs = CmsRunHistoStacker(qset)
        >>> #crhs.make_all_stacks()
        """

        self.load_histograms()
        self.collect_histogram_info()
        self.merge_histograms()
        self.make_merged_pretty()
        self.make_stack_by_lumi()

        self.stacks = dict()
        for name in self.histograms:
            self.make_stack(name)




if __name__ == '__main__':
    import doctest
    doctest.testmod()