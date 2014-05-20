
import cmstoolsac3b.postprocessing as pstprc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.rendering as rnd
import plots_commons as com
import itertools
import re

class RandConeOverlapComp(pstprc.PostProcTool):
    def run(self):

        RandCone = gen.fs_filter_active_sort_load(
            {"sample":"whiz2to5",
             "analyzer":"PlotRandCone"}
        )
        ChHad = gen.fs_filter_active_sort_load(
            { "sample":"whiz2to5",
             "analyzer":"TemplateChHadIsoreal"}
        )

        zipped = itertools.izip(RandCone, ChHad)
        #zipped = (gen.callback(z, lambda x: x.histo.SetBinContent(1,0.)) for z in zipped) # remove first bin
        zipped = (gen.apply_histo_linecolor(z) for z in zipped)
        zipped = (gen.apply_histo_linewidth(z) for z in zipped)
        zipped = list(list(z) for z in zipped) # load all to memory

        if not (zipped and zipped[0]):
            self.message("WARNING Histograms not found!! Quitting..")
            return

        zipped[0][0].legend = "Rand. Cone Iso."
        zipped[0][1].legend = "Charged Had. Iso."
	zipped[0][1].primary_object().SetLineColor(1)

        def save_canvas(wrps, postfix):
            canvas = gen.canvas(
                wrps,
                [rnd.BottomPlotRatio, rnd.Legend, com.SimpleTitleBox]
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
       # save_canvas(
       #     (gen.gen_norm_to_lumi(z) for z in zipped),
       #     "_lumi"
       # )
	save_canvas(
	 (gen.gen_norm_to_integral(z) for z in zipped),
	 "_int"
	)


