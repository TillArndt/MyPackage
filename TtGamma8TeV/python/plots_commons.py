
import cmstoolsac3b.rendering as rnd
import cmstoolsac3b.settings as settings

class SimpleTitleBox(rnd.TitleBox):
    def make_title(self):
        return "      CMS work in progress #sqrt{s}=8 TeV  "

class LumiTitleBox(rnd.TitleBox):
    def make_title(self):
        return "      CMS work in progress  L="\
               + str(round(self.renderers[0].lumi/1000.,1))\
               + " fb^{-1} at #sqrt{s}=8 TeV"

settings.web_target_dir     = "/afs/cern.ch/work/h/htholen/public/www/"
settings.tex_target_dir     = "/afs/cern.ch/work/h/htholen/private/cmsPublishDir/cms_repo/notes/AN-13-195/trunk/auto_snippets/"
settings.plot_target_dir    = "/afs/cern.ch/work/h/htholen/private/cmsPublishDir/cms_repo/notes/AN-13-195/trunk/auto_images/"

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
settings.stacking_order = stacking_order

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
settings.pretty_names = pn

settings.rootfile_postfixes = [".root", ".png", ".eps"]