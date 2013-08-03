
import cmstoolsac3b.sample as smp

path_pc = "file:/disk1/tholen/eventFiles/dataDrvSigTmplt/"

class DYJets(smp.Sample):
    enable = False
    legend      = "DY + Jets"
    x_sec       = 3503.71
    n_events    = 30307207
    input_files = path_pc + 'DYToMuMu.root'

class RunA(smp.Sample):
    is_data     = True
    legend      = "Data"
    lumi        = 889.301 #lumiCalc2
    input_files = path_pc + 'RunA/patTuple*.root'
    cfg_builtin = {}

class RunB(smp.Sample):
    is_data     = True
    legend      = "Data"
    lumi        = 4425.7 #558.738 + 3867. #lumiCalc2
    input_files = path_pc + 'RunB/patTuple*.root'
    cfg_builtin = {}

class RunC(smp.Sample):
    is_data     = True
    legend      = "Data"
    lumi        = 7147.7 #lumiCalc2
    input_files = path_pc + 'RunC/patTuple*.root'
    cfg_builtin = {}

class RunD(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 7318. #lumiCalc2
    input_files = path_pc + 'RunD/patTuple*.root'
    cfg_builtin = {}


