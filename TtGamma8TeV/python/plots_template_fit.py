
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.wrappers as wrp
import cmstoolsac3b.rendering as rnd
import cmstoolsac3b.settings as settings
from ROOT import TF1, TPaveText
import itertools
import re
import plots_commons as com

############################################ lists histo and analyzer names ###
analyzers_mc_sihih_shift = [
    re.compile("realTemplateSihihShift"),
    re.compile("fakeTemplateSihihShift"),
]

analyzers_mc = [
    "realTemplateChHadIso",
    "fakeTemplateChHadIso",
    "realTemplateSihih",
    "fakeTemplateSihih",
    "realNm2PlotsihihEB",
    "fakeNm2PlotsihihEB",
    "realNm2PlotchargedHadronIsoEB",
    "fakeNm2PlotchargedHadronIsoEB",
#    "Nm1PlotSihihChHadIsoInv", # attention: do not let data and mc be merged 
#    "Nm1PlotChHadIsoSihihInv",
]
analyzers_mc += analyzers_mc_sihih_shift

analyzers_data = [
    "dataTemplateFitHistoSihih",
    "dataTemplateFitHistoChHadIso"
]
histos = [
    "sihihEB",
    "ChHadIso",
    "histo",
]

##################################################### convenience functions ###
def color(name):
    # mc templates
    real_color = 409
    fake_color = 625
    if name[:4] == "real":
        return real_color
    if name[:4] == "fake":
        return fake_color

    if name[-3:] == "Inv":
        return fake_color

def get_legend_name(key):
    if "TemplateSihihShift" in key:
        return key[:4]
    else:
        return settings.get_pretty_name(key)

def cosmetica1(wrps):
    for w in wrps:
        name = get_legend_name(w.analyzer)
        w.histo.SetTitle(name)
        w.histo.SetYTitle(w.histo.GetYaxis().GetTitle() + " / a.u.")
        w.legend = name
        w.histo.SetLineColor(color(w.analyzer))
        w.histo.SetLineWidth(3)
        w.histo.SetFillStyle(0)
        yield w

def cosmetica2(wrps):
    for w in wrps:
        name = get_legend_name(w.analyzer)
        w.histo.SetTitle(name)
        w.legend = name
        w.histo.SetLineColor(1)
        w.histo.SetLineWidth(1)
        w.histo.SetFillColor(color(w.analyzer))
        w.histo.SetFillStyle(1001)
        yield w

def scale_templates_to_fit(fit_function, templates):
    for i in range(0, len(templates)):
        templates[i].histo.Scale(fit_function.GetParameter(i))

def calc_chi2(x_min, x_max, templates, fitted):
    """"""
    ratio = gen.op.div((fitted, gen.op.sum(templates))).histo
    chi2 = 0.
    bin_min = ratio.GetXaxis().FindBin(x_min)
    bin_max = ratio.GetXaxis().FindBin(x_max) + 1
    for i in xrange(bin_min, bin_max):
        if ratio.GetBinError(i) > 1e-43:
            chi2 += ((1 - ratio.GetBinContent(i))/ratio.GetBinError(i))**2
    return chi2

def find_x_range(data_hist):
    x_min = data_hist.GetXaxis().GetXmin()
    x_max = data_hist.GetXaxis().GetXmax()
    for i in xrange(data_hist.GetNbinsX()):
        if data_hist.GetBinContent(i):
            x_min = data_hist.GetXaxis().GetBinLowEdge(i)
            break
    for i in xrange(data_hist.GetNbinsX() - 1, 0, -1):
        if data_hist.GetBinContent(i):
            x_max = data_hist.GetXaxis().GetBinUpEdge(i)
            break
    return x_min, x_max


############################################### template processing classes ###

### fetch templates from fileservice, stack, plot #########
class TemplateStacks(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(TemplateStacks, self).__init__(name),
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)
        self.save_lin_log_scale = True

    def set_up_stacking(self):
        mc_tmplts = gen.fs_filter_sort_load({
            "analyzer"  : analyzers_mc,
            "name"      : histos
        })
        mc_tmplts = gen.gen_norm_to_lumi(mc_tmplts)

        mc_tmplts = gen.group(mc_tmplts)
        def stack_with_purity_info(grps):
            for grp in grps:
                sub_tot_list = [0., 0.]
                grp = list(com.count_ttgamma_photons(grp,sub_tot_list))
                grp = gen.mc_stack((grp,))
                grp = grp.next()
                grp.sub_tot_list = sub_tot_list
                yield grp
        mc_tmplts = list(stack_with_purity_info(mc_tmplts))

        shift_dict = {"analyzer" : analyzers_mc_sihih_shift}
        mc_tmplts_plot = list(
            gen.rejector(mc_tmplts, shift_dict)
        )
        settings.post_proc_dict["mc_templates"] = mc_tmplts_plot
        self.stream_stack = mc_tmplts_plot

        settings.post_proc_dict["mc_templates_sihih_shift"] = list(
            gen.filter(mc_tmplts, shift_dict)
        )


### fitting tools #########################################
class TemplateFitTool(ppt.FSStackPlotter):
    def __init__(self, name = None):
        super(TemplateFitTool, self).__init__(name)
        self.mc_tmplts      = None
        self.fitted         = None
        self.fitbox_bounds  = None
        self.result         = wrp.Wrapper(name = "FitResults")
        self.n_templates    = 0

    def configure(self):
        super(TemplateFitTool, self).configure()
        self.canvas_decorators.append(com.LumiTitleBox)
        self.save_lin_log_scale = True
        self.save_name_lambda = lambda wrp: self.plot_output_dir + wrp.name.split("_")[1]

    def build_fit_function(self, mc_tmplts):
        templates = [tw.histo for tw in mc_tmplts]
        size = len(templates)
        self.n_templates = size

        def fit_func(x, par):
            value = 0.
            for i, hist in enumerate(templates):
                value += par[i] * hist.GetBinContent(hist.FindBin(x[0]))
            return value

        tf1 = TF1(
            "MyFitFunc",
            fit_func,
            self.x_min,
            self.x_max,
            size
        )
        for i in xrange(0, size):
            tf1.SetParameter(i,1.)

        return tf1

    def do_the_fit(self, mc_tmplts):
        self.fitted.histo.Fit(
            self.fit_func, "WL M N", "", self.x_min, self.x_max
        )

    def make_fit_results(self, mc_tmplts, chi2):
        """"""
        r = self.result
        fit_function = self.fit_func
        r.Chi2 = chi2
        r.NDF = fit_function.GetNDF()
        r.dataIntegral = self.fitted.histo.Integral()
        r.legend = []
        r.value = []
        r.error = []
        r.binIntegralMC = []
        r.binIntegralScaled = []
        r.binIntegralScaledError = []
        for i, tmplt in enumerate(mc_tmplts):
            r.legend.append(tmplt.legend)
            r.value.append(fit_function.GetParameter(i))
            r.error.append(fit_function.GetParError(i))
            r.binIntegralMC.append(tmplt.histo.Integral() / r.value[-1])
            r.binIntegralScaled.append(tmplt.histo.Integral())
            r.binIntegralScaledError.append(
                r.binIntegralScaled[-1] * r.error[-1] / r.value[-1]
            )
            if tmplt.legend == "real":
                r.mc_real_photon_ttgamma  = tmplt.sub_tot_list[0]
                r.mc_real_photon_total    = tmplt.sub_tot_list[1]
                r.pur_ttgam = r.mc_real_photon_ttgamma / r.mc_real_photon_total
                r.n_sig             = r.binIntegralScaled[-1]
                r.n_sig_err         = r.binIntegralScaledError[-1]
                r.n_sig_ttgam       = r.n_sig * r.pur_ttgam
                r.n_sig_ttgam_err   = r.n_sig_err * r.pur_ttgam

    def make_fit_textbox(self):
        res = self.result
        x1, x2, y2 = self.fitbox_bounds
        y1 = y2 - ((len(res.legend) + 1) * 0.04)

        textbox = TPaveText(x1,y1,x2,y2,"brNDC")
        textbox.SetBorderSize(1)
        textbox.SetLineColor(0)
        textbox.SetLineStyle(1)
        textbox.SetLineWidth(0)
        textbox.SetFillColor(0)
        textbox.SetFillStyle(1001)

        chi2 = (
            "#chi^{2} / NDF = "
            + str(round(res.Chi2,2))
            + " / "
            + str(res.NDF)
            )
        textbox.AddText(chi2)

        text = []
        for i, legend in enumerate(res.legend):
            text.append(
                "N_{"
                + legend
                + "} = %d #pm %d"%(
                    res.binIntegralScaled[i],
                    res.binIntegralScaledError[i]
                    )
            )
        for txt in reversed(text):
            textbox.AddText(txt)
        return textbox

    def set_up_stacking(self):
        # get templates and combine mc stack to single histograms
        data_lumi = settings.data_lumi_sum_wrp()
        def histo_wrapperize(stk_wrps):
            for s_w in stk_wrps:
                h_w = wrp.HistoWrapper(s_w.histo, **s_w.all_info())
                h_w = gen.op.prod((h_w, data_lumi))
                h_w.sub_tot_list = s_w.sub_tot_list
                yield h_w
        mc_tmplts = histo_wrapperize(self.mc_tmplts)
        mc_tmplts = list(cosmetica2(mc_tmplts))

        # do fit procedure
        self.fitted = gen.op.sum(self.fitted)
        self.x_min, self.x_max = find_x_range(self.fitted.histo)
        self.fit_func = self.build_fit_function(mc_tmplts)
        self.do_the_fit(mc_tmplts)

        scale_templates_to_fit(self.fit_func, mc_tmplts)
        chi2 = calc_chi2(self.x_min, self.x_max, mc_tmplts, self.fitted)
        self.make_fit_results(mc_tmplts, chi2)

        fit_textbox = self.make_fit_textbox()
        textboxes = {mc_tmplts[0].name: fit_textbox}
        self.canvas_decorators.append(
            rnd.TextBoxDecorator(None, True, textbox_dict=textboxes)
        )

        tmplt_stacks = [gen.op.stack(mc_tmplts)]
        stream_stack = [(tmplt_stacks[0], self.fitted)]
        self.stream_stack = gen.pool_store_items(stream_stack)


class TemplateFitToolSihih(TemplateFitTool):
    def configure(self):
        super(TemplateFitToolSihih, self).configure()
        self.fitbox_bounds  = 0.63, 0.93, 0.60
        self.mc_tmplts      = gen.filter(
            settings.post_proc_dict["mc_templates"], {
            "analyzer"  : ("realTemplateSihih", "fakeTemplateSihih"),
            "name"      : "sihihEB",
        })
        self.fitted         = gen.fs_filter_sort_load({
            "analyzer"  : "dataTemplateFitHistoSihih",
            "name"      : "sihihEB",
            "is_data"   : True,
        })


class TemplateFitToolChHadIso(TemplateFitTool):
    def configure(self):
        super(TemplateFitToolChHadIso, self).configure()
        self.fitbox_bounds  = 0.33, 0.62, 0.88
        self.mc_tmplts      = gen.filter(
            settings.post_proc_dict["mc_templates"], {
            "analyzer"  : ("realTemplateChHadIso", "fakeTemplateChHadIso"),
            "name"      : "ChHadIso",
        })
        self.fitted         = gen.fs_filter_sort_load({
            "analyzer"  : "dataTemplateFitHistoChHadIso",
            "name"      : "ChHadIso",
            "is_data"   : True,
        })


class TemplateFitToolSihihShift(TemplateFitTool):

    def configure(self):
        super(TemplateFitToolSihihShift, self).configure()
        self.fitbox_bounds  = 0.63, 0.93, 0.60
        self.mc_tmplts      = settings.post_proc_dict["mc_templates_sihih_shift"]
        self.fitted         = gen.fs_filter_sort_load({
            "analyzer"  : "dataTemplateFitHistoSihih",
            "name"      : "sihihEB",
            "is_data"   : True,
        })

    def build_fit_function(self, mc_tmplts):
        grouped = itertools.groupby(mc_tmplts, lambda w: w.analyzer[:-4])
        templates = [list(w for w in grp[1]) for grp in grouped]
        size = len(templates)
        self.template_matrix = templates
        first_histo = templates[0][0].histo

        def fit_func(x, par):
            value = 0.
            shift = par[size]
            shift = min(73., shift)
            shift = max(0., shift)
            bin_number = first_histo.FindBin(x[0])
            for i, hists in enumerate(templates):
                i_shift = int(shift)
                rest = shift - i_shift
                lower = hists[i_shift  ].histo.GetBinContent(bin_number)
                upper = hists[i_shift+1].histo.GetBinContent(bin_number)
                val = (1 - rest) * lower + rest * upper
                value += par[i] * val
            return value

        tf1 = TF1(
            "MyShiftFitFunc",
            fit_func,
            self.x_min,
            self.x_max,
            size + 1
        )
        for i in xrange(0, size + 1):
            tf1.SetParameter(i,1.)

        return tf1

    def do_the_fit(self, mc_tmplts):
        super(TemplateFitToolSihihShift, self).do_the_fit(mc_tmplts)
        size = len(self.template_matrix)
        shift = self.fit_func.GetParameter(size)
        picked_num = int(round(shift))
        del mc_tmplts[:]
        for i in range(size):
            tmplt = self.template_matrix[i][picked_num]
            tmplt.analyzer = tmplt.analyzer[:-4]
            mc_tmplts.append(self.template_matrix[i][picked_num])
        settings.post_proc_dict["fitted_shift_templates"] = mc_tmplts[:]

    def make_fit_results(self, mc_tmplts, chi2):
        super(TemplateFitToolSihihShift, self).make_fit_results(mc_tmplts, chi2)
        res = self.result
        size = len(self.template_matrix)
        val = self.fit_func.GetParameter(size)
        err = self.fit_func.GetParError(size)
        res.shift_val = val*0.00002 - 0.001
        res.shift_err = err*0.00002

    def make_fit_textbox(self):
        box = super(TemplateFitToolSihihShift, self).make_fit_textbox()
        box.AddText(
            "#delta = (%.3f #pm %.3f)#upoint 10^{-4}" % (
                self.result.shift_val*10000,
                self.result.shift_err*10000
            )
        )
        return box


### plot templates overlayed ##############################
def overlayed_template_iter():
    return itertools.chain(
        settings.post_proc_dict["mc_templates"],
        settings.post_proc_dict.get("fitted_shift_templates", list())
    )

class TemplateOverlaysNormIntegral(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(TemplateOverlaysNormIntegral, self).__init__(name),
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)

    def set_up_stacking(self):
        key_func = lambda w: w.analyzer[4:]
        mc_tmplts = overlayed_template_iter()
        mc_tmplts = (wrp.HistoWrapper(w.histo, **w.all_info()) for w in mc_tmplts)
        mc_tmplts = gen.gen_norm_to_integral(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        mc_tmplts = sorted(mc_tmplts, key=key_func)
        mc_tmplts = gen.group(mc_tmplts, key_func=key_func)
        self.stream_stack = mc_tmplts


class TemplateOverlaysNormLumi(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(TemplateOverlaysNormLumi, self).__init__(name),
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)

    def set_up_stacking(self):
        key_func = lambda w: w.analyzer[4:]
        mc_tmplts = overlayed_template_iter()
        mc_tmplts = (wrp.HistoWrapper(w.histo, **w.all_info()) for w in mc_tmplts)
        mc_tmplts = gen.gen_norm_to_lumi(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        mc_tmplts = sorted(mc_tmplts, key=key_func)
        mc_tmplts = gen.group(mc_tmplts, key_func=key_func)
        self.stream_stack = mc_tmplts


TemplateFitTools = ppc.PostProcChain(
    "TemplateFitTools",
    [
        TemplateStacks,
        TemplateFitToolSihihShift,
        TemplateFitToolSihih,
        TemplateFitToolChHadIso,
        TemplateOverlaysNormLumi,
        TemplateOverlaysNormIntegral,
#        DataDrvTemplates,
#        TemplateFitToolSihihDaDrv,
#        TemplateFitToolChHadIsoDaDrv,
    ]
)




################################ data-driven templates (not needed anymore) ###
class DataDrvTemplates(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(DataDrvTemplates, self).__init__(name)
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)

    def set_up_stacking(self):
        def cosmeticaDatDrv(wrps):
            for w in wrps:
                name = settings.get_pretty_name(w.analyzer)
                w.histo.SetTitle(name)
                w.legend = name
                w.is_data = False
                w.histo.SetLineColor(color(w.analyzer))
                w.histo.SetLineWidth(3)
                w.histo.SetFillStyle(0)
                yield w
        tmplts = settings.post_proc_dict["mc_templates"]
        tmplts = gen.filter(tmplts, {"is_data": True})
        tmplts = (wrp.HistoWrapper(w.histo, **w.all_info()) for w in tmplts)
        tmplts = gen.gen_norm_to_integral(tmplts)
        tmplts = cosmeticaDatDrv(tmplts)
        self.stream_stack = tmplts


class TemplateFitToolSihihDaDrv(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolSihihDaDrv, self).__init__(name)
        self.name_real      = "realTemplateSihih"
        self.name_fake      = "Nm1PlotSihihChHadIsoInv"
        self.name_data      = "dataTemplateFitHistoSihih"
        self.name_histo     = ("sihihEB", "histo")
        self.fitbox_bounds  = 0.63, 0.93, 0.60
        mc_tmplts = gen.filter(settings.post_proc_dict["mc_templates"], {
            "analyzer"  : (self.name_real, self.name_fake),
            "name"      : self.name_histo
        })


class TemplateFitToolChHadIsoDaDrv(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolChHadIsoDaDrv, self).__init__(name)
        self.name_real      = "realTemplateChHadIso"
        self.name_fake      = "Nm1PlotChHadIsoSihihInv"
        self.name_data      = "dataTemplateFitHistoChHadIso"
        self.name_histo     = ("ChHadIso", "histo")
        self.fitbox_bounds  = 0.33, 0.62, 0.88
        mc_tmplts = gen.filter(settings.post_proc_dict["mc_templates"], {
            "analyzer"  : (self.name_real, self.name_fake),
            "name"      : self.name_histo
        })
