
import itertools
import cmstoolsac3b.rendering as rnd
import cmstoolsac3b.generators as gen
import cmstoolsac3b.operations as op
import cmstoolsac3b.wrappers as wrp
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.postproctools as ppt
import plots_template_fit as tmpl_fit
from cmstoolsac3b import settings
from ROOT import TH1D, TVectorD

top_sample = next(s for s in settings.active_samples if s[:2] == "TT")
dicts_sample_MC = [
    {
        "sample"    : top_sample,
        "analyzer"  : "TemplateChHadIsofake",
    },
    {
        "sample"    : "whiz2to5",
        "analyzer"  : "TemplateChHadIsoreal",
    },
]
dicts_sample_altMC = [
    {
        "sample"    : "TTJeRD1",
        "analyzer"  : "TemplateChHadIsofake",
    },
    {
        "sample"    : "TTGamRD1",
        "analyzer"  : "TemplateChHadIsoreal",
    },
]



def make_fitter_class(base_class):
    class Fitter(base_class):
        def __init__(self, name=None, *args):
            super(Fitter, self).__init__(name)
            if args:
                self.mixer          = args[0]
                self.scale_factors  = args[1]

        def configure(self):
            super(Fitter, self).configure()
            self.fitted = self.mixer.make_mixed_histo(self.scale_factors)

    return Fitter


def make_input_maker_sbbkg(sample):
    class TemplateFitToolChHadIsoSbBkgInputBkg(ppc.PostProcTool):
        def run(self):
            wrp = tmpl_fit.get_merged_sbbkg_histo(sample)

            # multiply with weight
            if tmpl_fit.do_dist_reweighting:
                wrp = gen.op.prod((
                    settings.post_proc_dict["TemplateFitToolChHadIsoSbBkgInputBkgWeight"],
                    wrp,
                ))

            wrps = gen.gen_norm_to_data_lumi((wrp,))
            wrps = list(wrps)
            self.result = wrps
            gen.consume_n_count(
                gen.save(
                    gen.canvas((wrps,)),
                    lambda c: self.plot_output_dir + c.name
                )
            )
    return TemplateFitToolChHadIsoSbBkgInputBkg


def make_input_maker_sbid(sample):
    class TemplateFitToolChHadIsoSBIDInputBkg(ppc.PostProcTool):
        def run(self):
            wrps = tmpl_fit.rebin_chhadiso(gen.fs_filter_sort_load({
                "analyzer": "PlotSBID",
                "sample": sample,
            }))
            wrp = gen.op.merge(wrps)

            # multiply with weight
            if tmpl_fit.do_dist_reweighting:
                wrp = gen.op.prod((
                    settings.post_proc_dict["TemplateFitToolChHadIsoSBIDInputBkgWeight"],
                    wrp,
                ))

            wrps = gen.gen_norm_to_data_lumi((wrp,))
            wrps = list(wrps)
            self.result = wrps
            gen.consume_n_count(
                gen.save(
                    gen.canvas((wrps,)),
                    lambda c: self.plot_output_dir + c.name
                )
            )
    return TemplateFitToolChHadIsoSBIDInputBkg

def make_input_maker_randcone(sample):
    class TemplateFitToolRandConeIsoInputSig(ppc.PostProcTool):
        def run(self):
            wrps = tmpl_fit.rebin_chhadiso(gen.fs_filter_sort_load({
                "analyzer": "TemplateRandConereal",
                "sample": sample,
            }))
            wrp = gen.op.merge(wrps)

            # multiply with weight
            if tmpl_fit.do_dist_reweighting:
                wrp = gen.op.prod((
                    settings.post_proc_dict["TemplateFitToolRandConeIsoInputSigWeight"],
                    wrp,
                ))

            wrps = gen.gen_norm_to_data_lumi((wrp,))
            wrps = list(wrps)
            self.result = wrps
            gen.consume_n_count(
                gen.save(
                    gen.canvas((wrps,)),
                    lambda c: self.plot_output_dir + c.name
                )
            )
    return TemplateFitToolRandConeIsoInputSig



def gen_mixer_input(input_dict):
        for d in input_dict:
            yield   op.norm_to_integral(
                    op.merge(
                    list(
                    gen.load(
                    gen.filter(
                    gen.fs_content(),
                    d
                    )))))


def make_mixer_class(input_dict):
    gen_tmplt_input = tmpl_fit.rebin_chhadiso(gen_mixer_input(input_dict))
    class HistoMixer(ppt.FSStackPlotter):
        def configure(self):
            self.result = []
            for d in gen_tmplt_input:
                self.result.append(d)

        def make_mixed_histo(self, scale_factors):
            assert(len(scale_factors) == len(self.result))
            mix = op.sum((
                op.prod([tmplt, wrp.FloatWrapper(float(scale))])
                for scale,tmplt in itertools.izip(scale_factors, self.result)
            ))
            mix.legend      = "mix:"+(len(scale_factors)*" %d") % tuple(scale_factors)
            mix.name        = "pseudo data"
            mix.draw_option = "E1X0"
            mix.draw_option_legend = "p"
            #mix.draw_option_legend = ""
            mix.histo.SetMarkerStyle(24)
            return [mix]

        def set_up_stacking(self):
            gen_inp = lambda w: tmpl_fit.cosmetica1([op.norm_to_integral(w)])  # clone histo and color..
            self.stream_stack = (
                gen_inp(w) for w in self.result
            )
    return HistoMixer


class TemplateFitClosureEvaluation(ppc.PostProcTool):
    def __init__(self, name=None, fitters=None):
        super(TemplateFitClosureEvaluation, self).__init__(name)
        if not hasattr(self, "fitters"):
            self.fitters = fitters[:]
        self.plot_chi2      = None
        self.plot_n_real    = None
        self.plot_n_fake    = None

    def configure(self):
        pass

    def make_chi2_plot(self):
        histo = TH1D(
            "tmpltFitClosureChi2",
            ";template fit number;#chi^2",
            len(self.fitters),
            0.5,
            0.5 + len(self.fitters)
        )
        histo.SetMarkerStyle(4)
        for i, ft in enumerate(self.fitters):
            histo.SetBinContent(i, ft.result.Chi2)
            histo.SetBinError(i, 0.)
        self.plot_chi2 = wrp.HistoWrapper(
            histo,
            draw_option = "E1X0",
            draw_option_legend = " ",
            legend = "(NDF = %d)"%self.fitters[0].result.NDF
        )

    def make_fit_num_plot(self):
        n_fitters = len(self.fitters)
        self.plots_truth_vs_fitted = []
        self.plots_diffs = []
        for i_sf in range(len(self.fitters[0].scale_factors)):
            truth = TH1D(
                "tmpltFitClosureTruth%d"%i_sf,
                ";template fit number;number of photons",
                n_fitters, 0.5, 0.5 + n_fitters
            )
            truth.SetMarkerStyle(5)
            fitted = TH1D(
                "tmpltFitClosureFitted%d"%i_sf,
                ";template fit number;number of photons",
                n_fitters, 0.5, 0.5 + n_fitters
            )
            pull = TH1D(
                "PullDist%d"%i_sf,
                ";(MC truth minus fit result)/(fit result error);number of fit results",
                60, -3., 3.
            )
            fitted.SetMarkerStyle(4)

            for i_ft, ft in enumerate(self.fitters):
                sf      = ft.scale_factors[i_sf]
                fit_val = ft.result.binIntegralScaled[i_sf]
                fit_err = ft.result.binIntegralScaledError[i_sf]
                truth.SetBinContent(i_ft, sf)
                truth.SetBinError(i_ft, 0.)
                fitted.SetBinContent(i_ft, fit_val)
                fitted.SetBinError(i_ft, fit_err)
                pull.Fill((sf - fit_val)/fit_err)

            self.plots_truth_vs_fitted.append((
                wrp.HistoWrapper(
                    truth,
                    draw_option = "E1X0",
                    draw_option_legend = "f",
                    legend = "MC truth ("+self.fitters[0].result.legend[i_sf]+")",
                ),
                wrp.HistoWrapper(
                    fitted,
                    draw_option = "E1X0",
                    draw_option_legend = "p",
                    legend = "Fitted ("+self.fitters[0].result.legend[i_sf]+")",
                ),
            ))
            self.plots_diffs.append(
                wrp.HistoWrapper(
                    pull,
                    legend = " "
                )
            )

    def store_results(self):
        cnv = itertools.chain(
            gen.canvas(
                [self.plot_chi2] + self.plots_truth_vs_fitted,
                [rnd.Legend(None, True, y_pos=0.25)]
            ),
            gen.canvas(self.plots_diffs)
        )
        cnv = gen.save(cnv, lambda c: self.plot_output_dir + c.name)
        gen.consume_n_count(cnv)

    def store_sys_err_result(self):
        self.result = []
        for i_sf in range(len(self.fitters[0].scale_factors)):
            truth   = self.plots_truth_vs_fitted[i_sf][0].histo
            fitted  = self.plots_truth_vs_fitted[i_sf][1].histo
            bin = truth.GetNbinsX() / 2
            central_val = truth.GetBinContent(bin) 
            total_dev = central_val - fitted.GetBinContent(bin)
            sys_dev = total_dev / central_val
            self.result.append(wrp.Wrapper(
                central_val=central_val,
                total_dev=total_dev,
                sys_dev=sys_dev
            ))

    def run(self):
        self.configure()
        self.make_chi2_plot()
        self.make_fit_num_plot()
        self.store_results()
        self.store_sys_err_result()


def make_sequence(name, histo_mixer, nth_histo, range_func, center_values, fitter):
    tools           = []
    for n in range_func:
        values = center_values[:]
        values[nth_histo] = n
        full_name = "ClosureTestFitter_"+name+(len(values)*"_%04d") % tuple(values)
        tools.append(
            make_fitter_class(fitter)(
                full_name,
                histo_mixer,
                values
            )
        )
    eval_tool = TemplateFitClosureEvaluation("Evaluator_"+name+"_%d"%nth_histo, tools)
    tools.append(eval_tool)
    return ppc.PostProcChain(
        "Sequence%d"%nth_histo,
        tools
    )


def make_closure_test_sequence_chhadiso_sbbkg(seq_name, input_dicts):
    histo_mixer = make_mixer_class(input_dicts)("MixerChHadIsoSbBkg")
    name = "ChHadIso"
    tools = [
        histo_mixer,
        make_input_maker_sbbkg(input_dicts[0]["sample"]),
        make_sequence(
            name, histo_mixer, 1,
            xrange(1200, 2900, 100), [4000, 2000],
            tmpl_fit.TemplateFitToolChHadIsoSbBkg
        ),
        make_sequence(
            name, histo_mixer, 0,
            xrange(2100, 6100, 200), [4000, 2000],
            tmpl_fit.TemplateFitToolChHadIsoSbBkg
        ),
    ]
    return ppc.PostProcChain(
        "TemplateFitClosureSequences" + seq_name,
        tools
    )


def make_closure_test_sequence_chhadiso_sbid(seq_name, input_dicts):
    histo_mixer = make_mixer_class(input_dicts)("MixerChHadIsoSBID")
    name = "ChHadIso"
    tools = [
        histo_mixer,
        make_input_maker_sbid(input_dicts[0]["sample"]),
        make_sequence(
            name, histo_mixer, 1,
            xrange(1200, 2900, 100), [4000, 2000],
            tmpl_fit.TemplateFitToolRandConeIso
        ),
        make_sequence(
            name, histo_mixer, 0,
            xrange(2100, 6100, 200), [4000, 2000],
            tmpl_fit.TemplateFitToolRandConeIso
        ),
    ]
    return ppc.PostProcChain(
        "TemplateFitClosureSequences" + seq_name,
        tools
    )

def make_closure_test_sequence_chhadiso_raco(seq_name, input_dicts):
    histo_mixer = make_mixer_class(input_dicts)("MixerChHadIsoSBID")
    name = "ChHadIso"
    tools = [
        histo_mixer,
        make_input_maker_sbid(input_dicts[0]["sample"]),
        make_input_maker_randcone(input_dicts[1]["sample"]),
        make_sequence(
            name, histo_mixer, 1,
            xrange(1200, 2900, 100), [4000, 2000],
            tmpl_fit.TemplateFitToolRandConeIso
        ),
        make_sequence(
            name, histo_mixer, 0,
            xrange(2100, 6100, 200), [4000, 2000],
            tmpl_fit.TemplateFitToolRandConeIso
        ),
    ]
    return ppc.PostProcChain(
        "TemplateFitClosureSequences" + seq_name,
        tools
    )


def make_seq_MC(central_maker):
    return central_maker("MC", dicts_sample_MC)


def make_seq_altMC(central_maker):
    return central_maker("altMC", dicts_sample_altMC)

seq_sbbkg_MC    = make_seq_MC(make_closure_test_sequence_chhadiso_sbbkg)
seq_sbbkg_altMC = make_seq_altMC(make_closure_test_sequence_chhadiso_sbbkg)
seq_sbid_MC     = make_seq_MC(make_closure_test_sequence_chhadiso_sbid)
seq_sbid_altMC  = make_seq_altMC(make_closure_test_sequence_chhadiso_sbid)
seq_raco_MC     = make_seq_MC(make_closure_test_sequence_chhadiso_raco)
seq_raco_altMC  = make_seq_altMC(make_closure_test_sequence_chhadiso_raco)


def make_sys_uncert_fitter(fitter_base_class):
    fitter_name = fitter_base_class.__name__
    class Fitter(fitter_base_class):
        def __init__(self, name=None, *args):
            super(Fitter, self).__init__(name)
            if args:
                self.mixer = args[0]

        def configure(self):
            super(Fitter, self).configure()
            res_data = settings.post_proc_dict[fitter_name]
            self.fitted = self.mixer.make_mixed_histo(res_data.binIntegralScaled)

    # make mixer and tool chain
    histo_mixer = make_mixer_class(dicts_sample_altMC)("Mixer"+fitter_name)
    if "SBID" in fitter_name:
        input_maker = make_input_maker_sbid(dicts_sample_altMC[0]["sample"])
    else:
        input_maker = make_input_maker_sbbkg(dicts_sample_altMC[0]["sample"])
    fitter = Fitter(fitter_name, histo_mixer)
    return ppc.PostProcChain(
        "SysFit" + fitter_name,
        [
            histo_mixer,
            input_maker,
            fitter
        ]
    )


def make_sys_uncert_fitter_raco(fitter_base_class):
    fitter_name = fitter_base_class.__name__
    class Fitter(fitter_base_class):
        def __init__(self, name=None, *args):
            super(Fitter, self).__init__(name)
            if args:
                self.mixer = args[0]

        def configure(self):
            super(Fitter, self).configure()
            res_data = settings.post_proc_dict[fitter_name]
            self.fitted = self.mixer.make_mixed_histo(res_data.binIntegralScaled)

    # make mixer and tool chain
    histo_mixer = make_mixer_class(dicts_sample_altMC)("Mixer"+fitter_name)
    input_maker_bkg = make_input_maker_sbid(dicts_sample_altMC[0]["sample"])
    input_maker_sig = make_input_maker_randcone(dicts_sample_altMC[1]["sample"])
    
    fitter = Fitter(fitter_name, histo_mixer)
    return ppc.PostProcChain(
        "SysFit" + fitter_name,
        [
            histo_mixer,
            input_maker_bkg,
	    input_maker_sig,
            fitter
        ]
    )


sys_fit_sbbkg = make_sys_uncert_fitter(tmpl_fit.TemplateFitToolChHadIsoSbBkg)
sys_fit_sbid = make_sys_uncert_fitter(tmpl_fit.TemplateFitToolChHadIsoSBID)
sys_fit_raco = make_sys_uncert_fitter_raco(tmpl_fit.TemplateFitToolRandConeIso)
#dicts_sihih_shift_sep_fakes = [
#    {
#        "sample"    : "TTGamRD1",
#        "analyzer"  : "TemplateSihihreal",
#        },
#    {
#        "sample"    : "TTJeRD1",
#        "analyzer"  : "TemplateSihihfakeGamma",
#        },
#    {
#        "sample"    : "TTJeRD1",
#        "analyzer"  : "TemplateSihihfakeOther",
#        },
#    ]
#
#def make_closure_test_sequence_sihih_shift_sep_fakes():
#    histo_mixer = make_mixer_class(
#        gen_mixer_input(
#            dicts_sihih_shift_sep_fakes
#        )
#    )("MixerSihihShiftSepFakes")
#    tools = [
#        histo_mixer,
#        make_sequence(
#            "SihihShiftSepFake", histo_mixer, 2, xrange(300,1050,50), [1000, 300, 700], tmpl_fit.TemplateFitToolSihihShiftSepFakes),
#        make_sequence(
#            "SihihShiftSepFake", histo_mixer, 1, xrange(100, 550,50), [1000, 300, 700], tmpl_fit.TemplateFitToolSihihShiftSepFakes),
#        make_sequence(
#            "SihihShiftSepFake", histo_mixer, 0, xrange(500,1550,50), [1000, 300, 700], tmpl_fit.TemplateFitToolSihihShiftSepFakes),
#        ]
#    return ppc.PostProcChain(
#        "TemplateFitClosureSequences",
#        tools
#    )
#
#
#
#dicts_sihih_shift = [
#    {
#        "sample"    : "TTGamRD1",
#        "analyzer"  : "TemplateSihihreal",
#        },
#    {
#        "sample"    : "TTJeRD1",
#        "analyzer"  : "TemplateSihihfake",
#        },
#    ]
#
#def make_closure_test_sequence_sihih_shift():
#    histo_mixer = make_mixer_class(
#        gen_mixer_input(
#            dicts_sihih_shift
#        )
#    )("MixerSihihShift")
#    name = "SihihShift"
#    tools = [
#        histo_mixer,
#        make_sequence(
#            name, histo_mixer, 1, xrange(500,1500,100), [1000,1000], tmpl_fit.TemplateFitToolSihihShift),
#        make_sequence(
#            name, histo_mixer, 0, xrange(500,1500,100), [1000,1000], tmpl_fit.TemplateFitToolSihihShift),
#        ]
#    return ppc.PostProcChain(
#        "TemplateFitClosureSequencesSihihShift",
#        tools
#    )
#
