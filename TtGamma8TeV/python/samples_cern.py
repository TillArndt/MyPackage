"""
This file contains the samples located on pcac3b04 and cern afs.
Cross sections in picobarns.
Luminosity in inverse picobarns.
"""

import cmstoolsac3b.sample as smp

# this is already set as default in the cmssw configs.
import cmstoolsac3b.settings as settings

path_pc = settings.sample_data_path
postfix = "/*.root"

ttbar_xsec = settings.ttbar_xsec
ttbar_xsec_err = settings.ttbar_xsec_err


class MadG_2to7(smp.Sample):
    def __init__(self):
	self.legend      = "t#bar{t}#gamma (Madgraph,Signal)"
	self.x_sec       = 0.9387
	self.n_events    = 1000000
        self.input_files = path_pc + "MadG_2to7" + postfix
        self.cfg_builtin = {"preSelOpt":"MadG_Signal"}
        super(MadG_2to7, self).__init__()

class whiz2to5(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t}#gamma (Signal)"
        self.x_sec       = .9081 * 2.0
        self.n_events    = 1074860
        self.input_files = path_pc + "WHIZ" + postfix
        self.cfg_builtin = {"preSelOpt": "go4Whiz"}
        super(whiz2to5, self).__init__()


class whiz2to5_PDF(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t}#gamma (Signal)"
        self.x_sec       = .9081 * 2.0
        self.n_events    = 1039890
        self.input_files = path_pc + "WHIZPDF" + postfix
        self.cfg_builtin = {"preSelOpt": "go4Whiz"}
        super(whiz2to5_PDF, self).__init__()


class T_t(smp.Sample):
    def __init__(self):
        self.legend      = "Single top"
        self.x_sec       = 56.4
        self.n_events    = 99876
        self.input_files = path_pc + 'T_t' + postfix
        super(T_t, self).__init__()


class Tbar_t(smp.Sample):
    def __init__(self):
        self.legend      = "Single top"
        self.x_sec       = 30.7
        self.n_events    = 1935072
        self.input_files = path_pc + 'Tbar_t' + postfix
        super(Tbar_t, self).__init__()


class T_tW(smp.Sample):
    def __init__(self):
        self.legend      = "Single top"
        self.x_sec       = 11.1
        self.n_events    = 497658
        self.input_files = path_pc + 'T_tW' + postfix
        self.cfg_add_lines = ['process.source.eventsToSkip = cms.untracked.VEventRange("1:1085:325342-1:1085:325342")']
        super(T_tW, self).__init__()


class Tbar_tW(smp.Sample):
    def __init__(self):
        self.legend      = "Single top"
        self.x_sec       = 11.1
        self.n_events    = 493460
        self.input_files = path_pc + 'Tbar_tW' + postfix
        super(Tbar_tW, self).__init__()


class TTPoPy(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t} inclusive"
        self.x_sec       = ttbar_xsec
        self.n_events    = 6474753
        self.input_files = path_pc + 'TTPoPy' + postfix
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
        super(TTPoPy, self).__init__()


class TTPoHe(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t} inclusive"
        self.x_sec       = ttbar_xsec
        self.n_events    = 7000000
        self.input_files = path_pc + 'TTPoHe' + postfix
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
        super(TTPoHe, self).__init__()


class TTMadG(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t} inclusive"
        self.x_sec       = ttbar_xsec
        self.n_events    = 6854514
        self.input_files = path_pc + 'TTJets' + postfix
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
        #self.cfg_add_lines = ['process.source.eventsToSkip = cms.untracked.VEventRange("1:58828:17644617-1:58828:17644617")']
        super(TTMadG, self).__init__()


class TTMCNLO(smp.Sample):
    def __init__(self):
        self.legend      = "t#bar{t} inclusive"
        self.x_sec       = ttbar_xsec
        self.n_events    = 4900000
        self.input_files = path_pc + 'TTNLO' + postfix
        self.cfg_builtin = {"preSelOpt": "doOverlapRemoval"}
        self.cfg_add_lines = [
            "process.weightComb.src.append(cms.InputTag('MCatNLOWeight'))",
            "process.weightCombSequence.insert(1, process.MCatNLOWeight)"
        ]
        super(TTMCNLO, self).__init__()


class TTGamRD1(smp.Sample):
    def __init__(self):
        self.x_sec       = 1.6
        self.n_events    = 1719954
        self.input_files = path_pc + "TTGamRD1" + postfix
        super(TTGamRD1, self).__init__()


class TTJeRD1(smp.Sample):
    def __init__(self):
        self.legend      = "Fake Photons"
        self.x_sec       = ttbar_xsec
        self.n_events    = 6621325
        self.input_files = path_pc + "TTJetsRD1" + postfix
        super(TTJeRD1, self).__init__()


class WJets(smp.Sample):
    def __init__(self):
        self.legend      = "W + Jets"
        self.x_sec       = 37509.
        self.n_events    = 57709905
        self.input_files = path_pc + 'WJets' + postfix
        super(WJets, self).__init__()


class DYJets(smp.Sample):
    def __init__(self):
        self.legend      = "DY + Jets"
        self.x_sec       = 3503.71
        self.n_events    = 30307207
        self.input_files = path_pc + 'DYJets' + postfix
        super(DYJets, self).__init__()


class RunA(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 889.3 #lumiCalc2
        self.input_files = path_pc + 'RunA' + postfix
        self.cfg_builtin = {}
        super(RunA, self).__init__()


class RunB(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 4425.7 #558.738 + 3867. #lumiCalc2
        self.input_files = path_pc + 'RunB' + postfix
        self.cfg_builtin = {}
        super(RunB, self).__init__()


class RunC(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 7147.7 #lumiCalc2
        self.input_files = path_pc + 'RunC' + postfix
        self.cfg_builtin = {}
        super(RunC, self).__init__()


class RunD(smp.Sample):
    def __init__(self):
        self.is_data     = True
        self.legend      = "Data"
        self.lumi        = 7318. - 68.8 #lumiCalc2 # and correct to value from pixelLumiCalc
        self.input_files = path_pc + 'RunD' + postfix
        self.cfg_builtin = {}
        super(RunD, self).__init__()


