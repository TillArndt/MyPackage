
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postproctools as ppt
import plots_commons as com
import re


def generate_data_mc_comp_tools():
    """
    Generates postproctools by subclassing from ptt.FSStackPlotter.
    Walks over all samples and specific analyzer tokens.
    """
    #run_labels = settings.data_samples().keys()
    #run_labels.append(None) # all runs
    run_labels = [""]
    analyzer_pats = [
        re.compile("CrtlPlot"),
        re.compile("Nm1Filt"),
#        re.compile("DataMCCompPhotons"),
#        re.compile("DataMCJetCheck"),
#        re.compile("DataMCMuonCheck"),
#        re.compile("DataMCPhotonCheck"),
#        re.compile("WeightsCheck"),
        ]
    list_of_tools = []
    for at in analyzer_pats:
        for rl in run_labels:
            sample_list = _make_stack_sample_list(rl)
            tool = ppt.FSStackPlotter(
                "DataMC_" + at.pattern + "_logscale" + rl
            )
            tool.filter_dict = {
                "analyzer": at,
                "sample": sample_list
            }
            tool.canvas_decorators.append(com.LumiTitleBox)
            tool.save_log_scale = True
            list_of_tools.append(tool)
            tool = ppt.FSStackPlotter(
                "DataMC_" + at.pattern + "_linscale" + rl
            )
            tool.filter_dict = {
                "analyzer": at,
                "sample": sample_list
            }
            tool.canvas_decorators.append(com.LumiTitleBox)
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
