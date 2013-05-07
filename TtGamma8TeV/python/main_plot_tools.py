
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postprocessing as pstprc
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.generators as gen
import cmstoolsac3b.rendering as rnd
import re
import itertools

def generate_data_mc_comp_tools():
    """
    Generates postproctools by subclassing from ptt.FSStackPlotter.
    Walks over all samples and specific analyzer tokens.
    """
    run_labels = settings.data_samples().keys()
    run_labels.append(None) # all runs
    analyzer_pats = [
        re.compile("CrtlFilt"),
        re.compile("PhotonAna"),
        re.compile("DataMCCompPhotons"),
        re.compile("DataMCJetCheck"),
        re.compile("DataMCMuonCheck"),
        re.compile("DataMCPhotonCheck"),
        re.compile("WeightsCheck"),
    ]
    list_of_tools = []
    for at in analyzer_pats:
        for rl in run_labels:
            sample_list = _make_stack_sample_list(rl)
            tool = ppt.FSStackPlotter(
                "DataMC_" + at.pattern + "_" + rl
            )
            tool.filter_dict = {
                "analyzer":at,
                "sample": sample_list
            }
            list_of_tools.append(tool)
    return list_of_tools

def _make_stack_sample_list(run_label = None):
    """Returns list of sample names."""
    sample_list = settings.samples_stack
    # reject all non matching data samples.
    if run_label:
        data_sample_names = settings.data_samples().keys()
        sample_list = filter(
            lambda x: not (x in data_sample_names),
            settings.samples_stack
        )
        sample_list.append(run_label)
    return sample_list


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


