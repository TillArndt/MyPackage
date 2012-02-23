#!/net/software_cms/slc5_amd64_gcc434/cms/cmssw/CMSSW_4_2_8/external/slc5_amd64_gcc434/bin/python
#!/afs/cern.ch/cms/slc5_amd64_gcc434/cms/cmssw/CMSSW_4_2_8/external/slc5_amd64_gcc434/bin/python

"""
This program manages cmsRun processes. It reads run information
from *.ini configuration files and starts cmsRun with proper
parameters.

author: Heiner Tholen
"""

import ROOT
import MyPackage.TtGammaAnalysis.CmsRunController as controller
import MyPackage.TtGammaAnalysis.CmsRunKoolStyle as root_style

if __name__ == '__main__':

    # fill colors
    colors = dict()
    colors["Signal"]            = ROOT.kRed + 1
    colors["Semi-#mu t#bart"]   = ROOT.kAzure + 7
    colors["W + Jets"]          = ROOT.kSpring + 8
    colors["Z + Jets"]          = ROOT.kSpring + 5
    colors["WZ + Jets"]         = ROOT.kSpring + 2
    colors["Single Top"]        = ROOT.kOrange + 2
    colors["QCD"]               = ROOT.kYellow + 2
    root_style.set_fill_colors(colors)

    # Stacking Order (lowest first)
    order = []
    order.append("Data")
    order.append("Signal")
    order.append("QCD")
    order.append("Single Top")
    order.append("Z + Jets")
    order.append("W + Jets")
    order.append("Semi-#mu t#bart")
    root_style.set_stacking_order(order)

    # pretty names
    pn = dict()
    pn["photonInputDummy"]      = "preselected"
    pn["myLargePtPhotons"]      = "large p_{T}"
    pn["photonsWithTightID"]    = "tight photon ID"
    pn["removeCocFails"]        = "#DeltaR(photon, jet)"
    root_style.set_pretty_names(pn)

    # start working
    controller.main()

