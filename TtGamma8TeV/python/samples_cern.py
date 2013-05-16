"""
This file contains the samples located on pcac3b04 and cern afs.
Cross sections in picobarns.
Luminosity in inverse picobarns.
"""

import cmstoolsac3b.sample as smp

# this is already set as default in the cmssw configs.
#import cmstoolsac3b.settings as settings
#settings.cfg_common_builtins.update({
#    "jetsource":"selectedPatJetsForAnalysis",
#    "photonsource":"patPhotons",
#    "muonsource":"tightmuons"
#})

path_pc = "file:/user/tholen/eventFiles/fromGrid20130502/"

class whiz2to5(smp.Sample):
    legend      = "t#bar{t}#gamma signal"
    x_sec       = 908.1 * 2.0
    n_events    = 1080000
    input_files = path_pc + "whiz2to5_1.root"

class T_t(smp.Sample):
    legend      = "Single Top"
    x_sec       = 56.4
    n_events    = 99876
    input_files = path_pc + 'T_t.root'
    cfg_builtin = {"preSelOpt":"go4Noise", }

class Tbar_t(smp.Sample):
    legend      = "Single Top"
    x_sec       = 30.7
    n_events    = 1935072
    input_files =path_pc + 'Tbar_t.root'
    cfg_builtin = {"preSelOpt":"go4Noise", }

class T_tW(smp.Sample):
    legend      = "Single Top"
    x_sec       = 11.1
    n_events    = 497658
    input_files = path_pc + 'T_tW.root'
    cfg_builtin = {"preSelOpt":"go4Noise", }

class Tbar_tW(smp.Sample):
    legend      = "Single Top"
    x_sec       = 11.1
    n_events    = 5083
    input_files = path_pc + 'Tbar_tW.root'
    cfg_builtin = {"preSelOpt":"go4Noise", }

class TTJets(smp.Sample):
    legend      = "t#bar{t} inclusive"
# Kindonakis https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat8TeV
    x_sec       = 234.
    n_events    = 6923750
    input_files = map(
        lambda x: path_pc + x + ".root",
        ['TTJets1', 'TTJets2' ,'TTJets3']# , 'TTJets4', 'TTJets5']
    )
    cfg_builtin = {"preSelOpt":"go4Noise", }

class WJets(smp.Sample):
    legend      = "W + Jets"
    x_sec       = 37509.0
    n_events    = 57709905 # * 0.52836249 # problems running over all events
    input_files = path_pc + 'WJets.root'
    cfg_builtin = {"preSelOpt":"go4Noise", }

class DYJets(smp.Sample):
    legend      = "DY + Jets"
    x_sec       = 3503.71
    n_events    = 30459503
    input_files = path_pc + 'DYJets.root'
    cfg_builtin = {"preSelOpt":"go4Noise", }

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


