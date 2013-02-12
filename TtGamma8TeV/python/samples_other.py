
import cmstoolsac3b.sample as smp

path = "file:/disk1/tholen/eventFiles/fromGrid20130117/"

class TTbar(smp.Sample):
    legend = "t#bar{t} inclusive"
    x_sec  = 225.197
    n_events = 6736135
    input_files = path + "TTbar.root"

class WJets(smp.Sample):
    legend = "W + Jets"
    x_sec = 37509.0
    n_events = 18393090
    input_files = path + "WJets.root"

class DYJets(smp.Sample):
    legend = "Z + Jets"
    x_sec = 3503.71
    n_events = 1082838
    input_files = path + "DYJets.root"

class SingleTop_TCh_T(smp.Sample):
    legend = "Single Top"
    x_sec = 56.4
    n_events = 23777
    input_files = path + "SingleTop-tCh-T.root"

class SingleTop_TCh_Tbar(smp.Sample):
    legend = "Single Top"
    x_sec = 30.7
    n_events = 1935072 
    input_files = path + "SingleTop-tCh-Tbar.root"

class SingleTop_TWCh_T(smp.Sample):
    legend = "Single Top"
    x_sec = 11.1
    n_events = 497658
    input_files = path + "SingleTop-tWCh-T.root"

class SingleTop_TWCh_Tbar(smp.Sample):
    legend = "Single Top"
    x_sec = 11.1
    n_events = 493460
    input_files = path + "SingleTop-tWCh-Tbar.root"

