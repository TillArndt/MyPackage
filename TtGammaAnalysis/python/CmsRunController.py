
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
    colors["t#bar{t}#gamma #mu+Jets (Signal)"]  = ROOT.kRed + 1
    colors["t#bar{t}#gamma (Signal)"]           = ROOT.kRed + 1
    colors["t#bar{t} inclusive"]                = ROOT.kAzure + 7
    colors["W + Jets"]                          = ROOT.kSpring + 8
    colors["Z + Jets"]                          = ROOT.kSpring + 5
    colors["Single Top"]                        = ROOT.kOrange + 2
    colors["QCD"]                               = ROOT.kYellow + 2
    colors["q_{top} = 4/3"]                     = ROOT.kViolet + 8
    root_style.set_colors(colors)

    # Stacking Order (lowest first, also non-mc should be stated)
    order = []
    order.append("Data")
    order.append("q_{top} = 4/3")
    order.append("t#bar{t}#gamma #mu+Jets (Signal)")
    order.append("t#bar{t}#gamma (Signal)")
    order.append("QCD")
    order.append("Z + Jets")
    order.append("W + Jets")
    order.append("Single Top")
    order.append("t#bar{t} inclusive")
    root_style.set_stacking_order(order)

    # pretty names
    # use it like this: name = root_style.get_pretty_name(name)
    pn = dict()
    pn["photonInputDummy"]              = "preselected"
    pn["largeEtFilter"]                 = "large e_{T}"
    pn["cocFilter"]                     = "#DeltaR(photon, jet/#mu)"
    pn["tightIDFilter"]                 = "tight photon ID"
    pn["PhotonFilteta"]                 = "#eta"
    pn["PhotonFiltjurassicecaliso"]     = "jurassic iso"
    pn["PhotonFilthaspixelseeds"]       = "pixelseed"
    pn["PhotonFilthcaliso"]             = "hcal iso"
    pn["PhotonFiltetcut"]               = "E_{T}"
    pn["PhotonFiltsigmaietaieta"]       = "#sigma_{i #eta i #eta}"
    pn["PhotonFilthollowconetrackiso"]  = "hollow cone"
    pn["PhotonFiltetawidth"]            = "#eta witdh"
    pn["PhotonFilthadronicoverem"]      = "H/E"
    pn["PhotonFiltdrjet"]               = "#DeltaR(photon, jet)"
    pn["PhotonFiltdrmuon"]              = "#DeltaR(photon, #mu)"
    root_style.set_pretty_names(pn)

    # change directory names
    #root_style.DIR_FILESERVICE  = "outputFileService/"
    #root_style.DIR_LOGS         = "outputLogs/"
    #root_style.DIR_CONFS        = "outputConfs/"
    #root_style.DIR_PLOTS        = "outputPlots/"

    # add postfixes for canvas saving
    #root_style.canvas_postfixes.append('.eps')
    root_style.canvas_postfixes.append('.png')

    # list of post processing tools
    tools = []
    from UserCode.RWTH3b.cmsRunController.tools.CRCutflowParser import CRCutflowParser
    from UserCode.RWTH3b.cmsRunController.tools.CRHistoOverflow import CRHistoOverflow
    from UserCode.RWTH3b.cmsRunController.tools.CRHistoStacker import CRHistoStacker
    from UserCode.RWTH3b.cmsRunController.tools.CRHistoPlotter import CRHistoPlotter
    from UserCode.RWTH3b.cmsRunController.tools.CRHistoEfficiencies import CRHistoEfficiencies
    from UserCode.RWTH3b.cmsRunController.tools.CRTemplateHisto import CRTemplateHisto
    from MyPackage.TtGammaAnalysis.myTTGammaAnalysisTool import MyTTGammaAnalysisTool
    from MyPackage.TtGammaAnalysis.myTTGammaAnalysisToolV2 import MyTTGammaAnalysisToolV2
    #tools.append(CRHistoOverflow)
    #tools.append(CRHistoStacker)
    #tools.append(CRHistoPlotter)
    #tools.append(CRHistoEfficiencies)
    tools.append(CRTemplateHisto)
    #tools.append(MyTTGammaAnalysisTool)
    #tools.append(MyTTGammaAnalysisToolV2)

    # search paths for decorators
    modules = []
    modules.append("UserCode.RWTH3b.cmsRunController.tools.CRHistoStackerDecorators")
    modules.append("UserCode.RWTH3b.cmsRunController.tools.CRHistoPlotterDecorators")
    modules.append("UserCode.RWTH3b.cmsRunController.examples.BottomPlots")
    modules.append("UserCode.RWTH3b.cmsRunController.examples.HistoCosmetics")
    root_style.decorator_search_paths = modules

    # start working
    import UserCode.RWTH3b.cmsRunController.classes.CRController as controller
    controller.main(tools)

#TODO: read list of tools from ini file