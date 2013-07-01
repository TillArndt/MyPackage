

import cmstoolsac3b.postprocessing as pp
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.generators as gen
import cmstoolsac3b.settings as settings
import cmstoolsac3b.decorator as dec
import cmstoolsac3b.wrappers as wrappers
import plots_commons as com
import itertools
import re

sample_key_func = lambda w: w.sample
legend_key_func = lambda w: settings.get_stack_position(w.sample)

class CutflowHistos(pp.PostProcTool):
    """Prepares cutflow histos for all samples, stores them in histo pool."""
    can_reuse = False

    def _set_plot_output_dir(self):
        pass

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
        count = gen.consume_n_count(wrps)
        self.message("INFO: "+self.name+" stored "+str(count)+" histos in pool.")


class CutflowStack(ppt.FSStackPlotter):
    """Reads cutflow histos from pool and stacks them up."""
    can_reuse = False

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


class CutflowTable(pp.PostProcTool):
    """Reads cutflow histos from pool and creates latex table code."""

    def input_histos(self):
        wrps = gen.pool_content()
        wrps = gen.filter(
            wrps,
            {"analyzer": re.compile("CutFlow")}
        )
        wrps = itertools.ifilter(
            lambda w: type(w) is wrappers.HistoWrapper,
            wrps
        )
        wrps = sorted(wrps, key = legend_key_func)
        return wrps

    def make_first_line(self, wrp):
        line = "\\begin{tabular}{ "
        for i in xrange(wrp.histo.GetNbinsX()):
            line += "c "
        line += "}  \n"
        return line

    def make_headline(self, wrp):
        bin_label = wrp.histo.GetXaxis().GetBinLabel
        labels = (bin_label(i) for i in xrange(wrp.histo.GetNbinsX()))
        line = " & ".join(labels)
        line = " & " + line + " \n"
        return line

    def make_line_for_histo(self, wrp):
        bin_cont = wrp.histo.GetBinContent
        nums = (bin_cont(i) for i in xrange(wrp.histo.GetNbinsX()))
        tokens = itertools.imap(str,nums)
        num_line = " $&$ ".join(tokens)
        line = wrp.analyzer + "&$" + num_line + "$\\\\ \n"
        return line

    def run(self):
        table_lines = []
        for wrp in self.input_histos():
            if not table_lines:
                table_lines.append(self.make_first_line(wrp))
                table_lines.append(self.make_headline(wrp))
            table_lines.append(self.make_line_for_histo(wrp))
        table_lines.append("\\end{tabular} \n")

        with open(self.plot_output_dir + "cutflow_table.tex", "w") as f:
            f.writelines(table_lines)


