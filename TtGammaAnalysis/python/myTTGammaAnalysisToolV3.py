
__author__ = 'tholen'

from UserCode.RWTH3b.cmsRunController.tools.CRHistoDispatch import *
from UserCode.RWTH3b.cmsRunController.classes.CRRootStyle import CRRootStyle
root_style = CRRootStyle()
from PyQt4 import QtCore


class TTGammaAnalysisWorker(CRHistoWorker):
    """
    """

    def load_fit_results(self, filename):
        """
        """

        file = QtCore.QSettings(filename, 1)
        parameters = {}
        integrals  = {}
        n_par = file.beginReadArray("parameters")
        for i in range(0, n_par):
            file.setArrayIndex(i)
            legend = str(file.value("legend").toString())
            parameters[legend] = (
                file.value("value").toDouble()[0],
                file.value("error").toDouble()[0]
            )
            integrals[legend] = (
                file.value("binIntegral").toDouble()[0]
            )
        return parameters, integrals


    def calc_pur_uncert(self, pur, sig, last_bin):
        """
        """


        histos = {}
        for histo in self.cutflow_fileservice:
            histos[histo.sample] = histo.histo

        rel_errors = {
            "semiMuonBG": 24./157.5,
            "T_s": 0.11 / 2.27,
            "Tbar_s": 0.09 / 1.49,
            "T_t": 2.4 / 42.6,
            "Tbar_t": 3.4 / 64.6,
            "T_tW_DR": 0.6 / 5.3,
            "Tbar_tW_DR": 0.6 / 5.3,
            "DYJetsToLL": 272. / 4998.,
            "WJets": 1558. / 31314.
        }

        pur_err2 = 0.
        for sample, rel_err in rel_errors.items():
            sample_err = rel_err * histos[sample].GetBinContent(last_bin)
            pur_sample_err = sample_err * pur * pur / sig
            pur_err2 += pur_sample_err**2

        return pur_err2**0.5


    def scale_to_lumi(self, histos, lumi):
        """
        """

        for histo in histos:
            histo.histo.Scale(lumi/histo.lumi)


    def run_procedure(self):
        """
        """

        # load fit result
        fit_param, template_sum = self.load_fit_results(
            root_style.DIR_PLOTS
            + "../CRTemplateFitTool/sihihRebinned/FitResults.ini"
        )

        # scale cutflows to lumi
        self.scale_to_lumi(self.cutflow_fileservice, self.lumi)

        # prepare histos
        histo_data = self.cutflow_stacks[0].histo.GetHists()[0]
        histos_mc = self.cutflow_stacks[1].histo.GetHists()
        histo_sig = None
        histo_bkg = None
        histo_tt  = None
        for histo in histos_mc:
            title = histo.GetTitle()
            if title == "t#bar{t}#gamma #mu+Jets (Signal)":
                histo_sig = histo.Clone()
            else:
                if not histo_bkg:
                    histo_bkg = histo.Clone()
                else:
                    histo_bkg.Add(histo)
            if title == "t#bar{t} inclusive":
                histo_tt = histo.Clone()

        # the bins
        first_bin = histo_data.GetXaxis().GetFirst()
        last_bin = histo_data.GetXaxis().FindBin("hollow cone")

        # the quantities for R
        eff_gamma = (
            histo_sig.GetBinContent(last_bin)
            / histo_sig.GetBinContent(first_bin)
        )

        tt_gamma_signal = histo_sig.GetBinContent(last_bin)
        pur_gamma = (
            tt_gamma_signal
            / (
                histo_sig.GetBinContent(last_bin)
                + histo_bkg.GetBinContent(last_bin)
            )
        )
        pur_gamma_err_tt = self.calc_pur_uncert(
            pur_gamma,
            tt_gamma_signal,
            last_bin
        )

        pur_gamma_err = pur_gamma_err_tt

        pur_tt = (
            (
                histo_tt.GetBinContent(first_bin)
                + histo_sig.GetBinContent(first_bin)
            ) / (
                histo_sig.GetBinContent(first_bin)
                + histo_bkg.GetBinContent(first_bin)
            )
        )

        N_fit = (
            fit_param["real photons"][0]
            * template_sum["real photons"]
        )
        N_fit_err = (
            fit_param["real photons"][1]
            * template_sum["real photons"]
        )

        N_tt_data = histo_data.GetBinContent(first_bin)

        # R
        R_denom = eff_gamma * N_tt_data * pur_tt
        R = N_fit * pur_gamma / R_denom
        R_err_fit = N_fit_err * pur_gamma / R_denom
        R_err_eff = R * (0.828*0.005 + 0.172*0.01)
        R_err_pur = R * pur_gamma_err / pur_gamma
        R_err_rad = 0.00143
        R_err_sys = (R_err_eff**2 + R_err_pur**2 + R_err_rad**2)**0.5

        print "eff_gamma: ", eff_gamma
        print "pur_tt: ", pur_tt
        print "pur_gamma: ", pur_gamma
        print "pur_gamma_err_tt: ", pur_gamma_err_tt
        print "pur_gamma_err: ", pur_gamma_err
        print "N_fit:", N_fit
        print "R: ", R
        print "R_err_fit", R_err_fit
        print "R_err_eff", R_err_eff
        print "R_err_pur", R_err_pur
        print "R_err_rad", R_err_rad
        print "R_err_sys", R_err_sys


class TTGammaAnalysisTool(CRPostProcTool):
    """
    """

    def configure(self):
        self.after_every_process = False


    def start(self, processes):
        """
        """

        # plot dir will be changed for every fitter
        orig_DIR_PLOTS = root_style.DIR_PLOTS
        root_style.DIR_PLOTS = orig_DIR_PLOTS + self.__class__.__name__ + "/"
        root_style.create_folders()

        qset = self.main_settings
        lumi, parse_ok = qset.value("dataLumiSum", 1.).toDouble()

        qset.beginGroup(self.__class__.__name__)

        dispatch = CRCentralHistoDispatch()

        # build and run stackers
        request = CRHistoWorkerRequest(
            TTGammaAnalysisWorker,
            self.fetch_list("samples"),
            []
        )

        request.HIST_cutflow_stacks = self.fetch_list("cutflowStacks")
        request.HIST_cutflow_fileservice = self.fetch_list("cutflowFileservice")
        worker = dispatch.build_worker(request, processes, qset)
        worker.lumi = lumi
        worker.run_procedure()
        del worker

        qset.endGroup() # self.__class__.__name__
        root_style.DIR_PLOTS = orig_DIR_PLOTS
