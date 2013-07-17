
#import sys
#sys.path.append("/home/home2/institut_3b/tholen/installs/pycharm-2.0.2/pycharm-debug.egg")
#from pydev import pydevd
#pydevd.settrace('localhost', port=22022, suspend=False)

# DEAR PEDESTRIAN: http://github.com/heinzK1X/CMSToolsAC3b

import cmstoolsac3b.main as main
import cmstoolsac3b.settings as settings
settings.ttbar_xsec = 245.8
settings.ttbar_xsec_err = 2.6
settings.ttbar_xsec_cms = 228.4
settings.ttbar_xsec_cms_stat = 9.0
settings.ttbar_xsec_cms_syst = ((+29.0)**2 + (-26.0)**2)**.5
settings.ttbar_xsec_cms_lum  = 10.0
settings.ttbar_xsec_cms_err = (
      settings.ttbar_xsec_cms_stat**2
    + settings.ttbar_xsec_cms_syst**2
    + settings.ttbar_xsec_cms_lum**2
)**.5

import plots_commons  # sets style related things
from cmstoolsac3b.sample import load_samples
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
import plots_counters
import plots_template_fit
import plots_xsec
import plots_summary

post_proc_tools = [
    ppt.UnfinishedSampleRemover(True),
#    plots_counters.SampleEventCount,
    plots_counters.CounterReader
]
post_proc_tools += plots_data_mc_comp.generate_data_mc_comp_tools()
post_proc_tools += [
#    plots_ME_overlap.MEOverlapComp,
    plots_cutflow.cutflow_chain,
    plots_template_fit.TemplateFitToolSihih,
    plots_template_fit.TemplateFitToolChHadIso,
    plots_xsec.XsecCalculatorSihih,
    ppt.HistoPoolClearer,
]

import sys_uncert
sys_uncert.makeSysSamplesPU()
sys_uncert.makeSysSamplesDRCut()
sys_uncert.makeSysSamplesETCut()

post_proc_tools += [
    sys_uncert.SysIsrFsr(None, post_proc_tools),
    sys_uncert.SysPU(None, post_proc_tools),
    sys_uncert.SysSelEffPlus(None, post_proc_tools),
    sys_uncert.SysSelEffMinus(None, post_proc_tools),
    sys_uncert.SysOverlapDRCutLow(None, post_proc_tools),
    sys_uncert.SysOverlapDRCutHigh(None, post_proc_tools),
    sys_uncert.SysPhotonETCutHigh(None, post_proc_tools),
    sys_uncert.SysPhotonETCutLow(None, post_proc_tools),
    sys_uncert.SysTemplateFit(None, post_proc_tools),
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


