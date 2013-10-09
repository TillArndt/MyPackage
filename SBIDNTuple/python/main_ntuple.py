

import cmstoolsac3b.main as main
import cmstoolsac3b.settings as settings
settings.ttbar_xsec = 245.8
settings.ttbar_xsec_err = 2.6 * settings.ttbar_xsec

from cmstoolsac3b.sample import load_samples
import MyPackage.TtGamma8TeV.samples_cern as samples_cern
settings.samples = {}
settings.samples.update(load_samples(samples_cern))
settings.samples = dict(
    (k, v)
    for k, v in settings.samples.iteritems()
    if k in ["TTJeRD1", "TTPoPy", "TTMadG"])
settings.active_samples = settings.samples.keys()

settings.cfg_main_import_path="MyPackage.SBIDNTuple.cfg_produce_ntuple"

settings.try_reuse_results = True
settings.max_num_processes = 4
work = "/afs/cern.ch/work/h/htholen/"
settings.web_target_dir     = work + "public/www/SBID/"

settings.DIR_NTUPLE = "outputNTuple"

settings.rootfile_postfixes= ['.root', '.png']

import tuple_to_histo
from cmstoolsac3b import postproctools
settings.post_proc_tools = [
    tuple_to_histo.FakeHistoProducer(None, "TTJeRD1"),
    tuple_to_histo.FakeHistoProducer(None, "TTPoPy"),
    tuple_to_histo.FakeHistoProducer(None, "TTMadG"),
    tuple_to_histo.SBIDHistoProducer(None, "TTJeRD1"),
    tuple_to_histo.SBIDHistoProducer(None, "TTPoPy"),
    tuple_to_histo.SBIDHistoProducer(None, "TTMadG"),
    tuple_to_histo.Chi2Producer(None, "TTJeRD1"),
    tuple_to_histo.Chi2Producer(None, "TTPoPy"),
    tuple_to_histo.Chi2Producer(None, "TTMadG"),
    tuple_to_histo.Chi2Evaluator(None, "TTJeRD1"),
    tuple_to_histo.Chi2Evaluator(None, "TTPoPy"),
    tuple_to_histo.Chi2Evaluator(None, "TTMadG"),
    tuple_to_histo.Chi2EvaluatorDouble(None, "TTJeRD1", "TTPoPy"),
    tuple_to_histo.Chi2EvaluatorDouble(None, "TTJeRD1", "TTMadG"),
    postproctools.SimpleWebCreator
]



if __name__ == '__main__':
    main.main()
