
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postprocessing as pstprc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.rendering as rnd
import re
import itertools

class DataMCComp(pstprc.PostProcTool):
    
    def doMCCompsForRun(self, runLabel="AllRuns"):

        def removeWildListItem(x): 
            if "Run" not in x:
                return x
	samplelist=settings.samples_stack
	if runLabel!="AllRuns":
	        samplelist=filter(removeWildListItem, settings.samples_stack)
		samplelist.append(runLabel)
	
        stream_stack1 = gen.fs_mc_stack_n_data_sum(
            {"analyzer":(re.compile("DataMCCompPhotons")),
            "sample": samplelist}
        )
        stream_stack2 = gen.fs_mc_stack_n_data_sum(
            {"analyzer":(re.compile("DataMCJetCheck")),
            "sample": samplelist}
        )
        stream_stack3 = gen.fs_mc_stack_n_data_sum(
            {"analyzer":(re.compile("DataMCMuonCheck")),
            "sample": samplelist}
        )
        stream_stack4 = gen.fs_mc_stack_n_data_sum(
            {"analyzer":(re.compile("DataMCPhotonCheck")),
            "sample": samplelist}
        )
        stream_stack = itertools.chain(stream_stack1, stream_stack2, stream_stack3, stream_stack4)

        stream_stack = gen.pool_store_items(stream_stack)

        stream_canvas = gen.canvas(
            stream_stack,
            [rnd.LegendRight]
        )

        stream_canvas = gen.save(
            stream_canvas,
            lambda wrp: self.plot_output_dir + wrp.name+runLabel,
        )

        count = gen.consume_n_count(stream_canvas)
        self.message("INFO: "+self.name+" produced "+str(count)+" canvases.")

    def run(self):        
        self.doMCCompsForRun("Run2012Arecover06Aug2012")
        self.doMCCompsForRun("Run2012B13Jul2012")
	self.doMCCompsForRun()

class CrtlFiltTool(pstprc.PostProcTool):
    def run(self):

        stream_stack1 = gen.fs_mc_stack(
            {"analyzer":(re.compile("CrtlFilt*")),
            "sample":settings.samples_stack}
        )
        stream_stack2 = gen.fs_mc_stack(
                {"analyzer":(re.compile("PhotonAna*")),
                "sample":settings.samples_stack}
        )
        stream_stack = itertools.chain(stream_stack1, stream_stack2)

        stream_stack = gen.pool_store_items(stream_stack)

        stream_canvas = gen.canvas(
            stream_stack,
            [rnd.LegendRight]
        )

        stream_canvas = gen.save(
            stream_canvas,
            lambda wrp: self.plot_output_dir + wrp.name,
        )

        count = gen.consume_n_count(stream_canvas)
        self.message("INFO: "+self.name+" produced "+str(count)+" canvases.")


class OverlapComparison(pstprc.PostProcTool):
    def run(self):

        kicked = gen.fs_filter_sort_load(
            {"sample":"TTbarBG",
            "analyzer":"ttbarPhotonMerger",
            "name":re.compile("\S*Kicked")}
        )
        whizard = gen.fs_filter_sort_load(
            {"sample":"two2seven_27_m_8",
            "analyzer":"photonsSignalMEanalyzer"}
        )

        zipped = itertools.izip(kicked, whizard)
        zipped = (gen.callback(z, lambda x: x.histo.SetBinContent(1,0.)) for z in zipped) # remove first bin
        zipped = (gen.apply_histo_linecolor(z) for z in zipped)
        zipped = (gen.apply_histo_linewidth(z) for z in zipped)
        zipped = list(list(z) for z in zipped) # load all to memory

        def save_canvas(wrps, postfix):
            canvas = gen.canvas(
                wrps,
                [rnd.BottomPlotRatio, rnd.LegendRight]
            )
            canvas = gen.callback(canvas, lambda c: c.legend.GetListOfPrimitives()[1].SetLabel("Removed Photons"))
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
            (gen.gen_norm_to_integral(z) for z in zipped),
            "_int"
        )
        save_canvas(
            (gen.gen_norm_to_lumi(z) for z in zipped),
            "_lumi"
        )


