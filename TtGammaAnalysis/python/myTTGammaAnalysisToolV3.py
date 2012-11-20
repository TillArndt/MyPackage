
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


    def calc_R_pur_bkg_uncert(self, R, first_bin, last_bin):
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
            "WJets": 0.3#1558. / 31314.
        }

        tt_bkg_sum = 0.
        ttgamma_bkg_sum = 0.
        for sample, rel_err in rel_errors.items():
            tt_bkg_sum += histos[sample].GetBinContent(first_bin)
            ttgamma_bkg_sum += histos[sample].GetBinContent(last_bin)

        R_err2 = 0.
        for sample, rel_err in rel_errors.items():
            factor = (
                  histos[sample].GetBinContent(last_bin)
                / histos[sample].GetBinContent(first_bin)
            )
            deriv = R * (1 / tt_bkg_sum + factor / ttgamma_bkg_sum)
            err_smpl = histos[sample].GetBinContent(last_bin) * rel_err * deriv
            R_err2 += err_smpl**2

        return R_err2**0.5


    def scale_to_lumi(self, histos, lumi):
        """
        """

        for histo in histos:
            histo.histo.Scale(lumi/histo.lumi)


    def nfit_to_tex(self, n_fit, n_fit_err, n_predict):
        """
        """

        f1 = open(root_style.DIR_PLOTS + "n_fit.tex", "w")
        print >> f1, int(round(n_fit,0)),
        print >> f1, "\\pm", int(round(n_fit_err,0))
        f1.close()

        f2 = open(root_style.DIR_PLOTS + "n_predict.tex", "w")
        print >> f2, round(n_predict,1)
        f2.close()


    def R_to_tex(self, R, R_err_fit, R_err_sys):
        """
        """

        if R_err_sys:
            f = open(root_style.DIR_PLOTS + "R_sys.tex", "w")
        else:
            f = open(root_style.DIR_PLOTS + "R.tex", "w")
        print >> f, round(R,3),
        print >> f, "\\;\\pm", round(R_err_fit,3), " \\,\\tn{(fit)} ",
        if R_err_sys:
            print >> f, "\\;\\pm", round(R_err_sys,3), " \\,\\tn{(sys.)} "
        f.close()


    def xsec_to_tex(self, R, R_err_fit, R_err_sys):
        """
        """

        tt_xsec = 161.9
        tt_err_stat = 2.5
        tt_err_sys  = 5.1
        tt_err_lumi = 3.6

        xsec = R * tt_xsec
        xsec_err_stat = xsec*(
              (R_err_fit / R)**2
            + (tt_err_stat / tt_xsec)**2
        )**.5
        xsec_err_sys = xsec*(
              (R_err_sys / R)**2
            + (tt_err_sys / tt_xsec)**2
            + (tt_err_lumi / tt_xsec)**2
        )**.5


        f = open(root_style.DIR_PLOTS + "xsec.tex", "w")
        print >> f, round(xsec,1),
        print >> f, "\\;\\pm", round(xsec_err_stat,1), " \\,\\tn{(stat.)} ",
        print >> f, "\\;\\pm", round(xsec_err_sys,1), " \\,\\tn{(sys.)} ",
        print >> f, "\\;\\tn{pb}"
        f.close()

        k = 2.0
        k_err = 0.5

        xsec_k = xsec * k
        xsec_err_stat_k = xsec_err_stat * k
        xsec_err_sys_k = ( (xsec_err_sys*k)**2 + (xsec*k_err)**2 )**.5

        f = open(root_style.DIR_PLOTS + "xsec_kfactor.tex", "w")
        print >> f, round(xsec_k,1),
        print >> f, "\\;\\pm", round(xsec_err_stat_k,1), " \\,\\tn{(stat.)} ",
        print >> f, "\\;\\pm", round(xsec_err_sys_k,1), " \\,\\tn{(sys.)} ",
        print >> f, "\\;\\tn{pb}"
        f.close()


    def sys_err_to_tex(self, filename, relerr):
        """
        """

        f = open(root_style.DIR_PLOTS + filename + ".tex", "w")
        print >> f, round(relerr * 100., 2)
        f.close()


    def number_to_tex(self, filename, number, roundTo):
        """
        """

        f = open(root_style.DIR_PLOTS + filename + ".tex", "w")
        print >> f, round(number * 100., roundTo)
        f.close()


    def run_procedure(self):
        """
        """

        # load fit result
        fit_paramEB, template_sumEB = self.load_fit_results(
            root_style.DIR_PLOTS
            + "../CRTemplateFitTool/sihihEBRebinned/FitResults.ini"
        )
        fit_paramEE, template_sumEE = self.load_fit_results(
            root_style.DIR_PLOTS
            + "../CRTemplateFitTool/sihihEERebinned/FitResults.ini"
        )
        N_fit_EB = (
            fit_paramEB["real photons"][0]
            * template_sumEB["real photons"]
        )
        N_fit_EE = (
            fit_paramEE["real photons"][0]
            * template_sumEE["real photons"]
        )
        N_MC_predict = template_sumEB["real photons"] + template_sumEE["real photons"]
        N_fit = N_fit_EB + N_fit_EE
        N_fit_err = (
            (
                fit_paramEE["real photons"][1]
                * template_sumEE["real photons"]
            )**2 + (
                fit_paramEB["real photons"][1]
                * template_sumEB["real photons"]
            )**2
        )**.5
        N_percent_EB = N_fit_EB / N_fit
        N_percent_EE = N_fit_EE / N_fit

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
        last_bin = histo_data.GetXaxis().FindBin("H/E")

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
        pur_gamma_err_whiz = 0.083 * (
            pur_gamma / tt_gamma_signal
            * (1 + pur_gamma)
        )

        pur_tt = (
            (
                histo_tt.GetBinContent(first_bin)
                + histo_sig.GetBinContent(first_bin)
            ) / (
                histo_sig.GetBinContent(first_bin)
                + histo_bkg.GetBinContent(first_bin)
            )
        )

        N_presel_data = histo_data.GetBinContent(first_bin)

        # uncertainty from ISR / FSR
        R_relerr_rad = 0.399

        # R
        R_denom = eff_gamma * N_presel_data * pur_tt
        R = N_fit * pur_gamma / R_denom
        R_err_fit = N_fit_err * pur_gamma / R_denom
        #R_err_eff = R * (N_percent_EB*0.005 + N_percent_EE*0.01)
        R_err_eff = R * 0.463  #TODO: automate!!
        R_err_pur_whiz = R * pur_gamma_err_whiz / pur_gamma
        R_err_pur_bkg = self.calc_R_pur_bkg_uncert(R, first_bin, last_bin)
        R_err_rad = R * R_relerr_rad
        R_err_sys = (
              R_err_eff**2
            + R_err_pur_whiz**2
            + R_err_pur_bkg**2
            + R_err_rad**2
        )**0.5

        # save for texing
        self.nfit_to_tex(N_fit, N_fit_err, N_MC_predict)
        self.R_to_tex(R, R_err_fit, 0)
        self.R_to_tex(R, R_err_fit, R_err_sys)
        self.xsec_to_tex(R, R_err_fit, R_err_sys)
        self.sys_err_to_tex("err_eff", R_err_eff/R)
        self.sys_err_to_tex("err_pur_whiz", R_err_pur_whiz/R)
        self.sys_err_to_tex("err_pur_bkg", R_err_pur_bkg/R)
        self.sys_err_to_tex("err_rad", R_err_rad/R)
        self.number_to_tex("pur_tt", pur_tt, 1)
        self.number_to_tex("pur_gamma", pur_gamma, 1)
        self.number_to_tex("eff_gamma", eff_gamma, 1)

        print "eff_gamma: ", eff_gamma
        print "pur_tt: ", pur_tt
        print "pur_gamma: ", pur_gamma
        print "pur_gamma_err: ", pur_gamma_err_whiz
        print "N_fit:", N_fit, "+-", N_fit_err
        print "N_MC_predict:", N_MC_predict
        print "R: ", R
        print "R_err_fit", R_err_fit
        print "R_err_eff", R_err_eff
        print "R_err_pur_whiz", R_err_pur_whiz
        print "R_err_pur_bkg", R_err_pur_bkg
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
