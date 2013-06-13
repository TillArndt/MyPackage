"""
This file contains the samples located on pcac3b04 and cern afs.
Cross sections in picobarns.
Luminosity in inverse picobarns.
"""

import cmstoolsac3b.sample as smp

# this is already set as default in the cmssw configs.
import cmstoolsac3b.settings as settings
settings.cfg_common_builtins.update({
#    "jetsource"    : "selectedPatJetsForAnalysis",
#    "photonsource" : "patPhotons",
#    "muonsource"   : "tightmuons",
     "puWeight"     : "PUWeightTrue",
     "skipChecks"   : True
})

#path_pc = "file:/user/tholen/eventFiles/fromGrid20130502/"
path_pc = "file:/disk1/tholen/eventFiles/fromGrid20130601/"

class whiz2to5_1(smp.Sample):
    legend      = "t#bar{t}#gamma (Signal)"
    x_sec       = 908.1 * 2.0
    n_events    = 1080000 * 0.25
    input_files = path_pc + "whiz2to5_1.root" # n_events!!!
    cfg_builtin = {"preSelOpt": "go4Whiz"}

class whiz2to5_2(smp.Sample):
    legend      = "t#bar{t}#gamma (Signal)"
    x_sec       = 908.1 * 2.0
    n_events    = 1080000 * 0.25
    input_files = path_pc + "whiz2to5_2.root" # n_events!!!
    cfg_builtin = {"preSelOpt": "go4Whiz"}

class whiz2to5_3(smp.Sample):
    legend      = "t#bar{t}#gamma (Signal)"
    x_sec       = 908.1 * 2.0
    n_events    = 1080000 * 0.25
    input_files = path_pc + "whiz2to5_3.root" # n_events!!!
    cfg_builtin = {"preSelOpt": "go4Whiz"}

class whiz2to5_4(smp.Sample):
    legend      = "t#bar{t}#gamma (Signal)"
    x_sec       = 908.1 * 2.0
    n_events    = 1080000 * 0.25
    input_files = path_pc + "whiz2to5_4.root" # n_events!!!
    cfg_builtin = {"preSelOpt": "go4Whiz"}

class T_t(smp.Sample):
    legend      = "Single Top"
    x_sec       = 56.4
    n_events    = 99876
    input_files = path_pc + 'T_t.root'

class Tbar_t(smp.Sample):
    legend      = "Single Top"
    x_sec       = 30.7
    n_events    = 1935072
    input_files =path_pc + 'Tbar_t.root'

class T_tW(smp.Sample):
    legend      = "Single Top"
    x_sec       = 11.1
    n_events    = 497658
    input_files = path_pc + 'T_tW.root'
    cfg_add_lines = ['process.source.eventsToSkip = cms.untracked.VEventRange("1:1085:325342-1:1085:325342")']

class Tbar_tW(smp.Sample):
    legend      = "Single Top"
    x_sec       = 11.1
    n_events    = 5083
    input_files = path_pc + 'Tbar_tW.root'

# Kindonakis https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat8TeV
class TTJetsSignal(smp.Sample):
    legend      = "t#bar{t}#gamma (Signal)"
    x_sec       = 234.
    n_events    = 6923750 * 0.6
    input_files = map(
        lambda x: path_pc + x + ".root",
        ['TTJets1', 'TTJets2' ,'TTJets3', 'TTJets4', 'TTJets5'] # n_events!!!
    )
    cfg_builtin = {"preSelOpt": "go4Signal"}

class TTJets(smp.Sample):
    legend      = "t#bar{t} inclusive"
    x_sec       = 234.
    n_events    = 6923750
    input_files = map(
        lambda x: path_pc + x + ".root",
        ['TTJets1', 'TTJets2' ,'TTJets3', 'TTJets4', 'TTJets5'] # n_events!!!
    )
    cfg_builtin = {"preSelOpt": "go4Noise"}
    cfg_add_lines = ['process.source.eventsToSkip = cms.untracked.VEventRange("1:58828:17644617-1:58828:17644617")']

class WJets_1(smp.Sample):
    legend      = "W + Jets"
    x_sec       = 37509.0
    n_events    = 57709905 # * 0.52836249 # problems running over all events
    input_files = path_pc + 'WJets_1.root'

class WJets_2(smp.Sample):
    legend      = "W + Jets"
    x_sec       = 37509.0
    n_events    = 57709905 # * 0.52836249 # problems running over all events
    input_files = path_pc + 'WJets_2.root'

class DYJets_1(smp.Sample):
    legend      = "DY + Jets"
    x_sec       = 3503.71
    n_events    = 30459503
    input_files = path_pc + 'DYJets_1.root'

class DYJets_2(smp.Sample):
    legend      = "DY + Jets"
    x_sec       = 3503.71
    n_events    = 30459503
    input_files = path_pc + 'DYJets_2.root'

class RunA(smp.Sample):
    is_data     = True
    legend      = "Data"
    lumi        = 806.227 #pixelLumi
    #lumi        = 808.472 #lumiCalc2
    input_files = path_pc + 'RunA.root'
    cfg_builtin = {}

class RunA_rec(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = 82.521#pixelLumi
    lumi        = 82.136 #lumiCalc2
    input_files = path_pc + 'RunA_rec.root'
    cfg_builtin = {}

class RunB(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = 4446. #pixelLumi
    lumi        = 4429. #lumiCalc2
    input_files = path_pc + 'RunB.root'
    cfg_builtin = {}

class RunC(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 6392. #lumiCalc2
    input_files = path_pc + 'RunC.root'
    cfg_builtin = {}

class RunC_rec(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 134.242 #lumiCalc2
    input_files = path_pc + 'RunC_rec.root'
    cfg_builtin = {}

class RunC_aug(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 495.003 #lumiCalc2
    input_files = path_pc + 'RunC_aug.root'
    cfg_builtin = {}

class RunD(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 6689. #lumiCalc2
    input_files = path_pc + 'RunD.root'
    cfg_builtin = {}


