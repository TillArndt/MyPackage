__author__ = 'tholen'

from ROOT import TFile
from MyPackage.TtGammaAnalysis.CRPostProcessor import CmsRunPostProcTool

class CmsRunHistoOverflow(CmsRunPostProcTool):
    """
    Takes care about histogram overflow bins. Ether removes it completely or
    fills it into nearest real bin. This works on fileservice histograms, it
    is applied directly after the process has finished.
    To use this, add histogram names in qsetting ether to 'overflowRemove' or
    'overflowMoveIn'.
    """

    def __init__(self, qsetting):
        super(CmsRunHistoOverflow, self).__init__()
        self.qsetting = qsetting

        # get lists (QStringList)
        removed = qsetting.value("overflowRemove", "None").toStringList()
        moved = qsetting.value("overflowMoveIn", "None").toStringList()

        # convert to pythonic lists
        self.histos_remove  = [str(l) for l in removed]
        self.histos_move_in = [str(l) for l in moved]

        if self.histos_remove == ["None"] and self.histos_move_in == ["None"]:
            self.tool_enabled = False


    def start(self, process):

        # only for single processes
        if type(process) == list:
            return

        # only when process really ran
        if process.reused_old_data:
            return

        self.started.emit(self)

        # do work
        file = TFile(process.service_file_name, "UPDATE")
        for folder_key in file.GetListOfKeys():

            # only Directories contain the histograms
            if not folder_key.IsFolder():
                continue

            # walk over histograms
            folder = folder_key.ReadObj()
            for histo_key in folder.GetListOfKeys():

                # move in
                if self.histos_move_in.count(histo_key.GetName()):
                    folder.cd()
                    histo = histo_key.ReadObj()
                    folder.Delete(histo_key.GetName() + ";1")
                    self.move_overflow_in(histo)
                    histo.Write()

                # or only remove
                elif self.histos_remove.count(histo_key.GetName()):
                    folder.cd()
                    histo = histo_key.ReadObj()
                    folder.Delete(histo_key.GetName() + ";1")
                    self.remove_overflow(histo)
                    histo.Write()

        file.Close()
        self.finished.emit(self)


    def move_overflow_in(self, histo):
        nbins     = histo.GetNbinsX()
        firstbin  = histo.GetBinContent(0)
        firstbin += histo.GetBinContent(1)
        lastbin   = histo.GetBinContent(nbins + 1)
        lastbin  += histo.GetBinContent(nbins)
        histo.SetBinContent(1, firstbin)
        histo.SetBinContent(nbins, lastbin)
        self.remove_overflow(histo)


    def remove_overflow(self, histo):
        histo.SetBinContent(0, 0.)
        histo.SetBinContent(histo.GetNbinsX() + 1, 0.)