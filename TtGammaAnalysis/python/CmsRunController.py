
"""
This program manages cmsRun processes. It reads run information
from *.ini configuration files and starts cmsRun with proper
parameters.
"""

__author__ = 'Heiner Tholen'

import ROOT
from UserCode.RWTH3b.cmsRunController.classes.CRUtilities import CRShellUtility
from UserCode.RWTH3b.cmsRunController.classes.CRRootStyle import CRRootStyle
root_style = CRRootStyle()

if __name__ == '__main__':

    if CRShellUtility().do_utility_stuff():
        import sys
        sys.exit()

    # colors
    colors = dict()
    colors["Signal"]            = ROOT.kRed + 1
    colors["q_{top} = 4/3"]     = ROOT.kViolet + 8
    colors["Semi-#mu t#bart"]   = ROOT.kAzure + 7
    colors["W + Jets"]          = ROOT.kSpring + 8
    colors["Z + Jets"]          = ROOT.kSpring + 5
    colors["Single Top"]        = ROOT.kOrange + 2
    colors["QCD"]               = ROOT.kYellow + 2
    root_style.set_colors(colors)

    # Stacking Order (lowest first, also non-mc should be stated)
    order = []
    order.append("Data")
    order.append("q_{top} = 4/3")
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

    # change directory names
    #root_style.DIR_FILESERVICE  = "outputFileService"
    #root_style.DIR_LOGS         = "outputLogs"
    #root_style.DIR_CONFS        = "outputConfs"
    #root_style.DIR_PLOTS        = "outputPlots"

    # add postfixes for canvas saving
    root_style.canvas_postfixes.append('.png')

    # list of post processing tools
    tools = []
    from UserCode.RWTH3b.cmsRunController.tools.CRHistoOverflow import CRHistoOverflow
    from UserCode.RWTH3b.cmsRunController.tools.CRCutflowParser import CRCutflowParser
    from UserCode.RWTH3b.cmsRunController.tools.CRHistoStacker import CRHistoStacker
    from MyPackage.TtGammaAnalysis.myTTGammaAnalysisTool import MyTTGammaAnalysisTool
    tools.append(CRHistoOverflow)
    #tools.append(CRCutflowParser)
    tools.append(CRHistoStacker)
    tools.append(MyTTGammaAnalysisTool)

    # search paths for decorators
    modules = []
    modules.append("UserCode.RWTH3b.cmsRunController.tools.CRHistoStackerDecorators")
    modules.append("UserCode.RWTH3b.cmsRunController.examples.BottomPlots")
    modules.append("UserCode.RWTH3b.cmsRunController.examples.HistoCosmetics")
    root_style.decorator_search_paths = modules

    # start working
    import UserCode.RWTH3b.cmsRunController.classes.CRController as controller
    controller.main(tools)

