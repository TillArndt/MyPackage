
from cmstoolsac3b.sample import load_samples
import samples_whizard
import samples_other
samples = {}
samples.update(load_samples(samples_whizard))
samples.update(load_samples(samples_other))

import main_plot_tools

import ROOT
colors = dict()
colors["t#bar{t}#gamma #mu+Jets (Signal)"]  = ROOT.kRed + 1
colors["t#bar{t}#gamma (Signal)"]           = ROOT.kRed + 1
colors["t#bar{t} inclusive"]                = ROOT.kAzure + 7
colors["W + Jets"]                          = ROOT.kSpring + 8
colors["Z + Jets"]                          = ROOT.kSpring + 5
colors["Single Top"]                        = ROOT.kOrange + 2
colors["QCD"]                               = ROOT.kYellow + 2

stacking_order = [
    "t#bar{t}#gamma #mu+Jets (Signal)",
    "t#bar{t}#gamma (Signal)",
    "QCD",
    "Single Top",
    "Z + Jets",
    "W + Jets",
    "t#bar{t} inclusive",
]

import cmstoolsac3b.main
if __name__ == '__main__':
    cmstoolsac3b.main.main(
        post_proc_tools=[
            main_plot_tools.CrtlFiltTool
        ],
        max_num_processes=3,
        samples=samples,
        try_reuse_results=True,
        #suppress_cmsRun_exec=True,
        colors = colors,
        stacking_order = stacking_order,
        rootfile_postfixes = [".root", ".png"],
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_photon_selection",
    )


