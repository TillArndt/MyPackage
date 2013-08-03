
import cmstoolsac3b.main as main
import cmstoolsac3b.settings as settings

from cmstoolsac3b.sample import load_samples
import samples_Zmumugam
settings.samples = {}
settings.samples.update(load_samples(samples_Zmumugam))
settings.active_samples = settings.samples.keys()

import plots_make_signal_template
import cmstoolsac3b.postproctools as ppt
work = "/afs/cern.ch/work/h/htholen/"
settings.web_target_dir = work + "public/www/SignalTemplate/"

post_proc_tools = [
    plots_make_signal_template.plotter,
    ppt.SimpleWebCreator,
]

if __name__ == '__main__':
    main.main(
        post_proc_tools = post_proc_tools,
#        max_num_processes = 4,
        try_reuse_results = True,
        cfg_main_import_path="MyPackage.TtGamma8TeV.cfg_templateDatDrvSig",
    )
