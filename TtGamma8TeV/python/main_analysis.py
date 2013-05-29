
#import sys
#sys.path.append("/home/home2/institut_3b/tholen/installs/pycharm-2.0.2/pycharm-debug.egg")
#from pydev import pydevd
#pydevd.settrace('localhost', port=22022, suspend=False)

# DEAR PEDESTRIAN: http://github.com/heinzK1X/CMSToolsAC3b

import cmstoolsac3b.main
from cmstoolsac3b.sample import load_samples
import cmstoolsac3b.settings as settings
import samples_cern
samples = {}
samples.update(load_samples(samples_cern))
settings.samples_stack = samples.keys() # add all MC and data for stacking


import ROOT
colors = dict()
colors["t#bar{t}#gamma #mu+Jets (Signal)"]  = ROOT.kRed + 1
colors["t#bar{t}#gamma (Signal)"]           = ROOT.kRed + 1
colors["t#bar{t} inclusive"]                = ROOT.kAzure + 7
colors["W + Jets"]                          = ROOT.kSpring + 8
colors["Z + Jets"]                          = ROOT.kSpring + 5
colors["DY + Jets"]                          = ROOT.kSpring + 5
colors["Single Top"]                        = ROOT.kOrange + 2
colors["QCD"]                               = ROOT.kYellow + 2

stacking_order = [
    "t#bar{t}#gamma #mu+Jets (Signal)",
    "t#bar{t}#gamma (Signal)",
    "QCD",
    "Single Top",
    "Z + Jets",
    "DY + Jets",
    "W + Jets",
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
settings.pretty_names = pn

import plots_ME_overlap
import plots_data_mc_comp
import plots_cutflow
import cmstoolsac3b.postproctools as ppt
post_proc_tools = plots_data_mc_comp.generate_data_mc_comp_tools()
post_proc_tools += [
    plots_ME_overlap.MEOverlapComp,
    plots_cutflow.CutflowHistos,
    plots_cutflow.CutflowStack,
    plots_cutflow.CutflowTable,
    ppt.SimpleWebCreator,
]

if __name__ == '__main__':
    cmstoolsac3b.main.main(
        post_proc_tools = post_proc_tools,
        max_num_processes = 3,
        samples = samples,
        try_reuse_results = True,
#        suppress_cmsRun_exec=True,
        colors = colors,
        stacking_order = stacking_order,
        rootfile_postfixes = [".root", ".png"],
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_photon_selection",
    )


