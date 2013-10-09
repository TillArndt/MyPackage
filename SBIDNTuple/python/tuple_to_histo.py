
from cmstoolsac3b import postprocessing
from cmstoolsac3b import wrappers
from cmstoolsac3b import settings
from cmstoolsac3b import generators as gen
from ROOT import TFile, TH1D
import itertools


range_sieie  = list(x*0.001 for x in xrange(13, 21, 1))
range_phoiso = list(x*0.1   for x in xrange(10, 20, 5))
range_neuiso = list(x*0.1   for x in xrange(60, 70, 5))


def histo_key(s, p, n):
    return "%02d_%02d_%02d" % (s*1000, p*10, n*10)


def s_p_n(hist_key):
    s, p, n = tuple(float(v) for v in hist_key.split("_"))
    return s*0.001, p*0.1, n*0.1

class SBIDHistoProducer(postprocessing.PostProcTool):
    def __init__(self, name=None, sample=None):
        super(SBIDHistoProducer, self).__init__(name)
        if sample:
            self.sample = sample
            self.name = self.name + sample

    def produce_histo(self, sieie, phoiso, neuiso):
        histo_key_token = histo_key(sieie, phoiso, neuiso)
        histo_name = "SBID_"+self.sample+"_"+histo_key_token
        ntuple = TFile("outputNTuple/"+self.sample+"_edmTuple.root")
        events = ntuple.GetKey("Events").ReadObj()
        histo = TH1D(
            histo_name,
            ";PF charged hadron isolation / GeV;number of photons",
            40, 0., 10.
        )

        max_phoiso = (
            "min(0.2*floats_photonTuple_pt_NTuple.obj, "
            + "(4.5 + 0.005*floats_photonTuple_pt_NTuple.obj) * %f)" % phoiso
        )
        max_neuiso = (
            "min(0.2*floats_photonTuple_pt_NTuple.obj, "
            + "(4.5 + 0.005*floats_photonTuple_pt_NTuple.obj) * %f)" % neuiso
        )
        events.Project(
            histo_name,
            "floats_photonTuple_chargedisoSCFootRmEB_NTuple.obj",
            "("
            + ("floats_photonTuple_sieie_NTuple.obj < %f" % sieie)
            + "&& floats_photonTuple_pfphoIso_NTuple.obj < "
            + max_phoiso
            + "&& floats_photonTuple_pfneutralIso_NTuple.obj < "
            + max_neuiso
            + ")"
            + "* floats_photonTuple_lowerCut_NTuple.obj "
            + "* double_puWeight_PUWeightTrue_NTuple.obj"
        )
        histo.Sumw2()
        histo.SetDirectory(0)
        return histo, histo_key_token

    def run(self):
        self.result = wrappers.Wrapper()
        self.result.tokens = []
        for sieie in range_sieie:
            for phoiso in range_phoiso:
                for neuiso in range_neuiso:
                    self.message(
                        "INFO: producing histo (sieie, phoiso, neuiso): "
                        + ", %f, %f, %f" % (sieie, phoiso, neuiso)
                    )
                    histo, token = self.produce_histo(sieie, phoiso, neuiso)
                    setattr(self.result, token, histo)
                    self.result.tokens.append(token)


class FakeHistoProducer(postprocessing.PostProcTool):
    def __init__(self, name=None, sample=None):
        super(FakeHistoProducer, self).__init__(name)
        if sample:
            self.sample = sample
            self.name = self.name + sample

    def produce_histo(self):
        histo_name = "FakeHisto_"+self.sample
        ntuple = TFile("outputNTuple/"+self.sample+"_edmTuple.root")
        events = ntuple.GetKey("Events").ReadObj()
        histo = TH1D(
            histo_name,
            ";PF charged hadron isolation / GeV;number of photons",
            40, 0., 10.
        )
        events.Project(
            histo_name,
            "floats_photonTuple_chargedisoSCFootRmEB_NTuple.obj",
            "(1. - floats_photonTuple_real_NTuple.obj) "
            + "* floats_photonTuple_idCut_NTuple.obj "
            + "* double_puWeight_PUWeightTrue_NTuple.obj"
        )
        histo.Sumw2()
        histo.SetDirectory(0)
        wrp = wrappers.HistoWrapper(
            histo, sample=self.sample
        )
        return wrp

    def run(self):
        self.result = self.produce_histo()


class Chi2Producer(postprocessing.PostProcTool):
    can_reuse = False
    has_output_dir = False

    def __init__(self, name=None, sample=None):
        super(Chi2Producer, self).__init__(name)
        if sample:
            self.sample = sample
            self.name = self.name + sample

    def run(self):
        self.result = []
        fake_histo = settings.post_proc_dict["FakeHistoProducer"+self.sample]
        sbid_wrp = settings.post_proc_dict["SBIDHistoProducer"+self.sample]
        for tok in sbid_wrp.tokens:
            sbid_histo_wrp = wrappers.HistoWrapper(
                getattr(sbid_wrp, tok)
            )
            chi2 = gen.op.chi2((fake_histo, sbid_histo_wrp)).float
            s, p, n = s_p_n(tok)
            wrp = wrappers.FloatWrapper(
                chi2,
                histo_key=tok,
                sieie=s, phoiso=p, neuiso=n,
            )
            self.result.append(wrp)


class Chi2EvaluatorBase(postprocessing.PostProcTool):
    def make_histo(self, histo_key_list, range_list, name):
        half_step = (range_list[1] - range_list[0])/2
        histo = TH1D(
            "histo_in_"+name,
            ";upper "+name+" bound; chi2",
            len(range_list), range_list[0]-half_step, range_list[-1]+half_step
        )
        for i, h_key in enumerate(histo_key_list):
            histo.SetBinContent(i+1, self.wrp_dict[h_key].float)
        wrp = wrappers.HistoWrapper(
            histo
        )
        return wrp

    def do_evaluation(self, wrp_list):
        self.wrp_dict = dict((w.histo_key, w) for w in wrp_list)
        min_wrp = min(wrp_list, key=lambda w: w.float)
        histo_in_s = self.make_histo(
            list(
                histo_key(s, min_wrp.phoiso, min_wrp.neuiso)
                for s in range_sieie
            ), range_sieie, "sieie"
        )
        histo_in_p = self.make_histo(
            list(
                histo_key(min_wrp.sieie, p, min_wrp.neuiso)
                for p in range_phoiso
            ), range_phoiso, "phoiso"
        )
        histo_in_n = self.make_histo(
            list(
                histo_key(min_wrp.sieie, min_wrp.phoiso, n)
                for n in range_neuiso
            ), range_neuiso, "neuiso"
        )
        histo_in_s.min_token = min_wrp.histo_key
        histo_in_p.min_token = min_wrp.histo_key
        histo_in_n.min_token = min_wrp.histo_key
        self.result = [
            histo_in_s,
            histo_in_p,
            histo_in_n,
        ]
        gen.consume_n_count(
            gen.save(
                gen.canvas((h,) for h in self.result),
                lambda c: self.plot_output_dir + c.name
            )
        )


class Chi2Evaluator(Chi2EvaluatorBase):
    def __init__(self, name=None, sample=None):
        super(Chi2Evaluator, self).__init__(name)
        if sample:
            self.sample = sample
            self.name = self.name + sample

    def run(self):
        self.do_evaluation(
            settings.post_proc_dict["Chi2Producer"+self.sample]
        )


class Chi2EvaluatorDouble(Chi2EvaluatorBase):
    def __init__(self, name=None, sample1=None, sample2=None):
        super(Chi2EvaluatorDouble, self).__init__(name)
        if sample1:
            self.sample1 = sample1
            self.sample2 = sample2
            self.name = self.name + sample1 + sample2

    def run(self):
        list1 = settings.post_proc_dict["Chi2Producer"+self.sample1]
        list2 = settings.post_proc_dict["Chi2Producer"+self.sample2]
        comb = []
        for w1, w2 in itertools.izip(list1, list2):
            if w1.histo_key != w2.histo_key:
                self.message("ERROR histo_key not equal. Quitting.")
                return
            info = w1.all_info()
            del info["float"]
            comb.append(wrappers.FloatWrapper(
                w1.float + w2.float,
                **info
            ))
        self.do_evaluation(comb)



