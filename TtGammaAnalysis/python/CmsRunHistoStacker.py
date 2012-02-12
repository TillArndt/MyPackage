
from ROOT import TFile, TDirectory, TKey, TH1

class CmsRunHistoStacker:
    def __init__(self):
        pass

    def load_histograms(self, qsetting):
        """
        Loads histograms from FileService files.
        Histogram tree is sorted this way: [histoname][basename (of file) + POSTFIX]
        Where the folder in root files are named like this: analyzer_SOMENAME_POSTFIX
        """

        # get filenames
        filenames = []
        import os
        import fnmatch
        import MyPackage.TtGammaAnalysis.MyUtility as util
        for root, dirs, files in os.walk(util.DIR_FILESERVICE):
            for filename in fnmatch.filter(files, '*.root'):
                filenames.append(os.path.join(root, filename))

        # setup self.histograms with names
        self.histograms = dict()
        list_of_stacked_histos = qsetting.value("stackedHistos", "").toStringList()
        for h in list_of_stacked_histos:
            self.histograms[str(h)] = dict()

        # walk over files
        for filename in filenames:
            file = TFile(filename)
            basename = os.path.basename(filename)[0:-5]

            #walk over folders in file
            for folder in file.GetListOfKeys():

                # only Directories contain the histograms
                if not folder.IsFolder():
                    continue

                # make postfix from 'analyzer_SOMENAME_POSTFIX'
                analyzer_name_tokens = folder.GetName().split("_")
                postFix = ""
                if len(analyzer_name_tokens) > 2:
                    postFix = "_" + analyzer_name_tokens[2]

                # walk over histograms
                for histo in folder.GetListOfKeys():

                    if self.histograms.has_key(histo.GetName()):
                        self.histograms[histo.GetName][basename + postFix] = histo.ReadObj()

