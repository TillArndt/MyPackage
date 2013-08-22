
import copy
import cmstoolsac3b.settings as settings
import cmstoolsac3b.wrappers as wrappers
import cmstoolsac3b.postprocessing as ppc
from plots_commons import copy_tex_to_target_dir

class ShilpiMethod(ppc.PostProcTool):
    def configure(self):
        self.tight_cnt   = "FullTightIDCount,"
        self.shilp_cnt   = "ShilpiSumDirect,"

    def get_shilp_counts(self, c):
        for smp in settings.data_samples().itervalues():
            c.tight += smp.log_event_counts[self.tight_cnt]
            c.shilp += smp.log_event_counts[self.shilp_cnt]

    def calc_result(self, c):
        c.n_sig             = c.tight - c.shilp
        c.n_sig_err         = (c.tight + (0.3*c.shilp)**2)**.5
        c.n_sig_ttgam       = c.n_sig * c.pur_ttgam
        c.n_sig_ttgam_err   = c.n_sig_err * c.pur_ttgam

    def run(self):
        # get wrapper and run
        self.result = copy.deepcopy(
            settings.post_proc_dict["RealTightIdPurityCount"]
        )
        c = self.result
        c.tight     = 0.
        c.shilp     = 0.
        self.configure()
        self.get_shilp_counts(c)
        self.calc_result(c)


class ShilpiMethodMC(ShilpiMethod):
    def get_shilp_counts(self, c):
        data_lumi_sum = settings.data_lumi_sum()
        for smp in settings.mc_samples().itervalues():
            norm = data_lumi_sum / smp.lumi
            c.tight += smp.log_event_counts[self.tight_cnt] * norm
            c.shilp += smp.log_event_counts[self.shilp_cnt] * norm


class ShilpiMethodCheck(ShilpiMethod):
    def get_shilp_counts(self, c):
        data_lumi_sum = settings.data_lumi_sum()
        for smp in settings.mc_samples().itervalues():
            norm = data_lumi_sum / smp.lumi
            tight = smp.log_event_counts[self.tight_cnt] * norm
            real  = smp.log_event_counts["realFullTightIDCount,"] * norm
            c.tight += tight
            c.shilp += tight - real

    def calc_result(self, c):
        super(ShilpiMethodCheck, self).calc_result(c)
        c.n_sig_err         = c.tight**.5
        c.n_sig_ttgam_err   = c.n_sig_err * c.pur_ttgam


ShilpiMethodTools = ppc.PostProcChain("ShilpiMethodTools", [
    ShilpiMethod,
])


class ShilpiCheckTable(ppc.PostProcTool):
    def __init__(self, name=None):
        super(ShilpiCheckTable, self).__init__(name)

    def write_tabular(self):
        table = [
            r"\begin{tabular}{l c c } \\",
            r"\hline",
            r"\hline",
            r"Sample & fake-rate (MC) & fake-rate (MC truth) \\",
            r"\hline",
        ]
        data_lumi_sum = settings.data_lumi_sum()
        for smp in sorted(settings.active_samples + ["TTPoHe","TTMadG","TTMCNLO"]):
            smp = settings.samples[smp]
            if smp.is_data:
                continue
            norm = data_lumi_sum / smp.lumi
            tight = smp.log_event_counts["FullTightIDCount,"] * norm
            real  = smp.log_event_counts["realFullTightIDCount,"] * norm
            shilp = smp.log_event_counts["ShilpiSumDirect,"] * norm
            table.append(
                "\;\;\;"
                + smp.name.replace("_", r"\_")
                + r" & $%.1f\pm%.1f$ & $%.1f\pm%.1f$ \\" % (
                    shilp,
                    0.3 * shilp,                        # 30% on fr count
                    tight - real,
                    ((tight - real) * norm)**.5 / norm, # MC stat error
                )
            )
        table += (
            r"\hline",
            r"\hline",
            r"\end{tabular}",
            )
        with open(self.plot_output_dir + "shilpi_tabular.tex", "w") as f:
            f.writelines(map(lambda l: l + "\n", table))

    def run(self):
        self.target_dir = settings.tex_target_dir
        self.write_tabular()
        copy_tex_to_target_dir(self)

