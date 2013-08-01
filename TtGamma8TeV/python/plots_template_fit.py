
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.wrappers as wrp
import cmstoolsac3b.decorator as dec
import cmstoolsac3b.settings as settings
from ROOT import TF1, TPaveText
import itertools
import plots_commons as com

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

analyzers_mc = [
    "realTemplateChHadIso",
    "fakeTemplateChHadIso",
    "realTemplateSihih",
    "fakeTemplateSihih",
    "realNm2PlotsihihEB",
    "fakeNm2PlotsihihEB",
    "realNm2PlotchargedHadronIsoEB",
    "fakeNm2PlotchargedHadronIsoEB",
    "Nm1PlotSihihChHadIsoInv",
    "Nm1PlotChHadIsoSihihInv",
]
analyzers_data = [
    "dataTemplateFitHistoSihih",
    "dataTemplateFitHistoChHadIso"
]
histos = [
    "sihihEB",
    "ChHadIso",
    "histo",
]

def cosmetica1(wrps):
    for w in wrps:
        name = settings.get_pretty_name(w.analyzer)
        w.histo.SetTitle(name)
        w.legend = name
        w.histo.SetLineColor(color(w.analyzer))
        w.histo.SetLineWidth(3)
        w.histo.SetFillStyle(0)
        yield w

def cosmetica2(wrps):
    for w in wrps:
        name = settings.get_pretty_name(w.analyzer)
        w.histo.SetTitle(name)
        w.legend = name
        w.histo.SetLineColor(1)
        w.histo.SetLineWidth(1)
        w.histo.SetFillColor(color(w.analyzer))
        w.histo.SetFillStyle(1001)
        yield w

class TemplateStacks(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(TemplateStacks, self).__init__(name),
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)
        self.save_lin_log_scale = True

    def set_up_stacking(self):
        mc_tmplts = list(gen.fs_mc_stack({
            "analyzer"  : analyzers_mc,
            "name"      : histos
        }))
        settings.post_proc_dict["mc_templates"] = mc_tmplts
        self.stream_stack = mc_tmplts


class TemplateOverlaysNormIntegral(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(TemplateOverlaysNormIntegral, self).__init__(name),
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)

    def set_up_stacking(self):
        key_func = lambda w: w.analyzer[4:]
        mc_tmplts = settings.post_proc_dict["mc_templates"]
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
        mc_tmplts = settings.post_proc_dict["mc_templates"]
        mc_tmplts = (wrp.HistoWrapper(w.histo, **w.all_info()) for w in mc_tmplts)
        mc_tmplts = gen.gen_norm_to_lumi(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        mc_tmplts = sorted(mc_tmplts, key=key_func)
        mc_tmplts = gen.group(mc_tmplts, key_func=key_func)
        self.stream_stack = mc_tmplts


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



class TemplateFitTool(ppt.FSStackPlotter):
    def __init__(self, name = None):
        super(TemplateFitTool, self).__init__(name)
        self.name_real  = ""
        self.name_fake  = ""
        self.name_data  = ""
        self.name_histo = ""
        self.fitbox_bounds = None
        self.fit_result = wrp.Wrapper(name = "FitResults")

    def configure(self):
        super(TemplateFitTool, self).configure()
        self.canvas_decorators.append(com.LumiTitleBox)
        self.save_lin_log_scale = True
        self.save_name_lambda = lambda wrp: self.plot_output_dir + wrp.name.split("_")[1]

    def find_x_range(self, data_hist):
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
        self.x_min = x_min
        self.x_max = x_max

    def build_fit_function(self, template_wrappers):
        templates = [tw.histo for tw in template_wrappers]
        size = len(templates)

        def fit_func(x, par):
            value = 0.
            for i, hist in enumerate(templates):
                value += par[i] * hist.GetBinContent(hist.FindBin(x[0]))
            return value

        tf1 = TF1(
            "FitFunc",
            fit_func,
            self.x_min,
            self.x_max,
            size
        )
        for i in xrange(0, size):
            tf1.SetParameter(i,1.)

        return tf1

    def scale_templates_to_fit(self, fit_function, templates):
        for i in range(0, len(templates)):
            templates[i].histo.Scale(fit_function.GetParameter(i))

    def calc_chi2(self, templates, fitted):
        """"""
        ratio = gen.op.div((fitted, gen.op.sum(templates))).histo
        chi2 = 0.
        bin_min = ratio.GetXaxis().FindBin(self.x_min)
        bin_max = ratio.GetXaxis().FindBin(self.x_max) + 1
        for i in xrange(bin_min, bin_max):
            if ratio.GetBinError(i) > 1e-43:
                chi2 += ((1 - ratio.GetBinContent(i))/ratio.GetBinError(i))**2
        return chi2

    def save_fit_results(self, fit_function, templates, chi2, fitted):
        """"""
        res = self.fit_result
        res.Chi2 = chi2
        res.NDF = fit_function.GetNDF()
        res.dataIntegral = fitted.histo.Integral()
        res.legend = []
        res.value = []
        res.error = []
        res.binIntegralMC = []
        res.binIntegralScaled = []
        res.binIntegralScaledError = []
        for i, tmplt in enumerate(templates):
            res.legend.append(tmplt.legend)
            res.value.append(fit_function.GetParameter(i))
            res.error.append(fit_function.GetParError(i))
            res.binIntegralMC.append(tmplt.histo.Integral() / res.value[-1])
            res.binIntegralScaled.append(tmplt.histo.Integral())
            res.binIntegralScaledError.append(
                res.binIntegralScaled[-1] * res.error[-1] / res.value[-1]
            )
        res.write_info_file(self.plot_output_dir + "FitResults.info")

    def make_fit_textbox(self):
        res = self.fit_result

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
        mc_tmplts = gen.filter(settings.post_proc_dict["mc_templates"],
            {
                "analyzer"  : (self.name_real, self.name_fake),
                "name"      : self.name_histo
            }
        )
        def set_no_data(wrps):
            for w in wrps:
                w.is_data = False
                yield w
        mc_tmplts = set_no_data(mc_tmplts)

        data_tmplts = gen.fs_filter_sort_load({
            "analyzer"  : self.name_data,
            "name"      : self.name_histo
        })

        # combine mc stack to single histograms
        data_lumi = settings.data_lumi_sum_wrp()
        mc_tmplts = list(gen.gen_prod(itertools.izip(
            (wrp.HistoWrapper(w.histo, **w.all_info()) for w in mc_tmplts),
            itertools.repeat(data_lumi)
        )))

        mc_tmplts = list(cosmetica2(mc_tmplts))

        # do fit procedure
        fitted = gen.op.sum(data_tmplts)
        self.find_x_range(fitted.histo)
        fit_func = self.build_fit_function(mc_tmplts)
        fitted.histo.Fit(fit_func, "WL M N", "", self.x_min, self.x_max)
        self.scale_templates_to_fit(fit_func, mc_tmplts)
        chi2 = self.calc_chi2(mc_tmplts, fitted)
        self.save_fit_results(fit_func, mc_tmplts, chi2, fitted)

        #TODO: Make DECORATORS INSTANCEABLE BEFORE APPLYING
        #TODO: self.first_drawed.GetXaxis().SetNoExponent()
        textboxes = {
            mc_tmplts[0].name: self.make_fit_textbox()
        }
        class TextBoxDecorator(dec.Decorator):
            textbox_dict = textboxes
            def do_final_cosmetics(self):
                self.decoratee.do_final_cosmetics()
                textbox = self.textbox_dict[self.renderers[0].name]
                textbox.Draw()
        self.canvas_decorators.append(TextBoxDecorator)

        tmplt_stacks = [gen.op.stack(mc_tmplts)]
        stream_stack = [(tmplt_stacks[0], fitted)]
        self.stream_stack = gen.pool_store_items(stream_stack)


class TemplateFitToolSihih(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolSihih, self).__init__(name)
        self.name_real      = "realTemplateSihih"
        self.name_fake      = "fakeTemplateSihih"
        self.name_data      = "dataTemplateFitHistoSihih"
        self.name_histo     = "sihihEB"
        self.fitbox_bounds  = 0.63, 0.93, 0.60


class TemplateFitToolChHadIso(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolChHadIso, self).__init__(name)
        self.name_real      = "realTemplateChHadIso"
        self.name_fake      = "fakeTemplateChHadIso"
        self.name_data      = "dataTemplateFitHistoChHadIso"
        self.name_histo     = "ChHadIso"
        self.fitbox_bounds  = 0.33, 0.62, 0.88


class TemplateFitToolSihihDaDrv(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolSihihDaDrv, self).__init__(name)
        self.name_real      = "realTemplateSihih"
        self.name_fake      = "Nm1PlotSihihChHadIsoInv"
        self.name_data      = "dataTemplateFitHistoSihih"
        self.name_histo     = ("sihihEB", "histo")
        self.fitbox_bounds  = 0.63, 0.93, 0.60


class TemplateFitToolChHadIsoDaDrv(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolChHadIsoDaDrv, self).__init__(name)
        self.name_real      = "realTemplateChHadIso"
        self.name_fake      = "Nm1PlotChHadIsoSihihInv"
        self.name_data      = "dataTemplateFitHistoChHadIso"
        self.name_histo     = ("ChHadIso", "histo")
        self.fitbox_bounds  = 0.33, 0.62, 0.88


TemplateFitTools = ppc.PostProcChain(
    "TemplateFitTools",
    [
        TemplateStacks,
        DataDrvTemplates,
        TemplateOverlaysNormLumi,
        TemplateOverlaysNormIntegral,
        TemplateFitToolSihih,
        TemplateFitToolChHadIso,
        TemplateFitToolSihihDaDrv,
        TemplateFitToolChHadIsoDaDrv,
    ]
)