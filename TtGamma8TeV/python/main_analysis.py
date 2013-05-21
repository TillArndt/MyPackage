
#import sys
#sys.path.append("/home/home2/institut_3b/tholen/installs/pycharm-2.0.2/pycharm-debug.egg")
#from pydev import pydevd
#pydevd.settrace('localhost', port=22022, suspend=False)

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

import main_plot_tools
post_proc_tools = main_plot_tools.make_list_of_tools()

if __name__ == '__main__':
    cmstoolsac3b.main.main(
#        post_proc_tools = post_proc_tools,
        max_num_processes=3,
        samples=samples,
        try_reuse_results=True,
#        suppress_cmsRun_exec=True,
        colors = colors,
        stacking_order = stacking_order,
        rootfile_postfixes = [".root", ".png"],
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_photon_selection",
    )


