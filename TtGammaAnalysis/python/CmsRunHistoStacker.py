
import MyPackage.TtGammaAnalysis.MyUtility as util
from ROOT import TFile, TDirectory, TKey, TH1, THStack
from PyQt4 import QtCore

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
        self.qsetting = qsetting


    def load_histograms(self):
        """
        Loads histograms from FileService files.
        Histogram tree is sorted this way in self.histograms:
            {'histoname': {'basename (of file)': TH1 reference}}

        >>> util.DIR_FILESERVICE = "test/res"
        >>> qset = QtCore.QSettings("test/res/tmp.ini")
        >>> qset.setValue("stackedHistos",
        ...               QtCore.QStringList(["DeltaR_jet", "DeltaR_muon"]))
        >>> crhs = CmsRunHistoStacker(qset)
        >>> crhs.load_histograms()
        >>> crhs.root_file_names
        ['test/res/ttgamma_whizard.root', 'test/res/WJets.root']
        >>> crhs.histograms
        {'DeltaR_muon': {'ttgamma_whizard': None, 'WJets': None}, 'DeltaR_jet': {'ttgamma_whizard': None, 'WJets': None}}
        """

        # get filenames
        self.root_file_names = []
        import os
        import fnmatch
        for root, dirs, files in os.walk(util.DIR_FILESERVICE):
            for filename in fnmatch.filter(files, '*.root'):
                self.root_file_names.append(os.path.join(root, filename))

        # setup self.histograms with names
        self.histograms = []
        list_of_stacked_histos = self.qsetting.value("stackedHistos", "").toStringList()

        # walk over files
        for filename in self.root_file_names:
            file = TFile(filename)
            abbrev = os.path.basename(filename)[0:-5]

            #walk over folders in file
            for folder_key in file.GetListOfKeys():

                # only Directories contain the histograms
                if not folder_key.IsFolder():
                    continue

                # walk over histograms
                for histo_key in folder_key.ReadObj().GetListOfKeys():

                    histname = histo_key.GetName()
                    if not list_of_stacked_histos.contains(histname):
                        continue

                    histo = histo_key.ReadObj()
                    histo.name = histname
                    histo.abbrev = abbrev
                    self.histograms.append(histo)


    def add_histogram_info(self):
        """
        Takes infos for qsettings-object and puts to histograms.
        """

        qset = self.qsetting
        self.all_legend_entries = []
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

            # legend entry
            legend_entry = str(qset.value("legend", "").toString())
            histo.legend = legend_entry
            self.all_legend_entries.append(legend_entry)

            qset.endGroup() # histo.abbrev


    def sort_histograms(self):
        """
        Sorts histograms by 'legend' key in qsettings-object.
        """

        self.sorted_hists = dict()
        for name in self.histograms:

            groups = dict()
            for abbrev in self.histograms[name]:

                # no legend name, no histogram!
                if not self.qsetting.contains(abbrev + "/legend"):
                    continue

                legend_name = str(
                    self.qsetting.value(abbrev + "/legend").toString()
                )

                if not groups.has_key(legend_name):
                    groups[legend_name] = dict()

                histo = self.histograms[name][abbrev]
                groups[legend_name][abbrev] = histo

            self.sorted_hists[name] = groups


    def merge_histograms(self):
        """
        Merges histograms with same 'legend' key.
        Scales by luminosity first.
        """

        self.merged_histos = []
        for histo in self.histograms:

            merged_histos = dict()
            for legend_name in self.sorted_hists[name]:

                same_legend_histos = self.sorted_hists[name][legend_name]

                # get histo
                abbrev, histo = same_legend_histos.popitem()

                # scale
                lumi, parse_ok = self.qsetting.value(abbrev + "/lumi")
                if not parse_ok:
                    raise self.ParseError, \
                    "Parsing of lumi value failed for " + abbrev
                histo.Scale(1 / lumi)

                # merge
                merged_hist = histo.Clone()

                # now same procedure for all others
                while (len(same_legend_histos) > 0):
                    abbrev, histo = same_legend_histos.popitem()
                    lumi, parse_ok = self.qsetting.value(abbrev + "/lumi")
                    if not parse_ok:
                        raise self.ParseError, \
                        "Parsing of lumi value failed for " + abbrev
                    histo.Scale(1 / lumi)
                    merged_hist.Add(histo)

                merged_histos[legend_name] = merged_hist

            self.merged_histos[name] = merged_histos


    def make_stack_by_lumi(self, name):
        """
        Makes one stacked histogram, weighted by luminosity.
        Takes histograms from self.merged_histos[name].
        Appends stack to self.stacks.
        """

        stack = THStack(name, name)
        for index, legend_name in enumerate(self.merged_histos[name]):

            histo = self.merged_histos[name][legend_name]
            histo.SetFillColor(3 + index)
            histo.SetTitle(legend_name)
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
        self.sort_histograms()
        self.merge_histograms()

        self.stacks = dict()
        for name in self.histograms:
            self.make_stack(name)




if __name__ == '__main__':
    import doctest
    doctest.testmod()