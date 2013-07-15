
import cmstoolsac3b.postprocessing as pprc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.settings as settings
import cmstoolsac3b.wrappers as wrappers
from PyQt4 import QtCore

class XsecCalculator(pprc.PostProcTool):
    can_reuse = False

    def configure(self):
        self.fit_template_name = settings.get_pretty_name("realTemplateSihih")

    def load_fit_results(self, filename):
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
            "WJets": 0.3 #1558. / 31314.
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
        for histo in histos:
            histo.histo.Scale(lumi/histo.lumi)

    def run(self):
        self.configure()

        # load fit result
        fit_paramEB, template_sumEB = self.load_fit_results(
            self.plot_output_dir
            + "../TemplateFitToolSihih/FitResults.ini"
        )
        N_fit_EB = (
            fit_paramEB[self.fit_template_name][0]
            * template_sumEB[self.fit_template_name]
        )
        N_MC_predict = template_sumEB[self.fit_template_name] # + template_sumEE["real photons"]
        N_fit = N_fit_EB # + N_fit_EE
        N_fit_err = (
                        (
                           # fit_paramEE["real photons"][1]
                           # * template_sumEE["real photons"]
                           # )**2 + (
                            fit_paramEB[self.fit_template_name][1]
                            * template_sumEB[self.fit_template_name]
                        ) #**2
                    ) #**.5
        N_percent_EB = N_fit_EB / N_fit
        # N_percent_EE = N_fit_EE / N_fit

        # scale cutflows to lumi
        #self.scale_to_lumi(self.cutflow_fileservice, self.lumi)

        # prepare histos
        histo_data = list(gen.filter(gen.pool_content(),
            {"name":"CombinedCutflow", "is_data":True}
        ))[0].histo
        histos_mc = list(gen.filter(gen.pool_content(),
            {"name":"CombinedCutflow", "is_data":False}
        ))[0].stack.GetHists()
        histo_sig = None
        histo_bkg = None
        histo_tt  = None
        for histo in histos_mc:
            title = histo.GetTitle()
            if title == "t#bar{t}#gamma (Signal)":
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
        last_bin = histo_data.GetXaxis().FindBin(
            settings.get_pretty_name("drjet")
        )

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
#        pur_gamma_err_whiz = 0.083 * (
#            pur_gamma / tt_gamma_signal
#            * (1 + pur_gamma)
#            )

        pur_tt = (
            (
                histo_tt.GetBinContent(first_bin)
                + histo_sig.GetBinContent(first_bin)
                ) / (
                histo_sig.GetBinContent(first_bin)
                + histo_bkg.GetBinContent(first_bin)
                )
            )

        # selection performance
        N_presel_data = histo_data.GetBinContent(first_bin)
        N_sel_data = histo_data.GetBinContent(last_bin)
        StoB_gamma =    (
                            histo_sig.GetBinContent(last_bin)
                            / histo_bkg.GetBinContent(last_bin)
                        )
        StoB_presel =   (
                            histo_tt.GetBinContent(first_bin)
                            / (
                                histo_bkg.GetBinContent(first_bin)
                                - histo_tt.GetBinContent(first_bin)
                            )
                        )

        # r
        R_denom = eff_gamma * N_presel_data * pur_tt
        R = N_fit * pur_gamma / R_denom
        R_err_fit = N_fit_err * pur_gamma / R_denom
        #r_err_eff = R * (N_percent_EB*0.005 + N_percent_EE*0.01)
        #r_err_eff = R * 0.463  #TODO: automate!!
#        r_err_pur_whiz = R * pur_gamma_err_whiz / pur_gamma
        #R_err_pur_bkg = self.calc_R_pur_bkg_uncert(R, first_bin, last_bin)
#        R_err_rad = R * R_relerr_rad
  #      R_err_sys = (
        #                R_err_eff**2
   #                     + R_err_pur_whiz**2
         #               + R_err_pur_bkg**2
 #                       + R_err_rad**2
    #                    )**0.5

        xsec = R * settings.samples["TTJets"].x_sec
        xsec_err_stat = xsec * R_err_fit / R
     #   xsec_err_sys = xsec * R_err_sys / R

        wrp = wrappers.Wrapper(name = "x_sec_result")
        wrp.eff_gamma           =  eff_gamma
        wrp.pur_tt              =  pur_tt
        wrp.pur_gamma           =  pur_gamma
#        wrp.pur_gamma_err_whiz  =  pur_gamma_err_whiz
        wrp.N_sel_data          =  N_sel_data
        wrp.N_presel_data       =  N_presel_data
        wrp.StoB_presel         =  StoB_presel
        wrp.StoB_gamma          =  StoB_gamma
        wrp.N_fit               =  N_fit
        wrp.N_fit_err           =  N_fit_err
        wrp.N_MC_predict        =  N_MC_predict
        wrp.R                   =  R
        wrp.R_err_fit           =  R_err_fit
#        wrp.R_err_pur_whiz      =  R_err_pur_whiz
        wrp.xsec                =  xsec
        wrp.xsec_err_stat       =  xsec_err_stat
        settings.post_proc_dict["x_sec_result"] = wrp
        wrp.write_info_file(self.plot_output_dir + "x_sec_result.info")
