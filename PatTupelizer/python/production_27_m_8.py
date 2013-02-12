import cmstoolsac3b.main 
import cmstoolsac3b.sample as smp

samples = smp.generate_samples_glob(
    "/disk1/tholen/eventFiles/aodsim_27_m_8/*.root",
    "file:/disk1/tholen/eventFiles/patTuple_27_m_8/"
)

if __name__ == '__main__':
    cmstoolsac3b.main.main(
        max_num_processes=3,
        samples=samples,
        cfg_main_import_path="MyPackage.PatTupelizer.myttbarPatTuple_cfg"
    )


