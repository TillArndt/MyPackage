
import cmstoolsac3b.sample as smp
from glob import glob

path = "file:/disk1/tholen/eventFiles/"


class two2seven_27_m_8(smp.Sample):
    legend      = "t#bar{t}#gamma #mu+Jets (Signal)"
    x_sec        = 0.40419946 #pb
    n_events    = 106600
    input_files = map(
        lambda x: "file:" + x,
	glob(path[5:] + "patTuple_27_m_8/*.root")
    )
    

