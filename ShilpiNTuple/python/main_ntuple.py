

import cmstoolsac3b.main as main
import cmstoolsac3b.settings as settings
settings.ttbar_xsec = 245.8
settings.ttbar_xsec_err = 2.6 * settings.ttbar_xsec

from cmstoolsac3b.sample import load_samples
import MyPackage.TtGamma8TeV.samples_cern as samples_cern
settings.samples = {}
settings.samples.update(load_samples(samples_cern))
settings.active_samples = settings.samples.keys() # add all MC and data
settings.samples = dict(settings.mc_samples())
settings.active_samples = settings.samples.keys()

settings.cfg_main_import_path="MyPackage.ShilpiNTuple.cfg_produce_ntuple"

settings.try_reuse_results = True
settings.max_num_processes = 4

if __name__ == '__main__':
    main.main()