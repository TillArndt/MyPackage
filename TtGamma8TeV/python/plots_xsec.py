
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.settings as settings
import cmstoolsac3b.wrappers as wrappers

class XsecCalculator(ppc.PostProcTool):

    def __init__(self, name=None):
        super(XsecCalculator, self).__init__(name)
        self.fir_res_dir        = ""
        self.fit_template_name  = ""
        self.fake_template_name = ""
        self.pre_count_name     = "FidCountPre,"
        self.fid_count_name     = "FidCountPost,"
        self.post_count_name    = ""
        self.n_sig_ttgam_wrp    = None

    def configure(self):
        pass

#    def load_fit_results(self):
#        fit_res = wrappers.Wrapper.create_from_file(self.fir_res_dir)
#        parameters      = {}
#        mc_cont         = {}
#        data_cont       = {}
#        data_cont_err   = {}
#        for i, legend in enumerate(fit_res.legend):
#            parameters[legend]      = (fit_res.value[i], fit_res.error[i])
#            mc_cont[legend]         = fit_res.binIntegralMC[i]
#            data_cont[legend]       = fit_res.binIntegralScaled[i]
#            data_cont_err[legend]   = fit_res.binIntegralScaledError[i]
#
#        # fit result
#        fit_param, mc_cont, data_cont, data_cont_err, fit_res = self.load_fit_results()
#        r.N_MC_predict  = mc_cont[self.fit_template_name]
#        r.N_fit         = data_cont[self.fit_template_name]
#        r.N_fake        = data_cont[self.fake_template_name]
#        r.N_data_tmpl   = fit_res.dataIntegral
#        r.N_fit_err     = data_cont_err[self.fit_template_name]
#
#        return parameters, mc_cont, data_cont, data_cont_err, fit_res

    def run(self):
        self.configure()

        # store results in wrapper
        r = self.n_sig_ttgam_wrp
        r.name = self.name
        self.result = r

        # prepare mc counts
        class counts(object): pass
        c = counts()
        c.sig_pre   = 0.
        c.sig_fid   = 0.
        c.sig_post  = 0.
        c.bkg_pre   = 0.
        c.bkg_post  = 0.
        c.tt_pre    = 0.
        c.tt_post   = 0
        for smp in settings.mc_samples().itervalues():
            legend = smp.legend
            if legend == "t#bar{t}#gamma (Signal)":
                c.sig_pre  += smp.log_event_counts[self.pre_count_name] / smp.lumi
                c.sig_fid  += smp.log_event_counts[self.fid_count_name] / smp.lumi
                c.sig_post += smp.log_event_counts[self.post_count_name] / smp.lumi
            else:
                c.bkg_pre  += smp.log_event_counts[self.pre_count_name] / smp.lumi
                c.bkg_post += smp.log_event_counts[self.post_count_name] / smp.lumi
            if legend == "t#bar{t} inclusive":
                c.tt_pre  += smp.log_event_counts[self.pre_count_name] / smp.lumi
                c.tt_post += smp.log_event_counts[self.post_count_name] / smp.lumi
        data_lumi_sum = settings.data_lumi_sum()
        for k in c.__dict__.keys():
            c.__dict__[k] *= data_lumi_sum

        # prepare data counts
        c.data_pre  = 0.
        c.data_post = 0.
        for smp in settings.data_samples().itervalues():
            c.data_pre  += smp.log_event_counts[self.pre_count_name]
            c.data_post += smp.log_event_counts[self.post_count_name]

        # selection performance
        r.eff_gamma     = c.sig_post / c.sig_pre
        r.eff_gamma_fid = c.sig_post / c.sig_fid
        r.pur_tt        = (c.tt_pre + c.sig_pre) / (c.bkg_pre + c.sig_pre)
        r.N_presel_data = c.data_pre
        r.N_sel_data    = c.data_post
        r.StoB_gamma    = c.sig_post / c.bkg_post
        r.StoB_presel   = c.tt_pre   / (c.bkg_pre - c.tt_pre)

        # background-substracted number of ttgamma signal events
        # r.n_sig_ttgam   = self.n_sig_ttgam_wrp.n_sig_ttgam

        # R
        R_denom         = r.eff_gamma * r.N_presel_data * r.pur_tt
        r.R             = r.n_sig_ttgam     / R_denom
        r.R_err_stat    = r.n_sig_ttgam_err / R_denom

        # R_fid
        R_fid_denom     = r.eff_gamma_fid * r.N_presel_data * r.pur_tt
        r.R_fid         = r.n_sig_ttgam     / R_fid_denom
        r.R_fid_err_stat= r.n_sig_ttgam_err / R_fid_denom

        # xsec
        r.xsec          = r.R * settings.ttbar_xsec_cms
        r.xsec_err_stat = r.xsec * r.R_err_stat / r.R

        self.message(str(r))


class XsecCalculatorSihih(XsecCalculator):
    def configure(self):
        self.post_count_name = "Nm1CountPostsihihEB,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["TemplateFitToolSihih"]


class XsecCalculatorSihihShift(XsecCalculator):
    def configure(self):
        self.post_count_name = "Nm1CountPostsihihEB,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["TemplateFitToolSihihShift"]


class XsecCalculatorChHadIso(XsecCalculator):
    def configure(self):
        self.post_count_name = "Nm1CountPostchargedHadronIsoEB,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["TemplateFitToolChHadIso"]


class XsecCalculatorABCD(XsecCalculator):
    def configure(self):
        self.post_count_name = "Nm1CountPostsihihEB,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["RealPhotonsABCD"]


class XsecCalculatorABCDMC(XsecCalculator):
    def configure(self):
        self.post_count_name = "Nm1CountPostsihihEB,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["RealPhotonsABCD"]


class XsecCalculatorShilpi(XsecCalculator):
    def configure(self):
        self.post_count_name = "FullTightIDCount,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["ShilpiMethod"]


class XsecCalculatorShilpiMC(XsecCalculator):
    def configure(self):
        self.post_count_name = "FullTightIDCount,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["ShilpiMethodMC"]


class XsecCalculatorShilpiCheck(XsecCalculator):
    def configure(self):
        self.post_count_name = "FullTightIDCount,"
        self.n_sig_ttgam_wrp = settings.post_proc_dict["ShilpiMethodCheck"]


XsecCalculators = ppc.PostProcChain("XsecCalculators", [
    XsecCalculatorSihih,
    XsecCalculatorSihihShift,
    XsecCalculatorChHadIso,
    XsecCalculatorShilpi,
    XsecCalculatorABCD,
])