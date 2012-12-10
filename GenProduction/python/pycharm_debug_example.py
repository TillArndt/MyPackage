from pydev import pydevd
pydevd.settrace('localhost', port=22072, stdoutToServer=True, stderrToServer=True)

import cmstoolsac3b.main 
import cmstoolsac3b.sample as smp

samples = smp.generate_samples(
    ("tta0.lhef", "tta01.lhef", "tta025.lhef", "tta05.lhef", "tta075.lhef", "tta1.lhef"),
    "/user/backes/share/",
    "/user/tholen/eventFiles/"
)

if __name__ == '__main__':
    cmstoolsac3b.main.main(
        samples=samples,
        cfg_main_import_path="MyPackage.GenProduction.Hadronizer_MgmMatchTune4C_7TeV_madgraph_pythia8_cff_py_GEN_FASTSIM_HLT_PU_START42"
    )


