
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.generators as gen
import cmstoolsac3b.rendering as rnd
import itertools
import re

import plots_ME_overlap

def make_list_of_tools():
    tools = []
    tools += generate_data_mc_comp_tools()
    tools += [plots_ME_overlap.OverlapComparison]

def generate_data_mc_comp_tools():
    """
    Generates postproctools by subclassing from ptt.FSStackPlotter.
    Walks over all samples and specific analyzer tokens.
    """
    #run_labels = settings.data_samples().keys()
    #run_labels.append(None) # all runs
    run_labels = [None]
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


