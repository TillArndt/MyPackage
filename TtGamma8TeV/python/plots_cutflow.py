
from cmstoolsac3b import diskio
from cmstoolsac3b import settings
from cmstoolsac3b import wrappers
import cmstoolsac3b.postprocessing as pp
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.generators as gen
import cmstoolsac3b.decorator as dec
import plots_commons as com
import itertools
import re
import subprocess
import shutil
from math import sqrt

sample_key_func = lambda w: w.sample
legend_key_func = lambda w: settings.get_stack_position(w.sample)

class CutflowHistos(pp.PostProcTool):
    """Prepares cutflow histos for all samples, stores them in histo pool."""

    def combine_cutflow_histo(self, grp):
        """Adds histos with single bins to a combined cutflow histogram."""
        grp = list(grp)
        bin_labels = dict(
            (
                w.histo.GetMaximumBin(),
                settings.get_pretty_name(w.histo.GetXaxis().GetTitle())
            ) for w in grp
        )
        lumi = grp[0].lumi
        wrp = gen.op.sum(grp)
        wrp.lumi = lumi
        for bin, label in bin_labels.iteritems():
            wrp.histo.GetXaxis().SetBinLabel(bin, label)
        return wrp

    def run(self):
        wrps = gen.fs_content()
        wrps = gen.filter(
            wrps,
            {"analyzer": re.compile("CutFlow*")}
        )
        wrps = gen.filter_active_samples(wrps)
        wrps = sorted(wrps, key = sample_key_func)
        wrps = gen.load(wrps)
        grps = gen.group(wrps, sample_key_func)

        wrps = (self.combine_cutflow_histo(g) for g in grps)
        wrps = gen.pool_store_items(wrps)
        wrps = list(wrps)
        self.result = wrps
        count = len(wrps)
        self.message("INFO: "+self.name+" stored "+str(count)+" histos in pool.")


class CutflowStack(ppt.FSStackPlotter):
    """Reads cutflow histos from pool and stacks them up."""
    def configure(self):
        class AxisTitles(dec.Decorator):
            def do_final_cosmetics(self):
                self.decoratee.do_final_cosmetics()
                self.first_drawn.GetXaxis().SetTitle("cutflow")
                if hasattr(self, "bottom_hist"):
                    self.bottom_hist.GetXaxis().SetTitle("cutflow")
                self.first_drawn.GetYaxis().SetTitle("selected events / step")
        self.canvas_decorators += (com.LumiTitleBox, AxisTitles)
        self.save_log_scale = True

    def set_up_stacking(self):
        wrps = gen.pool_content()
        wrps = gen.filter(
            wrps,
            {"analyzer": re.compile("CutFlow")}
        )
        wrps = gen.group(wrps)
        stream_stack = gen.mc_stack_n_data_sum(
            wrps,
            use_all_data_lumi=True
        )
        def assign_name(wrp): wrp.name = "CombinedCutflow"
        self.stream_stack = gen.pool_store_items(stream_stack, assign_name)


class CutflowTableContent(pp.PostProcTool):
    """Generates cutflow table data."""
    can_reuse = False
    has_output_dir = False

    def __init__(self, name = None):
        super(CutflowTableContent, self).__init__()
        self.input_mc       = []
        self.input_data     = []
        self.head_line      = []
        self.table_data     = []
        self.table_mc_err   = []
        self.table_mc       = []
        self.titles_data    = []
        self.titles_mc      = []

    def get_input_histos(self):
        mcee = gen.gen_prod( # need to norm to lumi
            itertools.izip(
                gen.gen_norm_to_lumi(
                    gen.filter(
                        settings.post_proc_dict["CutflowHistos"],
                        {"is_data": False}
                    )
                ),
                itertools.repeat(
                    settings.data_lumi_sum_wrp()
                )
            )
        )
        data = gen.filter(
            settings.post_proc_dict["CutflowHistos"],
            {"is_data": True}
        )
        self.input_mc    = sorted(mcee, key = legend_key_func)
        self.input_data  = sorted(data, key = legend_key_func)

    def fill_head_line(self):
        bin_label = self.input_mc[0].histo.GetXaxis().GetBinLabel
        self.head_line = list(
            bin_label(i + 1)
                for i in xrange(self.input_mc[0].histo.GetNbinsX())
        )

    def _get_value_list(self, wrp):
        bin_cont = wrp.histo.GetBinContent
        return list(bin_cont(i + 1) for i in xrange(wrp.histo.GetNbinsX()))

    def _get_error_list(self, wrp):
        err_cont = wrp.histo.GetBinError
        return list(err_cont(i + 1) for i in xrange(wrp.histo.GetNbinsX()))

    def fill_tables(self):
        for wrp in self.input_data:
            self.titles_data.append(wrp.sample)
            self.table_data.append(self._get_value_list(wrp))
        for wrp in self.input_mc:
            self.titles_mc.append(wrp.sample)
            self.table_mc.append(self._get_value_list(wrp))
        for wrp in self.input_mc:
            self.table_mc_err.append(self._get_error_list(wrp))

    def _make_column_sum(self, table, squared = False):
        def gen_sum(A, B):
            return list(a + b for a,b in itertools.izip(A, B))
        def gen_sum_sq(A, B):
            return map(sqrt, ((a*a) + (b*b) for a,b in itertools.izip(A, B)))
        row = []
        for ro in table:
            if not row:
                row = ro[:]
            elif squared:
                row = gen_sum_sq(row, ro)
            else:
                row = gen_sum(row, ro)
        return row

    def fill_sum_rows(self):
        self.table_data.append(self._make_column_sum(self.table_data))
        self.table_mc.append(self._make_column_sum(self.table_mc))
        self.table_mc_err.append(self._make_column_sum(self.table_mc_err, True))
        self.titles_data.append("Data Sum")
        self.titles_mc.append("MC Sum")

    def run(self):
        self.get_input_histos()
        self.fill_head_line()
        self.fill_tables()
        self.fill_sum_rows()
        settings.post_proc_dict["CutflowTableContent"] = self

    def mc_title_val_err_iterator(self):
        for title, vals, errs in itertools.izip(
            self.titles_mc,
            self.table_mc,
            self.table_mc_err,
        ):
            yield title, vals, errs

    def data_title_value_iterator(self):
        for title, vals in itertools.izip(
            self.titles_data,
            self.table_data
        ):
            yield title, vals


class CutflowTableTxt(pp.PostProcTool):
    """Reads cutflow histos from pool and creates latex table code."""

    def __init__(self, name = None):
        super(CutflowTableTxt, self).__init__(name)
        self.cont           = None
        self.table_lines    = []
        self.sep            = ", "

    def configure(self):
        self.cont = settings.post_proc_dict["CutflowTableContent"]

    def make_header(self):
        line = self.sep.join(itertools.imap(lambda s: "%17s"%s, self.cont.head_line))
        line = 17*" " + self.sep + line + " \n"
        self.table_lines.append(line)

    def make_center(self):
        self.table_lines.append("\n")
        for title, vals, errs in self.cont.mc_title_val_err_iterator():
            zipped = ((a, b) for a, b in itertools.izip(vals, errs))
            self.table_lines.append(
                "%17s" % title
                + self.sep
                + self.sep.join("%8.1f +- %5.1f" % p for p in zipped)
                + " \n"
            )
        self.table_lines.append("\n")
        for title, vals in self.cont.data_title_value_iterator():
            self.table_lines.append(
                "%17s" % title
                + self.sep
                + self.sep.join("%17d" % v for v in vals)
            )
        self.table_lines.append("\n")

    def write_out(self):
        with open(self.plot_output_dir + "cutflow_table.txt", "w") as f:
            f.writelines(self.table_lines)
        wrp = wrappers.Wrapper(name="CutflowTableTxt")
        for i, line in enumerate(self.table_lines):
            setattr(wrp, "line_%2d"%i, line)
        diskio.write(wrp, self.plot_output_dir + "cutflow_table.info")

    def run(self):
        self.configure()
        self.make_header()
        self.make_center()
        self.write_out()


class CutflowTableTex(pp.PostProcTool):
    """Reads cutflow histos from pool and creates latex table code."""

    def __init__(self, name = None):
        super(CutflowTableTex, self).__init__(name)
        self.cont           = None
        self.table_lines    = []
        self.target_dir     = ""
        self.sep            = " $&$ "

    def configure(self):
        self.cont = settings.post_proc_dict["CutflowTableContent"]

    def make_header(self):
        self.table_lines += (
            r"\begin{tabular}{l | "
                + len(self.cont.head_line)*"r "
                + "}",
            17*" "
                + " & "
                + " & ".join(itertools.imap(
                    lambda s: "%17s" % settings.get_pretty_name(s + "_tex"),
                    self.cont.head_line
                ))
                + r" \\",
            r"\hline",
            r"\hline",
        )

    def make_center(self):
        for title, vals, errs in self.cont.mc_title_val_err_iterator():
            self.table_lines += (
                "%17s" % title.replace("_", r"\_")
                    + " &$ "
                    + self.sep.join("%17.1f" % v for v in vals)
                    + r" $ \\",
                17*" "
                    + " &$ "
                    + self.sep.join("\\pm%17.1f" % e for e in errs)
                    + r" $ \\",
            )
        self.table_lines.insert(-2, r"\hline")
        self.table_lines.append(r"\hline")
        for title, vals in self.cont.data_title_value_iterator():
            self.table_lines.append(
                "%17s" % title.replace("_", r"\_")
                + " &$ "
                + " $&$ ".join("%17d" % v for v in vals)
                + r" $ \\"
            )
        self.table_lines.insert(-1, r"\hline")
        self.table_lines.append(r"\hline")

    def make_footer(self):
        self.table_lines += (
            r"\end{tabular}",
        )

    def write_out(self):
        with open(self.plot_output_dir + "cutflow_tabular.tex", "w") as f:
            f.writelines(map(lambda l: l + "\n", self.table_lines))

        with open(self.plot_output_dir + "cutflow.tex", "w") as f:
            f.writelines(map(lambda l: l + "\n", tex_template))

#        subprocess.call(
#            ["pdflatex", "cutflow.tex"],
#            cwd=self.plot_output_dir
#        )

        wrp = wrappers.Wrapper(name="CutflowTableTex")
        for i, line in enumerate(self.table_lines):
            setattr(wrp, "line_%2d"%i, line)
        diskio.write(wrp, self.plot_output_dir + "cutflow_table.info")

    def copy_to_target_dir(self):
        if not self.target_dir:
            return
        self.message("INFO Copying cutflow_tabular.tex to " + self.target_dir)
        shutil.copy2(
            self.plot_output_dir + "cutflow_tabular.tex",
            self.target_dir
        )

    def run(self):
        self.configure()
        self.make_header()
        self.make_center()
        self.make_footer()
        self.write_out()
        self.copy_to_target_dir()


tex_template = [
    r"\documentclass[10pt,fullpage]{article}",
    r"\pagestyle{empty}",
    r"\usepackage[landscape]{geometry}  % [margin=5mm, ]",
    r"\usepackage[usenames]{color} % Farbunterstuetzung",
    r"\usepackage{amssymb}	% Mathe",
    r"\usepackage{amsmath} % Mathe",
    r"\usepackage[utf8]{inputenc} % Direkte Eingabe von Umlauten und anderen Diakritika",
    r"\begin{document}",
    r"\begin{table}",
    r"\input{cutflow_tabular.tex}",
    r"\end{table}",
    r"\end{document}",
]

_cutflow_table_tex_instance_with_target_dir = CutflowTableTex()
_cutflow_table_tex_instance_with_target_dir.target_dir = settings.tex_target_dir

cutflow_chain = pp.PostProcChain("CutflowTools", [
    CutflowHistos,
    CutflowStack,
    CutflowTableContent,
    CutflowTableTxt,
    _cutflow_table_tex_instance_with_target_dir,
])
