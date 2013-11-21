
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
settings.ttbar_xsec_err = 9.634
settings.ttbar_xsec_cms = 227.
settings.ttbar_xsec_cms_stat = 3.
settings.ttbar_xsec_cms_syst = 11.
settings.ttbar_xsec_cms_lum  = 10.
settings.ttbar_xsec_cms_err = (
      settings.ttbar_xsec_cms_stat**2
    + settings.ttbar_xsec_cms_syst**2
    + settings.ttbar_xsec_cms_lum**2
)**.5
settings.do_sys_uncert = not "--noSys" in sys.argv

settings.max_num_processes = 4

import plots_commons  # sets style related things
from cmstoolsac3b.sample import load_samples
import samples_cern
settings.samples = {}
settings.samples.update(load_samples(samples_cern))
settings.active_samples = settings.samples.keys() # add all MC and data
settings.active_samples.remove("TTPoHe")
#settings.active_samples.remove("TTMadG")
settings.active_samples.remove("TTPoPy")
settings.active_samples.remove("TTMCNLO")
settings.active_samples.remove("TTGamRD1")
settings.active_samples.remove("TTJeRD1")
settings.active_samples.remove("whiz2to5_PDF")
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
import sys_uncert

post_proc_sys = [
#    plots_ME_overlap.MEOverlapComp,
    plots_commons.IdPurityCount,
    plots_commons.RealIdPurityCount,
    plots_template_fit.TemplateFitTools,
#    plots_shilpi.ShilpiMethodTools,
#    plots_ABCD.RealPhotonsABCD,
#    plots_ABCD.RealPhotonsABCDMC,
    plots_xsec.XsecCalculators,
]

if settings.do_sys_uncert:
    sys_uncert.makeSysSamplesPU()
    sys_uncert.makeSysSamplesJEC()
    sys_uncert.makeSysSamplesJER()
    sys_uncert.makeSysSamplesTopPt()
    sys_uncert.makeSysSamplesTrig()
    sys_uncert.makeSysSamplesDRCut()
    sys_uncert.makeSysSamplesETCut()
    sys_uncert.makeSysSamplesBTag()
    sys_uncert.makeSysSamplesBTagWeight()

post_proc_tools = [
    ppt.UnfinishedSampleRemover(True),
    plots_counters.CounterReader,
    plots_counters.TopPtWeightNorm,
    plots_cutflow.cutflow_chain,
    plots_data_mc_comp.generate_data_mc_comp_tools(),
    plots_match_quality.MatchQualityStack,
]
post_proc_tools += post_proc_sys
post_proc_tools += [plots_template_fit.TemplateFitPlots]
closure_seq = post_proc_sys[:]
if not plots_template_fit.do_dist_reweighting:
    closure_seq += [plots_templ_fit_closure.seq_sbid_MC]
    closure_seq += [plots_templ_fit_closure.seq_sbbkg_MC]
closure_seq += [plots_templ_fit_closure.seq_sbid_altMC]
closure_seq += [plots_templ_fit_closure.seq_sbbkg_altMC]
post_proc_tools += closure_seq
post_proc_tools += [sys_uncert.SysFit(
    None,
    [
        plots_template_fit.TemplateFitTools,
        plots_templ_fit_closure.sys_fit_sbbkg,
        plots_templ_fit_closure.sys_fit_sbid,
        plots_xsec.XsecCalculators,
    ]
)]
if "TTMadG" in settings.active_samples:
    post_proc_tools += [
        sys_uncert.SysTTPoPy(
            None,
            post_proc_sys + [sys_uncert.SysIsrFsr(
                None,
                post_proc_sys + [sys_uncert.SysMCatNLO(
                    None,
                    post_proc_sys
                )]
            )],
        ),
    ]
else:
    post_proc_tools += [
        sys_uncert.SysTTMadG(
            None,
            post_proc_sys
        ),
        sys_uncert.SysIsrFsr(
            None,
            post_proc_sys + [sys_uncert.SysMCatNLO(
                None,
                post_proc_sys
            )]
        ),
    ]

if settings.do_sys_uncert:
    post_proc_tools += [
        ppt.SimpleWebCreator, # see output before looong sys calculation
        sys_uncert.SysPU(None, post_proc_sys),
        sys_uncert.SysJEC(None, post_proc_sys),
        sys_uncert.SysJER(None, post_proc_sys),
        sys_uncert.SysTopPt.push_tools(post_proc_sys),
        sys_uncert.SysTrig.push_tools(post_proc_sys),
        sys_uncert.SysSelEff.push_tools(post_proc_sys),
        sys_uncert.SysOverlapDRCut.push_tools(post_proc_sys),
        sys_uncert.SysPhotonETCut.push_tools(post_proc_sys),
        sys_uncert.SysBTagWeight.push_tools(post_proc_sys),
        sys_uncert.SysBTags(None, post_proc_sys),
        sys_uncert.SysWhizPDF(None, post_proc_sys),
        plots_summary.ResultSummaries,
        plots_summary.ResultTexifier("XsecCalculatorChHadIsoSBID"),
    ]
post_proc_tools += [
    ppt.SimpleWebCreator,
    plots_summary.RootPlotConverter,
    plots_summary.CopyTool,
#    plots_summary.TexCompiler,
]


def drop_toolchain():
    settings.postprocessor.tool_chain = []

def analysis_main():
    main.main(
        post_proc_tools = post_proc_tools,
        try_reuse_results = True,
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_photon_selection",
    )

if __name__ == '__main__':
    analysis_main()
