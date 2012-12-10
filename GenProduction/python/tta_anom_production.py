import cmstoolsac3b.main 
import cmstoolsac3b.sample as smp

samples = smp.generate_samples(
    ("tta0_all.lhef", "tta01_all.lhef", "tta025_all.lhef", "tta05_all.lhef", "tta075_all.lhef", "tta1_all.lhef"),
    "file:/user/backes/share/",
    "file:/user/tholen/eventFiles/"
)

if __name__ == '__main__':
    cmstoolsac3b.main.main(
        max_num_processes=2,
        samples=samples,
        cfg_output_module_name="AODSIMoutput",
        cfg_main_import_path="MyPackage.GenProduction.Hadronizer_MgmMatchTune4C_7TeV_madgraph_pythia8_cff_py_GEN_FASTSIM_HLT_PU_START42"
    )


