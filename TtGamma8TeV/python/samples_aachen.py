"""
This file contains the skimed samples that are located in Aachen. The skim requires one btagged jet and saves only the good muon, jets and photon collections.
"""

import cmstoolsac3b.sample as smp

skim="skimPU"

class SingleToptWChTbar(smp.Sample):
    legend="Single Top"
    x_sec = 11.1
    n_events=5083
    input_files='file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/SingleTop-tWCh-TbarSynchSelMuJetsSkim.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class SingleToptChTbar(smp.Sample):
    legend = "Single Top"
    x_sec  =  30.7
    n_events = 1935072
    input_files ='file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/SingleTop-tCh-TbarSynchSelMuJetsSkim.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class SingleToptChT(smp.Sample):
    legend = "Single Top"
    x_sec  =  56.4
    n_events = 99876
    input_files = 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/SingleTop-tCh-TSynchSelMuJetsSkim.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class SingleToptWChT(smp.Sample):
    legend = "Single Top"
    x_sec  =  11.1
    n_events = 497658
    input_files = 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/SingleTop-tWCh-TSynchSelMuJetsSkim.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class TTbarSig(smp.Sample):
    legend = "t#bar{t} inclusive"
    x_sec  = 234 # Kindonakis https://twiki.cern.ch/twiki/bin/view/CMS/StandardModelCrossSectionsat8TeV
    n_events = 6923750
    input_files ='file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/TTbarSigSynchSelMuJetsSkim.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis", "photonsource":"patPhotons", "muonsource":"tightmuons"}

class WJets(smp.Sample):
    legend = "W + Jets"
    x_sec = 37509.0
    n_events = 57709905 * 0.5283624931656643 #problems running over all events of skim
    input_files = 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/WJetsSynchSelMuJetsSkim.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

class DYJets(smp.Sample):
    legend = "DY + Jets"
    x_sec = 3503.71
    n_events = 30459503
    input_files = 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/DYJetsSynchSelMuJetsSkim.root'
    cfg_builtin = {"preSelOpt":"go4Noise", "jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}

## class Run2012Arecover06Aug2012(smp.Sample):
##     legend="Data"
##     #lumi= 82.521#pixelLumi
##     lumi= 82.136 #lumiCalc2
##     cfg_builtin = {"sample":"recover06Aug2012","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}
##     input_files= 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/Run2012A-recover-06Aug2012SynchSelMuJetsSkim.root'
##     is_data=True

#class Run2012A13Jul2012(smp.Sample):
#    legend="Data"
#    lumi=806.227 #pixelLumi
#    #lumi=808.472 #lumiCalc2
#    cfg_builtin = {"sample":"Run2012A-13Jul2012"}
#    input_files= 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/Run2012A-13Jul2012SynchSelMuJetsSkim.root'
#    is_data=True

#class Run2012B13Jul2012(smp.Sample):
#    legend="Data"
#    #lumi= 4446 #pixelLumi
#    lumi= 4429 #lumiCalc2
#    cfg_builtin = {"sample":"Run2012B-13Jul2012","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}
#    input_files= 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/Run2012B-13Jul2012SynchSelMuJetsSkim.root'
#    is_data=True

## class Run2012CEcalRecover11Dec2012(smp.Sample):
##     legend="Data"
##     #lumi= #pixelLumi
##     lumi=  134.242 #lumiCalc2
##     cfg_builtin = {"sample":"Run2012C-EcalRecover_11Dec2012","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}
##     input_files= 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/Run2012C-EcalRecover_11Dec2012SynchSelMuJetsSkim.root'
##     is_data=True

## class Run2012C24AugSynch(smp.Sample):
##     legend="Data"
##     #lumi= #pixelLumi
##     lumi= 495.003 #lumiCalc2
##     cfg_builtin = {"sample":"Run2012C-24AugSynch","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}
##     input_files= 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/Run2012C-24AugSynchSelMuJetsSkim.root'
##     is_data=True

class Run2012CPromptRecov2(smp.Sample):
    legend="Data"
    #lumi= #pixelLumi
    lumi= 6392. #lumiCalc2
    cfg_builtin = {"sample":"Run2012C-PromptReco-v2","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}
    input_files= 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/Run2012C-PromptReco-v2SynchSelMuJetsSkim.root'
    is_data=True

## class Run2012DPromptRecov1(smp.Sample):
##     legend="Data"
##     #lumi= #pixelLumi
##     lumi=  6689. #lumiCalc2
##     cfg_builtin = {"sample":"Run2012D-PromptReco-v1","jetsource":"selectedPatJetsForAnalysis" , "photonsource":"patPhotons", "muonsource":"tightmuons"}
##     input_files= 'file:/net/scratch_cms/institut_3b/kuessel/'+skim+'/Run2012D-PromptReco-v1SynchSelMuJetsSkim.root'
##     is_data=True

