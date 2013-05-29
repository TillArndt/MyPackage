
import cmstoolsac3b.postprocessing as pstprc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.rendering as rnd
import plots_commons as com
import itertools
import re

class MEOverlapComp(pstprc.PostProcTool):
    def run(self):

        kicked = gen.fs_filter_sort_load(
            {"sample":"TTJetsSignal",
             "analyzer":"ttbarPhotonMergerSingleCall",
             "name":re.compile("\S*Kicked")}
        )
        whizard = gen.fs_filter_sort_load(
            {"sample":"whiz2to5",
             "analyzer":"photonsSignalMEanalyzer"}
        )

        zipped = itertools.izip(kicked, whizard)
        zipped = (gen.callback(z, lambda x: x.histo.SetBinContent(1,0.)) for z in zipped) # remove first bin
        zipped = (gen.apply_histo_linecolor(z) for z in zipped)
        zipped = (gen.apply_histo_linewidth(z) for z in zipped)
        zipped = list(list(z) for z in zipped) # load all to memory

        if not (zipped and zipped[0]):
            self.message("WARNING Histograms not found!! Quitting..")
            return

        zipped[0][0].legend = "removed (madgraph)"
        zipped[0][1].legend = "tt#gamma (whizard)"

        def save_canvas(wrps, postfix):
            canvas = gen.canvas(
                wrps,
                [rnd.BottomPlotRatio, rnd.LegendRight, com.SimpleTitleBox]
            )
            canvas = gen.save(
                canvas,
                lambda c: self.plot_output_dir + c.name + postfix
            )
            canvas = gen.switch_log_scale(canvas)
            canvas = gen.save(
                canvas,
                lambda c: self.plot_output_dir + c.name + postfix + "_log"
            )
            gen.consume_n_count(canvas)

        # norm to integral / lumi and save
        save_canvas(
            (gen.gen_norm_to_lumi(z) for z in zipped),
            "_lumi"
        )
#        save_canvas(
#            (gen.gen_norm_to_integral(z) for z in zipped),
#            "_int"
#        )

