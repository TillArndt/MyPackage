
#import sys
#sys.path.append("/home/home2/institut_3b/tholen/installs/pycharm-2.0.2/pycharm-debug.egg")
#from pydev import pydevd
#pydevd.settrace('localhost', port=22022, suspend=False)


import cmstoolsac3b.settings as settings
import samples_merge
samples = {}
samples.update(samples_merge.generate_das_samples())


import cmstoolsac3b.main
if __name__ == '__main__':
    cmstoolsac3b.main.main(
        samples=samples,
        max_num_processes=3,
        try_reuse_results=True,
        cfg_use_file_service=False,
        #suppress_cmsRun_exec=True,
        cfg_main_import_path="MyPackage.TtMerging.cfg_merge",
    )


