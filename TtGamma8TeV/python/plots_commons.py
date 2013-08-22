
import os, shutil
import cmstoolsac3b.rendering as rnd
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.wrappers as wrappers

class SimpleTitleBox(rnd.TitleBox):
    def make_title(self):
        return "      CMS Preliminary #sqrt{s}=8 TeV  "


class LumiTitleBox(rnd.TitleBox):
    def make_title(self):
        return "      CMS Preliminary  L="\
               + str(round(self.renderers[0].lumi/1000.,1))\
               + " fb^{-1} at #sqrt{s}=8 TeV"


class PurityCount(ppc.PostProcTool):
    cnt_name = None

    def get_purity_counts(self, c):
        for smp in settings.mc_samples().itervalues():
            l = smp.legend
            c.mc_sum  += smp.log_event_counts[self.cnt_name] / smp.lumi
            if l == "t#bar{t}#gamma (Signal)":
                c.mc_ttgam  += smp.log_event_counts[self.cnt_name] / smp.lumi

    def run(self):
        self.result = wrappers.Wrapper()
        r           = self.result
        r.mc_sum    = 0.
        r.mc_ttgam  = 0.

        self.get_purity_counts(r)
        r.pur_ttgam = r.mc_ttgam / r.mc_sum

class TightIdPurityCount(PurityCount):
    cnt_name = "FullTightIDCount,"

class RealTightIdPurityCount(PurityCount):
    cnt_name = "realFullTightIDCount,"


def count_ttgamma_photons(wrps, sub_tot_list_ref):
    for w in wrps:
        sub_tot_list_ref[1] += w.histo.Integral()
        if w.legend == "t#bar{t}#gamma (Signal)":
            sub_tot_list_ref[0] += w.histo.Integral()
        yield w

def copy_tex_to_target_dir(obj):
    if not obj.target_dir: return
    obj.message("INFO Copying *.tex to " + obj.target_dir)
    for cwd, dirs, files in os.walk(obj.plot_output_dir):
        for f in files:
            if f[-4:] == ".tex":
                shutil.copy2(
                    obj.plot_output_dir + f,
                    obj.target_dir
                )
        break

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
settings.colors = colors

settings.stacking_order = [
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
pn["preselected"]               = "presel."
pn["etcut"]                     = "E_{T}"
pn["etaEB"]                     = "|#eta|"
pn["passEleVeto"]               = "e^{#pm} veto"
pn["hadTowOverEm"]              = "H / E"
pn["sihihEB"]                   = "#sigma_{i#eta i#eta}"
pn["chargedHadronIsoEB"]        = "hadr. iso"
pn["neutralHadronIsoEB"]        = "neutr. iso"
pn["photonIsoEB"]               = "pho. iso"
pn["drmuon"]                    = "#DeltaR(#gamma, #mu)"
pn["drjet"]                     = "#DeltaR(#gamma, j)"

pn["presel._tex"             ]    = "presel."
pn["E_{T}_tex"               ]    = "$E_{T}$"
pn["|#eta|_tex"              ]    = "$|\eta|$"
pn["e^{#pm} veto_tex"        ]    = r"$e^\pm$ veto"
pn["H / E_tex"               ]    = "H / E"
pn["#sigma_{i#eta i#eta}_tex"]    = r"$\sigma_{i\eta i\eta}$"
pn["hadr. iso_tex"           ]    = "hadr. iso"
pn["neutr. iso_tex"          ]    = "neutr. iso"
pn["pho. iso_tex"            ]    = "pho. iso"
pn["#DeltaR(#gamma, #mu)_tex"]    = r"$\Delta R(\gamma, \mu)$"
pn["#DeltaR(#gamma, j)_tex"  ]    = r"$\Delta R(\gamma, j)$"

pn["realTemplateSihih"]         = "real"
pn["fakeTemplateSihih"]         = "fake"
pn["realTemplateChHadIso"]      = "real"
pn["fakeTemplateChHadIso"]      = "fake"

pn.update({
    "SysIsrFsr"             : "sho./hadr.",
    "SysMCatNLO"            : r"generator", #. \MCATNLO",
    "SysMadgraph"           : r"generator", #. \MADGRAPH",
    "SysOverlapDRCut"       : "overlap removal",
    "SysPU"                 : "pileup",
    "SysPhotonETCut"        : r"$\epsilon_\gamma \;(\et)$",
    "SysSelEffSig"          : r"$\epsilon_\gamma \;(\sigma_{\rm sig})$",
    "SysSelEffBkg"          : r"$\epsilon_\gamma \;(\sigma_{\rm bkg})$",
})

pn.update({
    "XsecCalculatorSihih"       : r"$\sigma_{i\eta i\eta}$ fit",
    "XsecCalculatorSihihShift"  : r"$\sigma_{i\eta i\eta}$ fit (+shift)",
    "XsecCalculatorChHadIso"    : "hadr. iso fit",
    "XsecCalculatorABCD"        : "ABCD",
    "XsecCalculatorABCDMC"      : "ABCD (on MC)",
    "XsecCalculatorShilpi"      : "fr",
    "XsecCalculatorShilpiMC"    : "fr (on MC)",
    "XsecCalculatorShilpiCheck" : "MC truth",
})

settings.pretty_names = pn

settings.rootfile_postfixes = [".root", ".png", ".eps"]