"""
This file contains the samples located on pcac3b04 and cern afs.
Cross sections in picobarns.
Luminosity in inverse picobarns.
"""

import cmstoolsac3b.sample as smp

path_pc = "/user/tholen/eventFiles/fromGrid20130502/"

class whiz2to5(smp.Sample):
    legend      = "t#bar{t}#gamma signal"
    x_sec       = 908.1 * 2.0
    n_events    = 1080000
    input_files = path_pc + "whiz2to5.root"

class T_t(smp.Sample):
    legend      = "Single Top"
    x_sec       = 56.4
    n_events    = 99876
    input_files = path_pc + 'T_t.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class Tbar_t(smp.Sample):
    legend      = "Single Top"
    x_sec       = 30.7
    n_events    = 1935072
    input_files =path_pc + 'Tbar_t.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class T_tW(smp.Sample):
    legend      = "Single Top"
    x_sec       = 11.1
    n_events    = 497658
    input_files = path_pc + 'T_tW.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class Tbar_tW(smp.Sample):
    legend      = "Single Top"
    x_sec       = 11.1
    n_events    = 5083
    input_files = path_pc + 'Tbar_tW.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class TTJets(smp.Sample):
    legend      = "t#bar{t} inclusive"
# Kindonakis https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat8TeV
    x_sec       = 234.
    n_events    = 6923750
    input_files = map(
        lambda x: path_pc + x + ".root",
        ['TTJets1', 'TTJets2' ,'TTJets3' , 'TTJets4', 'TTJets5']
    )
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis", "photonsource":"patPhotons", "muonsource":"tightmuons"}

class WJets(smp.Sample):
    legend      = "W + Jets"
    x_sec       = 37509.0
    n_events    = 57709905 # * 0.52836249 # problems running over all events
    input_files = path_pc + 'WJets.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class DYJets(smp.Sample):
    legend      = "DY + Jets"
    x_sec       = 3503.71
    n_events    = 30459503
    input_files = path_pc + 'DYJets.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class RunA(smp.Sample):
    is_data     = True
    legend      = "Data"
    lumi        = 806.227 #pixelLumi
    #lumi        = 808.472 #lumiCalc2
    input_files = path_pc + 'RunA.root'
    cfg_builtin = {"sample":"Run2012A-13Jul2012"}

class RunA_rec(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = 82.521#pixelLumi
    lumi        = 82.136 #lumiCalc2
    input_files = path_pc + 'RunA_rec.root'
    cfg_builtin = {"sample":"recover06Aug2012","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class RunB(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = 4446. #pixelLumi
    lumi        = 4429. #lumiCalc2
    input_files = path_pc + 'RunB.root'
    cfg_builtin = {"sample":"Run2012B-13Jul2012","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class RunC(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 6392. #lumiCalc2
    input_files = path_pc + 'RunC.root'
    cfg_builtin = {"sample":"Run2012C-PromptReco-v2","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class RunC_rec(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 134.242 #lumiCalc2
    input_files = path_pc + 'RunC_rec.root'
    cfg_builtin = {"sample":"Run2012C-EcalRecover_11Dec2012","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class RunC_aug(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 495.003 #lumiCalc2
    input_files = path_pc + 'RunC_aug.root'
    cfg_builtin = {"sample":"Run2012C-24AugSynch","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class RunD(smp.Sample):
    is_data     = True
    legend      = "Data"
    #lumi        = #pixelLumi
    lumi        = 6689. #lumiCalc2
    input_files = path_pc + 'RunD.root'
    cfg_builtin = {"sample":"Run2012D-PromptReco-v1","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}


