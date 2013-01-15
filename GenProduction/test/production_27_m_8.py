import cmstoolsac3b.main 
import cmstoolsac3b.sample as smp

samples = smp.generate_samples_glob(
    "/disk1/tholen/eventFiles/lhef_27_m_8/*.lhef",
    "file:/disk1/tholen/eventFiles/aodsim_27_m_8/"
)

if __name__ == '__main__':
    cmstoolsac3b.main.main(
        max_num_processes=3,
        samples=samples,
        cfg_output_module_name="AODSIMoutput",
        cfg_use_file_service=False,
        cfg_main_import_path="MyPackage.GenProduction.MyHadronizer8TeV_cff_py_GEN_FASTSIM_HLT_PU"
    )


