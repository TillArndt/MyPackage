

import cmstoolsac3b.postprocessing as pp
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.generators as gen
import cmstoolsac3b.settings as settings
import plots_commons as com
import itertools
import re

sample_key_func = lambda w: w.sample
legend_key_func = lambda w: settings.get_stack_position(w.sample)

class CutflowHistos(pp.PostProcTool):
    """Prepares cutflow histos for all samples, stores them in histo pool."""
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
            print bin, label
            wrp.histo.GetXaxis().SetBinLabel(bin, label)
        return wrp

    def run(self):
        wrps = gen.fs_content()
        wrps = gen.filter(
            wrps,
            {"analyzer": re.compile("CutFlow*")}
        )
        wrps = sorted(wrps, key = sample_key_func)
        wrps = gen.load(wrps)
        grps = gen.group(wrps, sample_key_func)

        wrps = (self.combine_cutflow_histo(g) for g in grps)
        wrps = gen.pool_store_items(wrps)
        count = gen.consume_n_count(wrps)
        self.message("INFO: "+self.name+" stored "+str(count)+" histos in pool.")


class CutflowStack(ppt.FSStackPlotter):
    """Reads cutflow histos from pool and stacks them up."""
    def configure(self):
        self.canvas_decorators.append(com.LumiTitleBox)
        self.save_log_scale = True

    def set_up_stacking(self):
        wrps = gen.pool_content()
        wrps = gen.filter(
            wrps,
            {"analyzer": re.compile("CutFlow")}
        )
        wrps = gen.group(wrps)
        self.stream_stack = gen.mc_stack_n_data_sum(
            wrps,
            use_all_data_lumi=True
        )


class CutflowTable(pp.PostProcTool):
    """Reads cutflow histos from pool and creates latex table code."""

    def input_histos(self):
        wrps = gen.pool_content()
        wrps = gen.filter(
            wrps,
            {"analyzer": re.compile("CutFlow")}
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


