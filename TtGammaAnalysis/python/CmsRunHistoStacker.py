
import MyPackage.TtGammaAnalysis.MyUtility as util
from ROOT import TFile, TDirectory, TKey, TH1
from PyQt4 import QtCore

class CmsRunHistoStacker(QtCore.QObject):
    """
    Stacks Histograms produced in cmsRun and stored with TFileService.
    """

    # signals
    message = QtCore.pyqtSignal(str)

    def __init__(self, qsetting):
        super(CmsRunHistoStacker, self).__init__()
        self.qsetting = qsetting

    def load_histograms(self):
        """
        Loads histograms from FileService files.
        Histogram tree is sorted this way in self.histograms:
            {'histoname': {'basename (of file) + POSTFIX': TH1 reference}}
        where the folder_key in root files are named like this:
            analyzer_SOMENAME_POSTFIX

        >>> util.DIR_FILESERVICE = "test/res"
        WARNING: constant 'DIR_FILESERVICE' is changed from 'outputFileService' to 'test/res'!
        >>> qset = QtCore.QSettings("test/res/tmp.ini")
        >>> qset.setValue("stackedHistos",
        ...               QtCore.QStringList(["DeltaR_jet", "DeltaR_muon"]))
        >>> crhs = CmsRunHistoStacker()
        >>> crhs.load_histograms(qset)
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
        self.histograms = dict()
        list_of_stacked_histos = self.qsetting.value("stackedHistos", "").toStringList()
        for h in list_of_stacked_histos:
            self.histograms[str(h)] = dict()

        # walk over files
        for filename in self.root_file_names:
            file = TFile(filename)
            basename = os.path.basename(filename)[0:-5]

            #walk over folders in file
            for folder_key in file.GetListOfKeys():

                # only Directories contain the histograms
                if not folder_key.IsFolder():
                    continue

                # make postfix from 'analyzer_SOMENAME_POSTFIX'
                analyzer_name_tokens = folder_key.GetName().split("_")
                postFix = ""
                if len(analyzer_name_tokens) > 2:
                    postFix = "_" + analyzer_name_tokens[2]

                # walk over histograms
                for histo in folder_key.ReadObj().GetListOfKeys():

                    if self.histograms.has_key(histo.GetName()):
                        self.histograms[histo.GetName()][basename + postFix] = histo.ReadObj()


    def stack_histograms(self):
        """
        """

        self.load_histograms()


if __name__ == '__main__':
    import doctest
    doctest.testmod()