
#import sys
#sys.path.append("/home/home2/institut_3b/tholen/installs/pycharm-2.0.2/pycharm-debug.egg")
#from pydev import pydevd
#pydevd.settrace('localhost', port=22022, suspend=False)

# DEAR PEDESTRIAN: http://github.com/heinzK1X/CMSToolsAC3b

import cmstoolsac3b.settings as settings
import cmstoolsac3b.main as main
from cmstoolsac3b.sample import load_samples
import plots_commons  # sets style related things

import samples_cern
settings.samples = {}
settings.samples.update(load_samples(samples_cern))
settings.active_samples = settings.samples.keys() # add all MC and data for stacking
settings.active_samples.remove("TTNLO")
settings.active_samples.remove("TTNLOSignal")

import cmstoolsac3b.postproctools as ppt
import plots_ME_overlap
import plots_data_mc_comp
import plots_cutflow
import plots_template_fit
import plots_xsec
import plots_summary

post_proc_tools = [
    ppt.UnfinishedSampleRemover(True),
#    ppt.SampleEventCount,
]
#post_proc_tools += plots_data_mc_comp.generate_data_mc_comp_tools()
post_proc_tools += [
#    plots_ME_overlap.MEOverlapComp,
    plots_cutflow.cutflow_chain,
    plots_template_fit.TemplateFitToolSihih,
    plots_template_fit.TemplateFitToolChHadIso,
    plots_xsec.XsecCalculator,
    ppt.HistoPoolClearer,
]

import sys_uncert
sys_uncert.makeSysSamplesPU()
sys_uncert.makeSysSamplesDRCut()
sys_uncert.makeSysSamplesETCut()

post_proc_tools += [
#    sys_uncert.SysIsrFsr(None, post_proc_tools),
#    sys_uncert.SysPU(None, post_proc_tools),
#    sys_uncert.SysSelEffPlus(None, post_proc_tools),
#    sys_uncert.SysSelEffMinus(None, post_proc_tools),
#    sys_uncert.SysOverlapDRCutLow(None, post_proc_tools),
#    sys_uncert.SysOverlapDRCutHigh(None, post_proc_tools),
#    sys_uncert.SysPhotonETCutHigh(None, post_proc_tools),
    sys_uncert.SysPhotonETCutLow(None, post_proc_tools),
    plots_summary.ResultSummary,
    ppt.SimpleWebCreator,
    plots_summary.ResultTexifier,
    plots_summary.RootPlotConverter,
    plots_summary.ResultSummary,
]


if __name__ == '__main__':
    main.main(
        post_proc_tools = post_proc_tools,
        max_num_processes = 4,
        try_reuse_results = True,
#        suppress_cmsRun_exec = True,
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_photon_selection",
    )


