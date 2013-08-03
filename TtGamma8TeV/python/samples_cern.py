"""
This file contains the samples located on pcac3b04 and cern afs.
Cross sections in picobarns.
Luminosity in inverse picobarns.
"""

import cmstoolsac3b.sample as smp

# this is already set as default in the cmssw configs.
import cmstoolsac3b.settings as settings
settings.cfg_common_builtins.update({
     "puWeight"     : "PUWeightTrue",
     "skipChecks"   : True
})

#path_pc = "file:/user/tholen/eventFiles/fromGrid20130502/"
path_pc = "file:/disk1/tholen/eventFiles/fromGrid20130618/"

ttbar_xsec = settings.ttbar_xsec
ttbar_xsec_err = settings.ttbar_xsec_err

class whiz2to5(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t}#gamma (Signal)"
        self.x_sec       = .9081 * 2.0
        self.n_events    = 1074860
        self.input_files = path_pc + "whiz_*.root" # n_events!!!
        self.cfg_builtin = {"preSelOpt": "go4Whiz"}
        super(whiz2to5, self).__init__()

class T_t(smp.Sample):
    def __init__(self):
        self.legend      = "Single Top"
        self.x_sec       = 56.4
        self.n_events    = 99876
        self.input_files = path_pc + 'T_t_*.root'
        super(T_t, self).__init__()

class Tbar_t(smp.Sample):
    def __init__(self):
        self.legend      = "Single Top"
        self.x_sec       = 30.7
        self.n_events    = 1935072
        self.input_files = path_pc + 'Tbar_t_*.root'
        super(Tbar_t, self).__init__()

class T_tW(smp.Sample):
    def __init__(self):
        self.legend      = "Single Top"
        self.x_sec       = 11.1
        self.n_events    = 497658
        self.input_files = path_pc + 'T_tW_*.root'
        self.cfg_add_lines = ['process.source.eventsToSkip = cms.untracked.VEventRange("1:1085:325342-1:1085:325342")']
        super(T_tW, self).__init__()

class Tbar_tW(smp.Sample):
    def __init__(self):
        self.legend      = "Single Top"
        self.x_sec       = 11.1
        self.n_events    = 493460
        self.input_files = path_pc + 'Tbar_tW_*.root'
        super(Tbar_tW, self).__init__()

# Kindonakis https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat8TeV
class TTJetsSignal(smp.Sample):
    def __init__(self):
        self.enable      = False
        self.legend      = "t#bar{t}#gamma (Signal)"
        self.x_sec       = ttbar_xsec
        self.n_events    = 6854514
        self.input_files = path_pc + 'TTJets_*.root'
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
        super(TTJetsSignal, self).__init__()

class TTJets(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t} inclusive"
        self.x_sec       = ttbar_xsec
        self.n_events    = 6854514
        self.input_files = path_pc + 'TTJets_*.root'
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
    #    self.cfg_add_lines = ['process.source.eventsToSkip = cms.untracked.VEventRange("1:58828:17644617-1:58828:17644617")']
        super(TTJets, self).__init__()

class TTNLO(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t} inclusive"
        self.x_sec       = ttbar_xsec
        self.n_events    = 4900000
        self.input_files = path_pc + 'TTNLO_*.root'
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
        self.cfg_add_lines = ["process.puWeight.isMCatNLO=cms.untracked.bool(True)"]
        super(TTNLO, self).__init__()

class TTNLOSignal(smp.Sample):
    def __init__(self):
        self.enable      = False
        self.legend      = "t#bar{t}#gamma (Signal)"
        self.x_sec       = ttbar_xsec
        self.n_events    = 4900000
        self.input_files = path_pc + 'TTNLO_*.root'
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
        self.cfg_add_lines = ["process.puWeight.isMCatNLO=cms.untracked.bool(True)"]
        super(TTNLOSignal, self).__init__()

class WJets(smp.Sample):
    def __init__(self):
        self.legend      = "W + Jets"
        self.x_sec       = 37509.
        self.n_events    = 57709905
        self.input_files = path_pc + 'WJets_*.root'
        super(WJets, self).__init__()

class DYJets(smp.Sample):
    def __init__(self):
        self.legend      = "DY + Jets"
        self.x_sec       = 3503.71
        self.n_events    = 30307207
        self.input_files = path_pc + 'DYJets_*.root'
        super(DYJets, self).__init__()

class RunA(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 889.301 #lumiCalc2
        self.input_files = path_pc + 'RunA_*.root'
        self.cfg_builtin = {}
        super(RunA, self).__init__()

class RunB(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 4425.7 #558.738 + 3867. #lumiCalc2
        self.input_files = path_pc + 'RunB_*.root'
        self.cfg_builtin = {}
        super(RunB, self).__init__()

class RunC(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 7147.7 #lumiCalc2
        self.input_files = path_pc + 'RunC_*.root'
        self.cfg_builtin = {}
        super(RunC, self).__init__()

class RunD(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 7318. #lumiCalc2
        self.input_files = path_pc + 'RunD_*.root'
        self.cfg_builtin = {}
        super(RunD, self).__init__()

