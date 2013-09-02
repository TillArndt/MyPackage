
#import sys
#sys.path.append(
# "/home/home2/institut_3b/tholen/installs/pycharm-2.0.2/pycharm-debug.egg"
# )
#from pydev import pydevd
#pydevd.settrace('localhost', port=22022, suspend=False)

# DEAR PEDESTRIAN: http://github.com/heinzK1X/CMSToolsAC3b

import sys
import cmstoolsac3b.main as main
import cmstoolsac3b.settings as settings
settings.ttbar_xsec = 245.8
settings.ttbar_xsec_err = 2.6 * settings.ttbar_xsec
settings.ttbar_xsec_cms = 227.
settings.ttbar_xsec_cms_stat = 3.
settings.ttbar_xsec_cms_syst = 11.
settings.ttbar_xsec_cms_lum  = 10.
settings.ttbar_xsec_cms_err = (
      settings.ttbar_xsec_cms_stat**2
    + settings.ttbar_xsec_cms_syst**2
    + settings.ttbar_xsec_cms_lum**2
)**.5
settings.do_sys_uncert = False #not "--noSys" in sys.argv

import plots_commons  # sets style related things
from cmstoolsac3b.sample import load_samples
import samples_cern
settings.samples = {}
settings.samples.update(load_samples(samples_cern))
settings.active_samples = settings.samples.keys() # add all MC and data
settings.active_samples.remove("TTPoPy")
settings.active_samples.remove("TTMCNLO")
settings.active_samples.remove("TTMadG")
settings.active_samples.remove("TTGamRD1")
settings.active_samples.remove("TTJeRD1")
work = "/afs/cern.ch/work/h/htholen/"
cmsAN = work + "private/cmsPublishDir/cms_repo/notes/AN-13-195/trunk/"
settings.web_target_dir     = work + "public/www/MainAnalysis/"
settings.tex_target_dir     = cmsAN + "auto_snippets/"
settings.plot_target_dir    = cmsAN + "auto_images/"

import cmstoolsac3b.postproctools as ppt
import plots_ME_overlap
import plots_data_mc_comp
import plots_cutflow
import plots_counters
import plots_template_fit
import plots_xsec
import plots_summary
import plots_match_quality
import plots_ABCD
import plots_shilpi
import plots_templ_fit_closure

post_proc_sys = [
#    plots_ME_overlap.MEOverlapComp,
    plots_cutflow.cutflow_chain,
    plots_commons.TightIdPurityCount,
    plots_commons.RealTightIdPurityCount,
    plots_template_fit.TemplateFitTools,
#    plots_shilpi.ShilpiMethodTools,
#    plots_ABCD.RealPhotonsABCD,
#    plots_ABCD.RealPhotonsABCDMC,
    plots_xsec.XsecCalculators,
    ppt.HistoPoolClearer,
]

if settings.do_sys_uncert:
    import sys_uncert
    sys_uncert.makeSysSamplesPU()
    sys_uncert.makeSysSamplesTopPt()
    sys_uncert.makeSysSamplesDRCut()
    sys_uncert.makeSysSamplesETCut()
    sys_uncert.makeSysSamplesBTag()

post_proc_tools = [
    ppt.UnfinishedSampleRemover(True),
    plots_counters.CounterReader,
#    plots_counters.TopPtWeightNorm,
    plots_data_mc_comp.generate_data_mc_comp_tools(),
    plots_match_quality.MatchQualityStack,
]
post_proc_tools += post_proc_sys
if settings.do_sys_uncert:
    post_proc_tools += [
        sys_uncert.SysPU(None, post_proc_sys),
        sys_uncert.SysTopPt.push_tools(post_proc_sys),
        sys_uncert.SysSelEff.push_tools(post_proc_sys),
        sys_uncert.SysOverlapDRCut.push_tools(post_proc_sys),
        sys_uncert.SysPhotonETCut.push_tools(post_proc_sys),
        sys_uncert.SysBTags(None, post_proc_sys),
        sys_uncert.SysIsrFsr(None,
            post_proc_sys + [sys_uncert.SysMCatNLO(None, post_proc_sys)]
        ),
        sys_uncert.SysMadgraph(None, post_proc_sys),
        plots_summary.ResultSummaries,
        plots_summary.ResultTexifierMethodComp,
        plots_summary.ResultTexifier("XsecCalculatorSihihShift"),
    ]
post_proc_tools += [
    ppt.SimpleWebCreator,
#    plots_summary.RootPlotConverter,
#    plots_summary.CopyTool,
#    plots_summary.TexCompiler,
]

def drop_toolchain():
    settings.postprocessor.tool_chain = []

def analysis_main():
    main.main(
        post_proc_tools = post_proc_tools,
        max_num_processes = 4,
        try_reuse_results = True,
#        suppress_cmsRun_exec = True,
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_photon_selection",
    )

if __name__ == '__main__':
    analysis_main()
