
import os
import glob
import copy
import subprocess
import shutil
from cmstoolsac3b import settings, wrappers, diskio
import cmstoolsac3b.postprocessing as ppc
import plots_xsec
from plots_commons import copy_tex_to_target_dir

summed_uncerts = [
#    "SysMadgraph",
#    "SysOverlapDRCut",
    "SysPU",
    "SysFit",
#    "SysPhotonETCut",
    "SysSelEffSig",
    "SysSelEffBkg",
    "SysIsrFsr",
    "SysMCatNLO",
    "SysWhizPDF",
    "SysTopPt",
    "SysBTagWeight",
    "SysJEC",
    "SysJER",
]

result_quantities = ["n_sig_ttgam", "R_fid", "R", "xsec"]

def xsec_calc_name_iter():
    return (c.name for c in plots_xsec.XsecCalculators.tool_chain)

cmsPub  = "/afs/cern.ch/work/h/htholen/private/cmsPublishDir/"
cmsAN   = cmsPub + "cms_repo/notes/AN-13-195/trunk/"
cmsPAS  = cmsPub + "cms_repo/notes/TOP-13-011/trunk/"

def total_uncert(quantity):
    sum = 0.
    for key in summed_uncerts:
        wrp = settings.persistent_dict.get(key)
        if wrp:
            sum += (getattr(wrp, quantity))**2
    return sum**.5

class ResultSummary(ppc.PostProcTool):
    def __init__(self, xsec_calc):
        super(ResultSummary, self).__init__(
            self.__class__.__name__ + "_" + xsec_calc
        )
        self.xsec_calc = xsec_calc

    def run(self):
        res_wrp = settings.post_proc_dict[self.xsec_calc]
        res_wrp.name = self.name
        for q in result_quantities:
            name = self.xsec_calc + "_" + q
            for sys in summed_uncerts:
                wrp = settings.persistent_dict.get(sys)
                if wrp:
                    setattr(res_wrp, sys + "_" + name, getattr(wrp, name))
            total_sys = total_uncert(name)
            setattr(res_wrp, "TotalSysUncert_" + q, total_sys)
            setattr(res_wrp, q + "_err_sys", getattr(res_wrp, q) * total_sys)
            setattr(res_wrp, "xsec_err_sys",
                res_wrp.xsec * (
                    total_sys**2
                    + (settings.ttbar_xsec_cms_err / settings.ttbar_xsec_cms)**2
                )**.5
            )

        self.result = res_wrp # write out later..
        self.message("INFO " + str(res_wrp))

ResultSummaries = ppc.PostProcChain(
    "ResultSummaries",
    list(ResultSummary(x) for x in xsec_calc_name_iter())
)


class ResultTexifier(ppc.PostProcTool):
    def __init__(self, xsec_calc):
        super(ResultTexifier, self).__init__(
            self.__class__.__name__ + "_" + xsec_calc
        )
        self.xsec_calc = xsec_calc
        self.target_dir = settings.tex_target_dir
        self.numbers_digit = [
#            "N_MC_predict",
            "n_sig",
            "n_sig_err",
            "n_sig_ttgam",
            "n_sig_ttgam_err",
            "n_sig_ttgam_err_sys",
            "N_presel_data",
            "N_sel_data",
        ]
        self.numbers_percent_1f = [
            "TotalSysUncert_R",
            "eff_gamma",
            "pur_ttgam",
            "pur_tt",
        ]
        self.numbers_percent_1f += map(
            lambda s: s + "_" + xsec_calc + "_R",
            summed_uncerts
        )
        self.numbers_float_2f = [
            "StoB_gamma",
            "StoB_presel",
        ]

    def write_tex_snippets(self):
        res = self.result

        # write digit numbers
        for key in self.numbers_digit:
            with open(self.plot_output_dir + key + ".tex", "w") as f:
                f.write("%d" % getattr(res, key))

        # write percent numbers
        for key in self.numbers_percent_1f:
            with open(self.plot_output_dir + key + ".tex", "w") as f:
                f.write(("%.1f" % (getattr(res,key) * 100.))+"\\,\\%")

        # write float numbers
        for key in self.numbers_float_2f:
            with open(self.plot_output_dir + key + ".tex", "w") as f:
                f.write("%.2f" % getattr(res,key))

        # write special numbers
        # R_fid
        with open(self.plot_output_dir + "R_fid.tex", "w") as f:
            f.write(
                "(%.2f " % (res.R_fid*100)
                + r"\;\pm %.2f" % (res.R_fid_err_stat*100) + r"\,\stat"
                + r"\;\pm %.2f" % (res.R_fid_err_sys*100) + r"\,\syst"
                + r")\cdot 10^{-2}"
            )
        # R
        with open(self.plot_output_dir + "R.tex", "w") as f:
            f.write(
                "(%.2f " % (res.R*100)
                + r"\;\pm %.2f" % (res.R_err_stat*100) + r"\,\stat"
                + r"\;\pm %.2f" % (res.R_err_sys*100) + r"\,\syst"
                + r")\cdot 10^{-2}"
            )
        # xsec
        with open(self.plot_output_dir + "xsec.tex", "w") as f:
            f.write(
                "%.1f" % res.xsec
                + r"\;\pm" + ("%.1f" % res.xsec_err_stat) + r"\,\stat"
                + r"\;\pm" + ("%.1f" % res.xsec_err_sys) + r"\,\syst"
            )
        # largestSys
        with open(self.plot_output_dir + "largestSys.tex", "w") as f:
            f.write(("%.1f" % (
                getattr(res, "SysFit_"+self.xsec_calc+"_R") * 100.
                ))+"\\,\\%")

    def write_snippets_for_latexit(self):
        res = self.result
        wrp = wrappers.Wrapper(
            name="LatexitSnippets",
            xsec_ttgam=
            r"\sigma_{t \bar t+\gamma} \;&=\; R\;\cdot \;\sigma_{t\bar t} \\ &=\; "
            + (r"%.1f" % res.xsec)
            + (r"\;\pm \;%.1f{\rm (stat.)}" % res.xsec_err_stat)
            + (r" \;\pm \;%.1f{\rm (syst.)} \,\tn{pb}" % res.xsec_err_sys),
            R_result=
            r"\begin{align*} "
            + (r"\pi_{t\bar t} = %.1f" % (res.pur_tt*100)) + r"\,\% \\ "
            + (r"\pi_{t\bar t+\gamma} = %.1f" % (res.pur_ttgam*100)) + r"\,\% \\ "
            + (r"\epsilon_\gamma = %.1f" % (res.eff_gamma*100)) + r"\,\% \\ "
            + (r"\Rightarrow R \;=\;(%.2f " % (res.R*100))
            + (r"\;\pm %.2f^\tn{fit})\cdot 10^{-2} " % (res.R_err_stat*100))
            + r"\end{align*} ",
        )
        diskio.write(wrp)
        with open(self.plot_output_dir + "__LATEXIT_xsec.tex", "w") as f:
            f.write(wrp.xsec_ttgam + "\n")
        with open(self.plot_output_dir + "__LATEXIT_R.tex", "w") as f:
            f.write(wrp.R_result + "\n")

    def write_uncert_tabular(self):
        res = self.result
        table = [
            r"\begin{tabular}{l c c} \\",
            r"\hline",
            r"\hline",
            r"Source & \multicolumn{2}{c}{Uncertainty (\%)} \\",
            r"& $\Rvis$ & $\sigma_{\ttgam}$ \\",
            r"\hline",
            r"Statistical & %.1f & %.1f \\" % (
                getattr(res, "R_fid_err_stat") / getattr(res, "R_fid") * 100.,
                getattr(res, "xsec_err_stat") / getattr(res, "xsec") * 100.,
            ),
            r"\hline",
            r"Systematic & %.1f & %.1f \\" % (
                getattr(res, "R_fid_err_sys") / getattr(res, "R_fid") * 100.,
                getattr(res, "xsec_err_sys") / getattr(res, "xsec") * 100.,
            ),
            r"\hline",
            r"Individual contributions: & & \\"
        ]
#        # sort by largest contribution
#        for sys in sorted(summed_uncerts,
#            key=lambda s: -getattr(res, s + "_" + self.xsec_calc + "_R")
#        ):
        for sys in summed_uncerts:
            table.append(
                "\;\;\;"
                + settings.get_pretty_name(sys)
                + r" & %.1f & %.1f \\" % (
                    getattr(res, sys+"_"+self.xsec_calc+"_R_fid") * 100.,
                    getattr(res, sys+"_"+self.xsec_calc+"_xsec") * 100.,
                ),
            )
        table += (
            r"\;\;\;top-quark mass  & ---  & --- \\",
            r"\hline",
            r"\textbf{Total} & %.1f & %.1f \\" % (
(
    (getattr(res, "R_fid_err_stat") / getattr(res, "R_fid") * 100.)**2
  + (getattr(res, "R_fid_err_sys") / getattr(res, "R_fid") * 100.)**2
)**.5,
(
    (getattr(res, "xsec_err_stat") / getattr(res, "xsec") * 100.)**2
  + (getattr(res, "xsec_err_sys") / getattr(res, "xsec") * 100.)**2
)**.5,
            ),
            r"\hline",
            r"\hline",
            r"\end{tabular}",
        )
        with open(self.plot_output_dir + "sys_tabular.tex", "w") as f:
            f.writelines(map(lambda l: l + "\n", table))
        for n, l in enumerate(table):
            setattr(self.result, "line%02d"%n, l)

    def run(self):
        self.result = copy.deepcopy(
            settings.post_proc_dict["ResultSummary_" + self.xsec_calc]
        )
        self.write_tex_snippets()
        self.write_snippets_for_latexit()
        self.write_uncert_tabular()
        copy_tex_to_target_dir(self)


class ResultTexifierMethodComp(ResultTexifier):
    def __init__(self, name=None):
        super(ResultTexifier, self).__init__(name)

    def write_method_comparison_tabular(self):
        res = self.results
        l = len(res)
        for r in res:
            r.calc = r.name.split("_")[-1]
        table = [
            r"\begin{tabular}{l " + l*"c " + r"} \\",
            r"\hline",
            r"\hline",
            "Method " + (l*"& %s" + r" \\") % tuple(
                settings.get_pretty_name(r.calc)
                for r in res
            ),
            (r"$\Nsig / \epsilon_\gamma$ " + l*" & %.1f" + r" \\") % tuple(
                getattr(r, "n_sig_ttgam") / r.eff_gamma
                for r in res
            ),
            r"\hline",
            r"\hline",
            r"Source & \multicolumn{" + str(l) + r"}{c}{Uncertainty} \\",
            r"\hline",
            (r"Internal (e.g. fit) " + l*" & %.1f" + r" \\") % tuple(
                getattr(r, "n_sig_ttgam_err") / r.eff_gamma
                for r in res
                ),
            r"\hline",
            (r"Systematic" + l*" & %.1f" + r" \\") % tuple(
                getattr(r, "n_sig_ttgam_err_sys") / r.eff_gamma
                for r in res
                ),
            r"\hline",
            r"Contributions: & & \\"
        ]
        for sys in sorted(summed_uncerts,
            key=lambda s: -getattr(res[0], s + "_" + res[0].calc + "_n_sig_ttgam")
        ):
            table.append(
                "\;\;\;"
                + settings.get_pretty_name(sys)
                + (l*" & %.1f" + r" \\") % tuple(
                    getattr(r, sys+"_"+r.calc+"_n_sig_ttgam") * getattr(r, "n_sig_ttgam")  / r.eff_gamma
                    for r in res
                    ),
            )
        table += (
            r"\hline",
            (r"\textbf{Total uncertainty}" + l*" & %.1f" + r" \\") % tuple(
                    (
                        getattr(r, "n_sig_ttgam_err")**2
                        + getattr(r, "n_sig_ttgam_err_sys")**2
                    )**.5  / r.eff_gamma
                    for r in res
                ),
            r"\hline",
            r"\hline",
            r"\end{tabular}",
            )
        with open(self.plot_output_dir + "method_tabular.tex", "w") as f:
            f.writelines(map(lambda l: l + "\n", table))
        for n, l in enumerate(table):
            setattr(self.result, "line%02d"%n, l)

    def run(self):
        self.target_dir = settings.tex_target_dir
        self.results = list(
            settings.post_proc_dict["ResultSummary_" + calc]
            for calc in xsec_calc_name_iter()
        )
        self.result = wrappers.Wrapper()
        self.write_method_comparison_tabular()
        copy_tex_to_target_dir(self)


class RootPlotConverter(ppc.PostProcTool):
    has_output_dir = False

    def __init__(self, tool_name=None):
        super(RootPlotConverter, self).__init__(tool_name)
        self.target_dir = settings.plot_target_dir
        self.pdf_copy_dirs = [
(settings.DIR_PLOTS + "TemplateFitPlots/SideBandVSFakeTTMadG/", "sb_vs_fake_MadG_"),
(settings.DIR_PLOTS + "TemplateFitPlots/SideBandVSFakeTTPoPy/", "sb_vs_fake_PoPy_"),
(settings.DIR_PLOTS + "TemplateFitPlots/SideBandVSFakeTTPoHe/", "sb_vs_fake_PoHe_"),
(settings.DIR_PLOTS + "TemplateFitPlots/SideBandVSFakeTTMCNLO/", "sb_vs_fake_MCNLO_"),
(settings.DIR_PLOTS + "TemplateFitPlots/SideBandVSFakeTTJeRD1/", "sb_vs_fake_JeRD1_"),
(settings.DIR_PLOTS + "TemplateFitTools/TemplateFitToolChHadIsoSBIDInputBkgWeight/", "sb_rw_sbid_"),
(settings.DIR_PLOTS + "TemplateFitTools/TemplateFitToolChHadIsoSbBkgInputBkgWeight/", "sb_rw_sbbkg_"),
(settings.DIR_PLOTS + "TemplateFitPlots/SideBandVSFakeTTJeRD1/", "sb_vs_fake_JeRD1_"),
(settings.DIR_PLOTS + "TemplateFitTools/TemplateStacks/", ""),
(settings.DIR_PLOTS + "TemplateFitTools/TemplateOverlaysNormIntegral/", "overlay_int_"),
(settings.DIR_PLOTS + "TemplateFitTools/TemplateFitToolChHadIsoSBID/", "fit_ChHadIso_"),
(settings.DIR_PLOTS + "TemplateFitClosureSequencesaltMC/Sequence1/Evaluator_ChHadIso_1/", "closure_real_"),
(settings.DIR_PLOTS + "TemplateFitClosureSequencesaltMC/Sequence0/Evaluator_ChHadIso_0/", "closure_fake_"),
(settings.DIR_PLOTS + "DataMcComp/DataMC_Nm1Plot_logscale/","nm1_log_"),
(settings.DIR_PLOTS + "DataMcComp/DataMC_Nm1Plot_linscale/","nm1_lin_"),
(settings.DIR_PLOTS + "DataMcComp/DataMC_CrtlPlotPost_linscale/","post_lin_"),
(settings.DIR_PLOTS + "DataMcComp/DataMC_DataMCMuonCheck_logscale/","datamc_muon_"),
(settings.DIR_PLOTS + "DataMcComp/DataMC_DataMCJetCheck_logscale/","datamc_jet_"),
(settings.DIR_PLOTS + "MatchQualityStack/", "match_"),
        ]

    def convert_eps_to_pdf(self):
        for pdf_dir, _ in self.pdf_copy_dirs:
            for cwd, _, files in os.walk(pdf_dir):
                if files:
                    self.message("INFO converting eps files in " + cwd)
                for f in files:
                    f_eps = os.path.join(cwd, f)
                    f_pdf = os.path.join(cwd, f[:-4] + ".pdf")
                    if  f[-4:] == ".eps" and not os.path.exists(f_pdf):
                        subprocess.call([
                            "convert",
                            f_eps,
                            f_pdf
                        ])
                break

    def copy_to_target_dir(self):
        self.message("INFO copying pdfs to " + self.target_dir)
        for pdf_dir, prefix in self.pdf_copy_dirs:
            for _, _, files in os.walk(pdf_dir):
                for f in files:
                    if f[-4:] == ".pdf":
                        shutil.copy2(
                            os.path.join(pdf_dir, f),
                            os.path.join(self.target_dir, prefix + f)
                        )
                break

    def run(self):
        self.convert_eps_to_pdf()
        self.copy_to_target_dir()


class CopyTool(ppc.PostProcTool):
    has_output_dir = False
    def copy_from_AN_to_PAS(self):
        self.message("INFO copying auto_snippets and auto_images from AN to PAS")
        auto_snippets   = glob.glob(settings.tex_target_dir + "*.tex")
        auto_images     = glob.glob(settings.plot_target_dir + "*.pdf")
        target_snippets = cmsPAS + "auto_snippets/"
        target_images   = cmsPAS + "auto_images/"
        tex_dir         = cmsAN
        subprocess.call(["svn", "up"], cwd=tex_dir)
        subprocess.call(["cp"] + auto_snippets + [target_snippets])
        subprocess.call(["cp"] + auto_images + [target_images])

    def run(self):
        self.copy_from_AN_to_PAS()


class TexCompiler(ppc.PostProcTool):
    has_output_dir = False

    def run(self):
        #subprocess.call("./tdr_init.sh && ./tdr_compile.sh", shell=True, cwd=cmsAN)
        subprocess.call("./tdr_init.sh && ./tdr_compile.sh", shell=True, cwd=cmsPAS)
