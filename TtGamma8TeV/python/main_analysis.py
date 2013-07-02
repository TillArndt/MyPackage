
#import sys
#sys.path.append("/home/home2/institut_3b/tholen/installs/pycharm-2.0.2/pycharm-debug.egg")
#from pydev import pydevd
#pydevd.settrace('localhost', port=22022, suspend=False)

# DEAR PEDESTRIAN: http://github.com/heinzK1X/CMSToolsAC3b

import cmstoolsac3b.settings as settings
import cmstoolsac3b.main as main
from cmstoolsac3b.sample import load_samples
import samples_cern
settings.samples = {}
settings.samples.update(load_samples(samples_cern))
settings.active_samples = settings.samples.keys() # add all MC and data for stacking
settings.active_samples.remove("TTNLO")
settings.active_samples.remove("TTNLOSignal")

import ROOT
colors = dict()
colors["t#bar{t}#gamma #mu+Jets (Signal)"]  = ROOT.kRed + 1
colors["t#bar{t}#gamma (Signal)"]           = ROOT.kRed + 1
colors["t#bar{t} inclusive"]                = ROOT.kAzure + 7
colors["W + Jets"]                          = ROOT.kSpring + 8
colors["Z + Jets"]                          = ROOT.kSpring + 5
colors["DY + Jets"]                         = ROOT.kSpring + 5
colors["Single Top"]                        = ROOT.kOrange + 2
colors["QCD"]                               = ROOT.kYellow + 2

stacking_order = [
    "t#bar{t}#gamma #mu+Jets (Signal)",
    "t#bar{t}#gamma (Signal)",
    "QCD",
    "Z + Jets",
    "DY + Jets",
    "W + Jets",
    "Single Top",
    "t#bar{t} inclusive",
]

pn = dict()
pn["photonInputDummy"]              = "preselected"
pn["largeEtFilter"]                 = "large e_{T}"
pn["cocFilter"]                     = "#DeltaR(photon, jet/#mu)"
pn["tightIDFilter"]                 = "tight photon ID"
pn["PhotonFilteta"]                 = "#eta"
pn["PhotonFiltjurassicecaliso"]     = "ecal iso"
pn["PhotonFilthaspixelseeds"]       = "pixelseed"
pn["PhotonFilthcaliso"]             = "hcal iso"
pn["PhotonFiltetcut"]               = "E_{T}"
pn["PhotonFiltsigmaietaieta"]       = "#sigma_{i #eta i #eta}"
pn["PhotonFilthollowconetrackiso"]  = "track iso"
pn["PhotonFiltetawidth"]            = "#eta witdh"
pn["PhotonFilthadronicoverem"]      = "H/E"
pn["PhotonFiltdrjet"]               = "#DeltaR(photon, jet)"
pn["PhotonFiltdrmuon"]              = "#DeltaR(photon, #mu)"
pn["PhotonFiltptrelDrjet"]          = "E_{T,photon} / p_{T,jet}"
pn["realTemplateSihih"]             = "real photons"
pn["fakeTemplateSihih"]             = "fake photons"
pn["realTemplateChHadIso"]          = "real photons"
pn["fakeTemplateChHadIso"]          = "fake photons"
settings.pretty_names = pn

import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.postproctools as ppt
import plots_ME_overlap
import plots_data_mc_comp
import plots_cutflow
import plots_template_fit
import plots_xsec
settings.web_target_dir = "/afs/cern.ch/work/h/htholen/public/www/"

cutflow_tools = ppc.PostProcChain("CutflowTools", [
    plots_cutflow.CutflowHistos,
    plots_cutflow.CutflowStack,
    plots_cutflow.CutflowTable,
])

post_proc_tools = [
    ppt.UnfinishedSampleRemover(True),
#    ppt.SampleEventCount,
]
post_proc_tools += plots_data_mc_comp.generate_data_mc_comp_tools()
post_proc_tools += [
#    plots_ME_overlap.MEOverlapComp,
    cutflow_tools,
    plots_template_fit.TemplateFitTool,
    plots_xsec.XsecCalculator,
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
    ppt.SimpleWebCreator,
    sys_uncert.ResultDumper
]


if __name__ == '__main__':
    main.main(
        post_proc_tools = post_proc_tools,
        max_num_processes = 4,
        try_reuse_results = True,
#        suppress_cmsRun_exec = True,
        colors = colors,
        stacking_order = stacking_order,
        rootfile_postfixes = [".root", ".png"],
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_photon_selection",
    )


