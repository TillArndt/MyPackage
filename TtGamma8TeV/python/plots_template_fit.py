
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.wrappers as wrp
import cmstoolsac3b.rendering as rnd
from cmstoolsac3b import settings
from cmstoolsac3b import diskio
from ROOT import TF1, TH1, TPaveText, TFractionFitter, TObjArray, Double, TMath, TFile
import itertools
import re, os
import copy
import plots_commons as com
import array
import theta_auto
theta_auto.config.theta_dir = os.environ["CMSSW_BASE"] + "/theta"


############################################ lists histo and analyzer names ###
analyzers_mc = [
    "TemplateChHadIsoreal",
    "TemplateChHadIsofake",
    "PlotLooseIDSihihSBreal",
    "PlotLooseIDSihihSBfake",
    "PlotSBIDreal",
    "PlotSBIDfake",
#    "TemplateChHadIsofakeGamma",
#    "TemplateChHadIsofakeOther",
#    "TemplateSihihreal",
#    "TemplateSihihfake",
#    "realNm2PlotsihihEB",
#    "fakeNm2PlotsihihEB",
#    "realNm2PlotchargedHadronIsoEB",
#    "fakeNm2PlotchargedHadronIsoEB",
#    "Nm1PlotSihihChHadIsoInv",
#    "Nm1PlotChHadIsoSihihInv",
]

analyzers_mc_sihih_shift = [
#    re.compile(r"TemplateSihihShift\d{4}real"),
#    re.compile(r"TemplateSihihShift\d{4}fake$"),
]

analyzers_mc_sihih_shift_sep_fakes = [
#    re.compile(r"TemplateSihihShift\d{4}real"),
#    re.compile(r"TemplateSihihShift\d{4}fakeGamma"),
#    "TemplateSihihfakeOther",
]

all_analyzers = (
    analyzers_mc
    + analyzers_mc_sihih_shift
    + analyzers_mc_sihih_shift_sep_fakes
)

analyzers_data = [
    "TemplateSihih",
    "TemplateChHadIso",
]

legend_tags = ["real", "fakeGamma", "fakeOther", "fake"]



##################################################### convenience functions ###
def color(key):
    for tag in legend_tags:
        if tag in key:
            return settings.get_color(tag)
    if "SihihSB" in key:
        return settings.get_color("fake")
    return 0


def get_legend_name(key):
    if "Template" in key:
        for tag in legend_tags:
            if tag in key:
                return settings.get_pretty_name(tag)
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


def find_x_range(data_hist):
    x_min = data_hist.GetXaxis().GetXmin()
    x_max = data_hist.GetXaxis().GetXmax()
    for i in xrange(data_hist.GetNbinsX()):
        if data_hist.GetBinContent(i):
            x_min = data_hist.GetXaxis().GetBinLowEdge(i)
            break
    for i in xrange(data_hist.GetNbinsX(), 0, -1):
        if data_hist.GetBinContent(i):
            x_max = data_hist.GetXaxis().GetBinUpEdge(i)
            break
    return x_min - 1e-10, x_max + 1e-10


def histo_wrapperize(stk_wrps):
    data_lumi = settings.data_lumi_sum_wrp()
    for s_w in stk_wrps:
        h_w = wrp.HistoWrapper(s_w.histo, **s_w.all_info())
        h_w = gen.op.prod((h_w, data_lumi))
        h_w.sub_tot_list = s_w.sub_tot_list
        yield h_w


############################################### template processing classes ###
### rebin chhadiso templates
do_chhadisorebinnig = True
do_dist_reweighting = True

chhadiso_bins = array.array(
    "d",
    [0., 0.25, 0.5, 0.75, 1., 1.5, 2., 2.5, 3., 3.75, 4.5, 5.25, 6., 7., 8., 9., 10.]
)
def rebin_chhadiso(wrps, skip_it=not do_chhadisorebinnig, norm_by_bin_width=False):
    for w in wrps:
        if not skip_it:  # want rebinning ??
            if ("TemplateChHadIso" in w.analyzer
                or "PlotLooseID" in w.analyzer
                or "PlotSBID" in w.analyzer):
                # rebinning
                histo = w.histo.Rebin(
                    len(chhadiso_bins) - 1,
                    w.name+"rebin",
                    chhadiso_bins
                )
                # divide by bin width  ### WARNING: DIFFERENT INTEGRAL!!
                if norm_by_bin_width:
                    for i in xrange(histo.GetNbinsX()+1):
                        factor = histo.GetBinWidth(i) / 0.25
                        histo.SetBinContent(i, histo.GetBinContent(i) / factor)
                        histo.SetBinError(i, histo.GetBinError(i) / factor)
                w.histo = histo
        yield w


### fetch templates from fileservice, stack, plot #########
class TemplateStacks(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(TemplateStacks, self).__init__(name),
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)
        self.save_lin_log_scale = True

    def set_up_stacking(self):
        mc_tmplts = rebin_chhadiso(
            gen.fs_filter_active_sort_load({
                "analyzer"  : all_analyzers,
            })
        )
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

        mc_tmplts_plot = list(
            gen.filter(mc_tmplts, {"analyzer": analyzers_mc})
        )
        self.result = mc_tmplts_plot
        self.stream_stack = mc_tmplts_plot


### fitting tools #########################################
class Fitter(object):
    def __init__(self):
        self.x_min = 0.
        self.x_max = 0.
        self.fit_func = None
        self.fitted = None
        self.mc_tmplts = None

    def build_fit_function(self, fitted, mc_tmplts, x_min, x_max):
        templates = [tw.histo for tw in mc_tmplts]
        size = len(templates)
        self.x_min, self.x_max = x_min, x_max
        self.fitted = fitted
        self.mc_tmplts = mc_tmplts

        def fit_func(x, par):
            value = 0.
            for i, hist in enumerate(templates):
                value += par[i] * hist.GetBinContent(hist.FindBin(x[0]))
            return value

        self.fit_func = TF1(
            "MyFitFunc",
            fit_func,
            x_min,
            x_max,
            size
        )
        for i in xrange(0, size):
            self.fit_func.SetParameter(i, 1.)

    def do_the_fit(self):
        self.fitted.histo.Fit(
            self.fit_func, "WL M N", "", self.x_min, self.x_max
        )

    def scale_templates_to_fit(self, templates):
        for i in range(0, len(templates)):
            templates[i].histo.Scale(self.fit_func.GetParameter(i))

    def get_val_err(self, i_par):
        return (
            self.fit_func.GetParameter(i_par),
            self.fit_func.GetParError(i_par)
        )

    def get_ndf(self):
        return self.fit_func.GetNDF()

    def make_fit_result(self, result_wrp, mc_tmplts):
        r = result_wrp
        r.Chi2 = gen.op.chi2(
            (
                gen.op.sum(mc_tmplts),
                self.fitted
            ), self.x_min, self.x_max
        ).float
        r.NDF = self.get_ndf()
        r.FitProb = TMath.Prob(r.Chi2, r.NDF)
        r.dataIntegral = self.fitted.histo.Integral()
        r.legend = []
        r.value = []
        r.error = []
        r.binIntegralMC = []
        r.binIntegralScaled = []
        r.binIntegralScaledError = []
        for i, tmplt in enumerate(mc_tmplts):
            r.legend.append(tmplt.legend)
            val, err = self.get_val_err(i)
            r.value.append(val)
            r.error.append(err)
            r.binIntegralMC.append(tmplt.histo.Integral() / r.value[-1])
            r.binIntegralScaled.append(tmplt.histo.Integral())
            r.binIntegralScaledError.append(
                r.binIntegralScaled[-1] * r.error[-1] / r.value[-1]
            )
            if "real" in tmplt.legend:
                r.mc_real_photon_ttgamma  = tmplt.sub_tot_list[0]
                r.mc_real_photon_total    = tmplt.sub_tot_list[1]
                r.pur_ttgam = r.mc_real_photon_ttgamma / r.mc_real_photon_total
                r.n_sig             = r.binIntegralScaled[-1]
                r.n_sig_err         = r.binIntegralScaledError[-1]
                r.n_sig_ttgam       = r.n_sig * r.pur_ttgam
                r.n_sig_ttgam_err   = r.n_sig_err * r.pur_ttgam


class FractionFitter(Fitter):
    def __init__(self):
        super(FractionFitter, self).__init__()
        self.vals = []
        self.errs = []

    def build_fit_function(self, fitted, mc_tmplts, x_min, x_max):
        self.fitted = fitted
        self.mc_tmplts = mc_tmplts
        mc_array = TObjArray(len(mc_tmplts))
        for tmplt in mc_tmplts:
            mc_array.Add(tmplt.histo)
        self.fit_func = TFractionFitter(fitted.histo, mc_array)

    def do_the_fit(self):
        self.fit_func.Fit()

    def scale_templates_to_fit(self, templates):
        val = Double(0.)
        err = Double(0.)
        for i, tmplt in enumerate(templates):
            self.fit_func.GetResult(i, val, err)
            orig_frac = tmplt.histo.Integral() / self.fitted.histo.Integral()
            self.vals.append(val / orig_frac)
            self.errs.append(err / orig_frac)
            templates[i].histo.Scale(self.vals[-1])

    def get_val_err(self, i_par):
        return self.vals[i_par], self.errs[i_par]


class ThetaFitter(Fitter):
    def __init__(self):
        super(ThetaFitter, self).__init__()
        self.model = None
        self.fit_res = None
        self.ndf = 0
        self.sig_val = None
        self.sig_err = None
        self.bkg_val = None
        self.bkg_err = None

    def _store_histos_for_theta(self, wrp):
        filename = os.path.join(settings.dir_result, wrp.name + ".root")
        f = TFile.Open(filename, "RECREATE")
        f.cd()
        for key, value in wrp.__dict__.iteritems():
            if isinstance(value, TH1):
                value.SetName(key)
                value.Write()
        f.Close()

    def build_fit_function(self, fitted, mc_tmplts, x_min, x_max):
        self.x_min, self.x_max = x_min, x_max
        self.fitted = fitted
        self.mc_tmplts = mc_tmplts

        theta_root_wrp = wrp.Wrapper(
            name="ThetaHistos",
            chhadiso__DATA=fitted.histo,
            chhadiso__real=mc_tmplts[1].histo,
            chhadiso__fake=mc_tmplts[0].histo,
        )
        self._store_histos_for_theta(theta_root_wrp)
        theta_auto.config.workdir = settings.dir_result
        self.model = theta_auto.build_model_from_rootfile(
            os.path.join(settings.dir_result, "ThetaHistos.root"),
            include_mc_uncertainties=True
        )
        self.model.set_signal_processes(["real"])
        self.model.add_lognormal_uncertainty("fake_rate", 1., "fake")
        self.model.distribution.set_distribution_parameters(
            'fake_rate',
            width=theta_auto.inf
        )
        self.ndf = fitted.histo.GetNbinsX() - 2

    def do_the_fit(self):
        self.fit_res = theta_auto.mle(self.model, "data", 1, chi2=True)
        print self.fit_res

    def scale_templates_to_fit(self, templates):
        par_values = {
            "beta_signal":self.fit_res["real"]["beta_signal"][0][0],
            "fake_rate":self.fit_res["real"]["fake_rate"][0][0]
        }
        self.bkg_val = self.model.get_coeff("chhadiso", "fake").get_value(par_values)
        self.bkg_err = abs(self.bkg_val * self.fit_res["real"]["fake_rate"][0][1] / self.fit_res["real"]["fake_rate"][0][0])
        self.sig_val = self.fit_res["real"]["beta_signal"][0][0]
        self.sig_err = abs(self.fit_res["real"]["beta_signal"][0][1])
        templates[1].histo.Scale(self.sig_val)
        templates[0].histo.Scale(self.bkg_val)

    def get_val_err(self, i_par):
        if i_par == 1:
            return self.sig_val, self.sig_err
        elif i_par == 0:
            return self.bkg_val, self.bkg_err

    def get_ndf(self):
        return self.ndf


class CombineFitter(Fitter):
    def __init__(self):
        super(CombineFitter, self).__init__()

    def build_fit_function(self, fitted, mc_tmplts, x_min, x_max):
        combine_cfg = [

        ]
        # save histos to root file
        combine_root_wrp = wrp.Wrapper(
            name="CombineHistos",
            data_obs=fitted.histo,
            signal=mc_tmplts[1].histo,
            background=mc_tmplts[0].histo,
            n_data_obs=fitted.histo.Integral(),
            n_signal=mc_tmplts[1].histo.Integral(),
            n_background=mc_tmplts[0].histo.Integral(),
        )
        diskio.write(combine_root_wrp)
        raise Exception("STOP!")

    def do_the_fit(self):
        # exec theta_auto inline
        pass

    def scale_templates_to_fit(self, templates):
        # just scale...
        pass

    def get_val_err(self, i_par):
        pass

    def get_ndf(self):
        pass


class TemplateFitTool(ppt.FSStackPlotter):
    def __init__(self, name = None):
        super(TemplateFitTool, self).__init__(name)
        self.mc_tmplts      = None
        self.fitted         = None
        self.fitbox_bounds  = None
        self.result         = wrp.Wrapper()
        self.n_templates    = 0
        self.fitter         = Fitter()
        self.x_min          = 0.
        self.x_max          = 0.
        #self.canvas_decorators
        def fix_ratio_histo_name(cnvs):
            for c in cnvs:
                d = c.get_decorator(rnd.BottomPlotRatioSplitErr)
                d.dec_par["y_title"] = "Fit residual"
                yield c
        def set_no_exp(cnvs):
            for c in cnvs:
                c.first_drawn.GetYaxis().SetNoExponent()
                c.bottom_hist.GetYaxis().SetTitleSize(0.14)
                c.canvas.Modified()
                c.canvas.Update()
                yield c
        self.hook_pre_canvas_build = fix_ratio_histo_name
        self.hook_post_canvas_build = set_no_exp

    def configure(self):
        super(TemplateFitTool, self).configure()
        self.canvas_decorators.append(com.LumiTitleBox)
        self.save_name_lambda = lambda wrp: self.plot_output_dir + wrp.name.split("_")[1]

    def fetch_mc_templates(self):
        mc_tmplts = histo_wrapperize(self.mc_tmplts)
        return list(cosmetica2(mc_tmplts))

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
        textbox.SetTextSize(settings.box_text_size)

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
        self.result.fitter = self.fitter.__class__.__name__
        mc_tmplts = self.fetch_mc_templates()
        self.n_templates = len(mc_tmplts)
        settings.post_proc_dict[self.name+"_mc_tmplts"] = mc_tmplts[:]

        # do fit procedure
        self.fitted = gen.op.sum(self.fitted)
        self.x_min, self.x_max = find_x_range(self.fitted.histo)
        self.fitter.build_fit_function(
            self.fitted, mc_tmplts, self.x_min, self.x_max
        )
        self.fitter.do_the_fit()

        self.fitter.scale_templates_to_fit(mc_tmplts)
        self.fitter.make_fit_result(self.result, mc_tmplts)

        fit_textbox = self.make_fit_textbox()
        textboxes = {mc_tmplts[0].name: fit_textbox}
        self.canvas_decorators.append(
            rnd.TextBoxDecorator(None, True, textbox_dict=textboxes)
        )

        tmplt_stacks = [gen.op.stack(mc_tmplts)]
        stream_stack = [(tmplt_stacks[0], self.fitted)]
        self.stream_stack = gen.pool_store_items(stream_stack)

        del self.fitter

class TemplateFitToolSihih(TemplateFitTool):
    def configure(self):
        super(TemplateFitToolSihih, self).configure()
#        self.fitter = FractionFitter()
        self.fitbox_bounds  = 0.63, 0.93, 0.60
        self.mc_tmplts      = gen.filter(
            settings.post_proc_dict["TemplateStacks"], {
            "analyzer"  : ("TemplateSihihreal", "TemplateSihihfake"),
        })
        self.fitted         = gen.fs_filter_active_sort_load({
            "analyzer"  : "TemplateSihih",
            "is_data"   : True,
        })


class TemplateFitToolChHadIso(TemplateFitTool):
    def configure(self):
        super(TemplateFitToolChHadIso, self).configure()
        self.fitter = Fitter()
        self.fitbox_bounds = 0.33, 0.62, settings.defaults_Legend["y_pos"]

        # here the stacked templates are taken for purity calculation
        # but they are replaced in fetch_mc_templates(..)
        self.mc_tmplts      = gen.filter(
            settings.post_proc_dict["TemplateStacks"], {
            "analyzer"  : ("TemplateChHadIsoreal", "TemplateChHadIsofake"),
        })
        self.fitted         = rebin_chhadiso(
            gen.fs_filter_active_sort_load({
                "analyzer"  : "TemplateChHadIso",
                "is_data"   : True,
            })
        )
        ttbar_sample = next((
            s.name
            for s in settings.mc_samples().values()
            if s.legend == "t#bar{t} inclusive"
        ))
        self.gen_bkg_tmplt = rebin_chhadiso(
            gen.gen_norm_to_data_lumi(
                gen.fs_filter_active_sort_load({
                    "analyzer"  : "TemplateChHadIsofake",
                    "sample"    : ttbar_sample,
                })))
        self.gen_sig_tmplt = rebin_chhadiso(
            gen.gen_norm_to_data_lumi(
                gen.fs_filter_active_sort_load({
                    "analyzer"  : "TemplateChHadIsoreal",
                    "sample"    : re.compile("whiz2to5"),
                })))

    def fetch_mc_templates(self):
        # mix in tt(gam) only templates
        tmplts = super(TemplateFitToolChHadIso, self).fetch_mc_templates()
        sig = next(self.gen_sig_tmplt)
        bkg = next(self.gen_bkg_tmplt)
        tmplts[1].__dict__.update(sig.__dict__)
        tmplts[0].__dict__.update(bkg.__dict__)
        tmplts[0].is_data = False
        return list(cosmetica2(tmplts))


sb_anzlrs = (
    "PlotLooseIDSliceSihihSB12to13",
    "PlotLooseIDSliceSihihSB13to14",
    "PlotLooseIDSliceSihihSB14to15",
    "PlotLooseIDSliceSihihSB15to16",
    "PlotLooseIDSliceSihihSB16to17",
    "PlotLooseIDSliceSihihSB17to18",
#    "PlotLooseIDSliceSihihSB18to19",
#    "PlotLooseIDSliceSihihSB19to20",
)
def get_merged_sbbkg_histo(sample):
    wrps = rebin_chhadiso(gen.fs_filter_sort_load({
        "analyzer": sb_anzlrs,
        "sample": sample,
    }))
    return gen.op.merge(wrps)


class TemplateFitToolChHadIsoSbBkgInputBkgWeight(ppc.PostProcTool):
    def run(self):
            top_sample = next(s for s in settings.active_samples if s[:2] == "TT")
            wrp_fake = next(rebin_chhadiso(gen.fs_filter_sort_load({
                "analyzer": "TemplateChHadIsofake",
                "sample":   top_sample,#"TTMadG",
            })))
            wrp_sb = gen.op.merge(rebin_chhadiso(gen.fs_filter_sort_load({
                "analyzer": sb_anzlrs,
                "sample": top_sample,#"TTMadG",
            })))
            wrp = gen.op.div((
                gen.op.norm_to_integral(wrp_fake),
                gen.op.norm_to_integral(wrp_sb),
            ))
            wrp.lumi = 1.
            wrp.draw_option = "E1"
            self.result = wrp
            cnvs = list(gen.canvas(((wrp,),)),)
            cnvs[0].canvas.SetGridy(1)
            gen.consume_n_count(
                gen.save(
                    gen.canvas(((wrp,),)),
                    lambda c: self.plot_output_dir + c.name
                )
            )
            del wrp.draw_option


class TemplateFitToolChHadIsoSbBkgInputBkg(ppc.PostProcTool):
    def run(self):
        wrp = next(rebin_chhadiso(
            gen.gen_sum(
                [
                    gen.fs_filter_active_sort_load({
                        "analyzer"  : sb_anzlrs,
                        "is_data"   : True
                    })
                ]
            )
        ))
        # multiply with weight
        if do_dist_reweighting:
            wrp = gen.op.prod((
                settings.post_proc_dict["TemplateFitToolChHadIsoSbBkgInputBkgWeight"],
                wrp,
            ))
        wrp.lumi = settings.data_lumi_sum()

        self.result = [wrp]
        gen.consume_n_count(
            gen.save(
                gen.canvas((self.result,)),
                lambda c: self.plot_output_dir + c.name
            )
        )


class TemplateFitToolChHadIsoSbBkg(TemplateFitToolChHadIso):
    def configure(self):
        super(TemplateFitToolChHadIso, self).configure()
        self.fitter = ThetaFitter()
        self.fitbox_bounds  = 0.33, 0.62, 0.88

        self.mc_tmplts      = gen.filter(
            settings.post_proc_dict["TemplateStacks"], {
                "analyzer"  : ("TemplateChHadIsoreal", "PlotLooseIDSihihSBfake"),
                })
        self.fitted         = rebin_chhadiso(
            gen.fs_filter_active_sort_load({
                "analyzer"  : "TemplateChHadIso",
                "is_data"   : True,
                })
        )

        self.gen_bkg_tmplt = iter(settings.post_proc_dict["TemplateFitToolChHadIsoSbBkgInputBkg"])
        self.gen_sig_tmplt = rebin_chhadiso(
            gen.gen_norm_to_data_lumi(
                gen.fs_filter_active_sort_load({
                    "analyzer"  : "TemplateChHadIsoreal",
                    "sample"    : re.compile("whiz2to5"),
                })))


class TemplateFitToolChHadIsoSBIDInputBkgWeight(ppc.PostProcTool):
    def run(self):
            top_sample = next(s for s in settings.active_samples if s[:2] == "TT")
            wrp_fake = next(rebin_chhadiso(gen.fs_filter_sort_load({
                "analyzer": "TemplateChHadIsofake",
                "sample":   top_sample,#"TTMadG",
            })))
            wrp_sb = gen.op.merge(rebin_chhadiso(gen.fs_filter_sort_load({
                "analyzer": "PlotSBID",
                "sample": top_sample,#"TTMadG",
            })))
            wrp = gen.op.div((
                gen.op.norm_to_integral(wrp_fake),
                gen.op.norm_to_integral(wrp_sb),
            ))
            wrp.lumi = 1.
            wrp.draw_option = "E1"
            self.result = wrp
            cnvs = list(gen.canvas(((wrp,),)),)
            cnvs[0].canvas.SetGridy(1)
            gen.consume_n_count(
                gen.save(
                    cnvs,
                    lambda c: self.plot_output_dir + c.name
                )
            )
            del wrp.draw_option


class TemplateFitToolChHadIsoSBIDInputBkg(ppc.PostProcTool):
    def run(self):
        wrp = next(rebin_chhadiso(
            gen.gen_sum(
                [gen.fs_filter_active_sort_load({
                    "analyzer"  : "PlotSBID",
                    "is_data"   : True
                })]
            )
        ))
        # normalize to mc expectation
        integral_fake = next(
            gen.gen_integral(
                gen.gen_norm_to_data_lumi(
                    gen.filter(
                        settings.post_proc_dict["TemplateStacks"],
                        {"analyzer": "TemplateChHadIsofake"}
                    )
                )
            )
        )
        print integral_fake
        wrp = gen.op.prod((
            gen.op.norm_to_integral(wrp),
            integral_fake
        ))

        # multiply with weight
        if do_dist_reweighting:
            wrp = gen.op.prod((
                settings.post_proc_dict["TemplateFitToolChHadIsoSBIDInputBkgWeight"],
                wrp,
            ))

        wrp.lumi = settings.data_lumi_sum()
        self.result = [wrp]
        gen.consume_n_count(
            gen.save(
                gen.canvas((self.result,)),
                lambda c: self.plot_output_dir + c.name
            )
        )


class TemplateFitToolChHadIsoSBID(TemplateFitToolChHadIso):
    def configure(self):
        super(TemplateFitToolChHadIso, self).configure()
        self.fitter = ThetaFitter()
        self.fitbox_bounds  = 0.33, 0.62, 0.88

        self.mc_tmplts      = gen.filter(
            settings.post_proc_dict["TemplateStacks"], {
                "analyzer"  : ("TemplateChHadIsoreal", "PlotSBIDfake"),
            }
        )
        self.fitted         = rebin_chhadiso(
            gen.fs_filter_active_sort_load({
                "analyzer"  : "TemplateChHadIso",
                "is_data"   : True,
            })
        )

        self.gen_bkg_tmplt = iter(
            settings.post_proc_dict["TemplateFitToolChHadIsoSBIDInputBkg"]
        )
        self.gen_sig_tmplt = rebin_chhadiso(
            gen.gen_norm_to_data_lumi(
                gen.fs_filter_active_sort_load({
                    "analyzer"  : "TemplateChHadIsoreal",
                    "sample"    : re.compile("whiz2to5"),
                })
            )
        )


class TemplateFitToolSihihShift(TemplateFitTool):
    num_pat = re.compile(r".*(\d{4})")

    def configure(self):
        super(TemplateFitToolSihihShift, self).configure()
        self.fitbox_bounds  = 0.63, 0.93, 0.60
        self.mc_tmplts      = settings.post_proc_dict["mc_templates_sihih_shift"]
        self.fitted         = gen.fs_filter_active_sort_load({
            "analyzer"  : "TemplateSihih",
            "is_data"   : True,
        })

    def build_fit_function(self, mc_tmplts):

        grouped = itertools.groupby(
            mc_tmplts,
            lambda w: self.num_pat.match(w.analyzer).groups()[0]
        )
        templates = [list(w for w in grp[1]) for grp in grouped]
        n_shifted = len(templates)
        n_tmplts  = len(templates[0])
        self.template_matrix = templates
        self.n_shifted  = n_shifted
        self.n_tmplts   = n_tmplts
        first_histo = templates[0][0].histo

        def fit_func(x, par):
            value = 0.
            shift = par[n_tmplts]  # shift is last param
            shift = min(n_shifted-3, shift)
            shift = max(0, shift)
            i_shift = int(shift)
            rest = shift - i_shift
            bin_number = first_histo.FindBin(x[0])
            for i,p in enumerate(par):
                par[i] = max(1., p)
            for i in xrange(n_tmplts):
                lower = templates[i_shift  ][i].histo.GetBinContent(bin_number)
                upper = templates[i_shift+1][i].histo.GetBinContent(bin_number)
                val = (1 - rest) * lower + rest * upper
                value += par[i] * val
            return value

        tf1 = TF1(
            "MyShiftFitFunc",
            fit_func,
            self.x_min,
            self.x_max,
            n_tmplts + 1
        )
        for i in xrange(0, n_tmplts + 1):
            tf1.SetParameter(i,1.)
        #tf1.FixParameter(n_tmplts, 50.)

        return tf1

    def do_the_fit(self, mc_tmplts):
        super(TemplateFitToolSihihShift, self).do_the_fit(mc_tmplts)
        shift = self.fit_func.GetParameter(self.n_tmplts) # shift is last param
        picked_num = int(min(self.n_shifted-2,max(0., round(shift))))
        del mc_tmplts[:]
        for i in range(self.n_tmplts):
            tmplt = self.template_matrix[picked_num][i]
            tmplt.analyzer = re.sub(r"[0-9]+", "", tmplt.analyzer) # remove number
            mc_tmplts.append(self.template_matrix[picked_num][i])
        settings.post_proc_dict[self.name+"_mc_tmplts"] = mc_tmplts[:]

    def make_fit_results(self, mc_tmplts, chi2):
        super(TemplateFitToolSihihShift, self).make_fit_results(mc_tmplts, chi2)
        res = self.result
        val = self.fit_func.GetParameter(self.n_tmplts)
        err = self.fit_func.GetParError(self.n_tmplts)
        res.shift_val = val*0.00002 - 0.001     ## scaling to shift in sihih
        res.shift_err = err*0.00002             ## scaling to shift in sihih

    def make_fit_textbox(self):
        box = super(TemplateFitToolSihihShift, self).make_fit_textbox()
        box.AddText(
            "#delta = (%.3f #pm %.3f)#upoint 10^{-4}" % (
                self.result.shift_val*10000,
                self.result.shift_err*10000
            )
        )
        return box


class TemplateFitToolSihihShiftSepFakes(TemplateFitToolSihihShift):
    def configure(self):
        super(TemplateFitToolSihihShiftSepFakes, self).configure()
        mc_tmplts = settings.post_proc_dict["mc_templates_sihih_shift_sep_fakes"]

        # interleave the non shifted fakeOther template for fitting
        fake_other = mc_tmplts.pop(-1)
        grouped = itertools.groupby(
            mc_tmplts,
            lambda w: self.num_pat.match(w.analyzer).groups()[0]
        )
        def gen_interleave(grps):
            for g in grps:
                g = iter(g[1])
                w = g.next()
                f = copy.copy(fake_other)
                f.analyzer = re.sub("Gamma", "Other", w.analyzer)
                yield f
                yield w
                yield g.next()
        self.mc_tmplts = gen_interleave(grouped)


### plot templates overlayed ##############################
class TemplateOverlays(ppt.FSStackPlotter):
    def __init__(self, name=None):
        super(TemplateOverlays, self).__init__(name)
        self.canvas_decorators = self.canvas_decorators[1:]
        self.canvas_decorators.append(com.SimpleTitleBox)
        self.norm_func = lambda g: (w for w in g)

    def set_up_stacking(self):
        key_func = lambda w: w.post_proc_key
        mc_tmplts = itertools.chain(*list(
            gen.get_from_post_proc_dict(k)
            for k in settings.post_proc_dict.keys()
            if ("_mc_tmplts" in k
            )
        ))
        mc_tmplts = self.norm_func(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        def histo_namer(wrp):
            wrp.analyzer = wrp.post_proc_key[:-10]
            return wrp
        mc_tmplts = (histo_namer(w) for w in mc_tmplts)
        mc_tmplts = sorted(mc_tmplts, key=key_func)
        mc_tmplts = gen.group(mc_tmplts, key_func=key_func)
        self.stream_stack = mc_tmplts


class TemplateOverlaysNormIntegral(TemplateOverlays):
    def __init__(self, name=None):
        super(TemplateOverlaysNormIntegral, self).__init__(name)
        self.norm_func = gen.gen_norm_to_integral


class TemplateOverlaysNormLumi(TemplateOverlays):
    def __init__(self, name=None):
        super(TemplateOverlaysNormLumi, self).__init__(name)
        self.norm_func = gen.gen_norm_to_lumi


class SideBandOverlay(TemplateOverlays):
    def set_up_stacking(self):
        key_func = lambda w: w.analyzer[:-4]
        mc_tmplts = itertools.chain(*list(
            gen.get_from_post_proc_dict(k)
                for k in settings.post_proc_dict.keys()
                if ("TemplateStacks" in k
                )
        ))
        mc_tmplts = histo_wrapperize(mc_tmplts)
        mc_tmplts = gen.gen_norm_to_lumi(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        mc_tmplts = sorted(mc_tmplts, key=key_func)
        mc_tmplts = gen.group(mc_tmplts, key_func=key_func)
        self.stream_stack = mc_tmplts


TemplateFitTools = ppc.PostProcChain(
    "TemplateFitTools",
    [
        TemplateStacks,
#        TemplateFitToolSihih,
#        TemplateFitToolSihihShift,
#        TemplateFitToolSihihShiftSepFakes,
        TemplateFitToolChHadIso,
        TemplateFitToolChHadIsoSbBkgInputBkgWeight,
        TemplateFitToolChHadIsoSbBkgInputBkg,
        TemplateFitToolChHadIsoSbBkg,
        TemplateFitToolChHadIsoSBIDInputBkgWeight,
        TemplateFitToolChHadIsoSBIDInputBkg,
        TemplateFitToolChHadIsoSBID,
        TemplateOverlaysNormLumi,
        TemplateOverlaysNormIntegral,
        SideBandOverlay,
    ]
)


def apply_overlay_draw_mode(wrps):

    def style_boxed_errors(w):
        w.draw_option = "E2"
        w.histo.SetFillColor(922)
        w.histo.SetFillStyle(3008)
        w.histo.SetLineWidth(0)

    def style_error_bars(w):
        w.draw_option = "E1"

    for w in wrps:
        w.histo.SetMarkerSize(0)
        if "TemplateChHadIsofake" in w.analyzer:
            style_boxed_errors(w)
        else:
            style_error_bars(w)
        yield w


class SideBandVSFake(TemplateOverlays):
    def set_up_stacking(self):
        mc_tmplts = gen.fs_filter_sort_load({
            "sample"    : self.sample_name,
            "analyzer"  : ("TemplateChHadIsofake", "PlotSBID")
        })
        sb_wrp = get_merged_sbbkg_histo(self.sample_name)
        mc_tmplts = [sb_wrp] + list(mc_tmplts)
        mc_tmplts = gen.gen_norm_to_integral(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        mc_tmplts = rebin_chhadiso(mc_tmplts)
        mc_tmplts = gen.apply_histo_linecolor(mc_tmplts, [625, 618, 596])
        mc_tmplts = apply_overlay_draw_mode(mc_tmplts)
        mc_tmplts = gen.group(mc_tmplts, key_func=lambda w: w.sample)
        self.stream_stack = mc_tmplts


def make_SideBandVSFake(samplename):
    tool = SideBandVSFake("SideBandVSFake" + samplename)
    tool.sample_name = samplename
    return tool


class SigRegCmp(TemplateOverlays):
    def set_up_stacking(self):
        mc_tmplts = gen.fs_filter_sort_load({
            "sample"    : ("whiz2to5", "TTGamRD1"),
            "analyzer"  : "TemplateChHadIsoreal",
            })
        mc_tmplts = gen.gen_norm_to_integral(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        def leg(wrps):
            for w in wrps:
                w.legend = w.sample
                w.draw_option = "E1"
                w.histo.SetMarkerStyle(24)
                yield w
        mc_tmplts = leg(mc_tmplts)
        mc_tmplts = rebin_chhadiso(mc_tmplts)
        mc_tmplts = gen.apply_histo_linecolor(mc_tmplts, [409, 625, 618, 596, 430])
        mc_tmplts = gen.group(mc_tmplts, key_func=lambda w: w.analyzer)
        self.stream_stack = mc_tmplts


class SihihSidebandSlices(TemplateOverlays):
    def set_up_stacking(self):
        def sum_up_two(wrps):
            while True:
                try:
                    h = gen.op.sum((next(wrps), next(wrps)))
                except StopIteration:
                    return
                yield h
        mc_tmplts = list(sum_up_two(gen.fs_filter_sort_load({
            "sample"    : self.sample_name,
            "analyzer"  : re.compile("PlotLooseIDSliceSihihSB"),
            })))
        mc_tmplts = itertools.chain(gen.fs_filter_sort_load({
            "sample"    : self.sample_name,
            "analyzer"  : "TemplateChHadIsofake",
            }),
            mc_tmplts
        )
        mc_tmplts = gen.gen_norm_to_integral(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        mc_tmplts = rebin_chhadiso(mc_tmplts)
        mc_tmplts = gen.apply_histo_linecolor(mc_tmplts, [409, 625, 618, 596, 430])
        mc_tmplts = gen.group(mc_tmplts, key_func=lambda w: w.sample)
        self.stream_stack = mc_tmplts

def make_SihihSidebandSlices(samplename):
    tool = SihihSidebandSlices("SihihSidebandSlices" + samplename)
    tool.sample_name = samplename
    return tool


class SihihSidebandVarSlices(TemplateOverlays):
    def set_up_stacking(self):
        mc_tmplts = self.__dict__["input_func"]()
        mc_tmplts = gen.gen_norm_to_integral(mc_tmplts)
        mc_tmplts = cosmetica1(mc_tmplts)
        mc_tmplts = rebin_chhadiso(mc_tmplts)
        mc_tmplts = gen.apply_histo_linecolor(mc_tmplts, [409, 625, 618, 596, 430])
        mc_tmplts = gen.group(mc_tmplts, key_func=lambda w: w.sample)
        self.stream_stack = mc_tmplts


def make_SihihSidebandVarSlices(samplename, input_func):
    tool = SihihSidebandSlices("SihihSidebandSlices" + samplename)
    tool.sample_name = samplename
    tool.input_func = input_func
    return tool


tt_sample_names = ["TTPoPy", "TTJeRD1", "TTMCNLO", "TTPoHe", "TTMadG"]
TemplateFitPlots = ppc.PostProcChain(
    "TemplateFitPlots",
    [
        SigRegCmp,
    ]
    + list(make_SideBandVSFake(s) for s in tt_sample_names)
    + list(make_SihihSidebandSlices(s) for s in tt_sample_names)
)
