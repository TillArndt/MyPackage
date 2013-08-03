
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postprocessing as ppc
import os
import glob
import subprocess
import shutil

summed_uncerts = [
    "SysIsrFsr",
    "SysOverlapDRCut",
    "SysPU",
#    "SysPhotonETCut",
    "SysSelEffSig",
    "SysSelEffBkg",
]

cmsAN   = "/afs/cern.ch/work/h/htholen/private/cmsPublishDir/cms_repo/notes/AN-13-195/trunk/"
cmsPAS  = "/afs/cern.ch/work/h/htholen/private/cmsPublishDir/cms_repo/notes/TOP-13-011/trunk/"

def total_uncert():
    sum = 0.
    for key in summed_uncerts: 
        sum += (settings.persistent_dict.get(key, 0.))**2
    return sum**.5

class ResultSummary(ppc.PostProcTool):
    can_reuse = False
    def run(self):
        res = settings.post_proc_dict["x_sec_result"]
        for key, data in settings.persistent_dict.iteritems():
            setattr(res, key, data)
        total_sys           = total_uncert()
        res.TotalSysUncert  = total_sys
        res.R_err_sys       = res.R * total_sys
        res.xsec_err_sys    = res.xsec * (
            total_sys**2
            + (settings.ttbar_xsec_cms_err / settings.ttbar_xsec_cms)**2
        )**.5

        print res

        res.write_info_file(settings.DIR_PLOTS + "summary_analysis.info")
        self.message("INFO " + str(res))


class ResultTexifier(ppc.PostProcTool):
    def __init__(self, name = None):
        super(ResultTexifier, self).__init__(name)
        self.target_dir = settings.tex_target_dir
        self.numbers_digit = [
            "N_MC_predict",
            "N_fit",
            "N_fit_err",
            "N_presel_data",
            "N_sel_data",
        ]
        self.numbers_percent_1f = [
            "TotalSysUncert",
            "eff_gamma",
            "pur_gamma",
            "pur_tt",
        ]
        self.numbers_percent_1f += summed_uncerts
        self.numbers_float_2f = [
            "StoB_gamma",
            "StoB_presel",
        ]

    def write_tex_snippets(self):
        res = settings.post_proc_dict["x_sec_result"]

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
        # R
        with open(self.plot_output_dir + "R.tex", "w") as f:
            f.write(
                "(%.2f " % (res.R*100)
                + r"\;\pm %.2f" % (res.R_err_fit*100) + r"\,\stat"
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

    def write_uncert_tabular(self):
        res = settings.post_proc_dict["x_sec_result"]
        table = [
            r"\begin{tabular}{l c} \\",
            r"\hline",
            r"\hline",
            r"Source & Uncertainty (\%) \\",
            r"\hline",
            r"Statistical & %.1f \\" % (
                getattr(res, "R_err_fit") / getattr(res, "R") * 100.
            ),
            r"\hline",
            r"Systematic & %.1f \\" % (
                getattr(res, "R_err_sys") / getattr(res, "R") * 100.
            ),
            r"\hline",
            r"Individual contributions: & \\"
        ]
        for sys in sorted(summed_uncerts, key=lambda u: -getattr(res, u)):
            table.append(
                "\;\;\;"
                + settings.get_pretty_name(sys)
                + r" & %.1f \\" % (getattr(res, sys) * 100.)
            )
        table += (
            r"\;\;\;JES & --- \\",
            r"\;\;\;JER & --- \\",
            r"\;\;\;top quark $\pt$ & --- \\",
            r"\;\;\;b-tag & --- \\",
            r"\;\;\;top quark mass & --- \\",
            r"\;\;\;PDF uncert. & --- \\",
#            r"  & --- \\",
#            r"  & --- \\",
            r"\hline",
            r"\textbf{Total} & %.1f \\" % (
                  (getattr(res, "R_err_fit") / getattr(res, "R") * 100.)**2
                + (getattr(res, "R_err_sys") / getattr(res, "R") * 100.)**2
            )**.5,
            r"\hline",
            r"\end{tabular}",
        )
        with open(self.plot_output_dir + "sys_tabular.tex", "w") as f:
            f.writelines(map(lambda l: l + "\n", table))

    def copy_to_target_dir(self):
        if not self.target_dir: return
        self.message("INFO Copying *.tex to " + self.target_dir)
        for cwd, dirs, files in os.walk(self.plot_output_dir):
            for f in files:
                if f[-4:] == ".tex":
                    shutil.copy2(
                        self.plot_output_dir + f,
                        self.target_dir
                    )
            break

    def run(self):
        self.write_tex_snippets()
        self.write_uncert_tabular()
        self.copy_to_target_dir()


class RootPlotConverter(ppc.PostProcTool):
    def __init__(self, tool_name=None):
        super(RootPlotConverter, self).__init__(tool_name)
        self.target_dir = settings.plot_target_dir
        self.pdf_copy_dirs = [
            (settings.DIR_PLOTS + "CutflowTools/CutflowStack/", ""),
            (settings.DIR_PLOTS + "TemplateFitToolSihih/", ""),
            (settings.DIR_PLOTS + "TemplateFitToolChHadIso/", ""),
            (settings.DIR_PLOTS + "DataMcComp/DataMC_Nm1Plot_logscale/", "nm1_log_"),
            (settings.DIR_PLOTS + "DataMcComp/DataMC_Nm1Plot_linscale/", "nm1_lin_"),
            (settings.DIR_PLOTS + "DataMcComp/DataMC_CrtlPlotPost_linscale/", "post_lin_"),
            (settings.DIR_PLOTS + "DataMcComp/DataMC_DataMCMuonCheck_logscale", "datamc_muon_"),
            (settings.DIR_PLOTS + "DataMcComp/DataMC_DataMCJetCheck_logscale", "datamc_jet_"),
            (settings.DIR_PLOTS + "MatchQualityStack", "match_"),
        ]

    def _set_plot_output_dir(self):
        pass

    def convert_eps_to_pdf(self):
        for pdf_dir, _ in self.pdf_copy_dirs:
            for cwd, _, files in os.walk(pdf_dir):
                if files:
                    self.message("INFO converting eps files in " + cwd)
                for f in files:
                    if  f[-4:] == ".eps":
                        subprocess.call([
                            "convert",
                            os.path.join(cwd, f),
                            os.path.join(cwd, f[:-4] + ".pdf")
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
