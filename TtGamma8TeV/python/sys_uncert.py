
import copy
import cmstoolsac3b.postprocessing as ppc
from cmstoolsac3b import diskio
from cmstoolsac3b import settings
from cmstoolsac3b import wrappers
from cmstoolsac3b.generators import _iterableize
from plots_summary import result_quantities, xsec_calc_name_iter


top_sample = next(s for s in settings.active_samples if s[:2] == "TT")

################################################## base class / preparation ###
def makeSysSample(old_name, new_name, dict_update):
    """Utility method for generating systematic samples."""
    new_smp = copy.deepcopy(settings.samples[old_name])
    new_smp.name = new_name
    new_smp.cfg_builtin.update(dict_update)
    settings.samples[new_name] = new_smp


class SysBase(ppc.PostProcChainVanilla):
    """Base for sys uncerts. Calculates and stores deviation of new result."""

    def __init__(self, name=None, tools=None, preparation_func=None):
        super(SysBase, self).__init__(name, tools)
        self.preparation_func = preparation_func

    def prepare_for_systematic(self):
        if self.preparation_func:
            self.preparation_func()
        for calc in xsec_calc_name_iter():
            setattr(self, calc, settings.post_proc_dict[calc])

    def finish_with_systematic(self):
        wrp = wrappers.Wrapper(name=self.name)
        wrp.formula = "abs(new - old) / old"
        for calc in xsec_calc_name_iter():
            self.calc_uncert(calc, wrp)
        diskio.write(wrp, settings.dir_result + "sys_uncert_result.info")
        settings.persistent_dict[self.name] = wrp

    def calc_uncert(self, xsec_calc, wrp):
        new = settings.post_proc_dict[xsec_calc]
        old = getattr(self, xsec_calc)
        for q in result_quantities:
            new_val = getattr(new, q)
            old_val = getattr(old, q)
            res = abs((new_val - old_val) / old_val)
            setattr(wrp, xsec_calc+"_"+q, res)
            self.message(
                "INFO Uncertainty on "
                + xsec_calc + "_" + q + " / %: " + str(res * 100.)
            )


class SysGroup(ppc.PostProcChain):
    def push_tools(self, tools):
        for t in self.tool_chain:
            if isinstance(t, SysGroup):
                t.push_tools(tools)
            else:
                t.add_tools(tools)
        return self

    def store_result(self, result, formula):
        wrp = wrappers.Wrapper(name=self.name)
        wrp.__dict__.update(result)
        settings.persistent_dict[self.name] = wrp
        wrp.formula = formula
        diskio.write(wrp, settings.dir_result + "sys_uncert_result.info")
        self.message("INFO Group uncertainty results: " + str(wrp))


class SysGroupMax(SysGroup):
    """Groups systematics together. Takes largest deviation as result."""
    def finished(self):
        res = {}
        for q in result_quantities:
            for calc in xsec_calc_name_iter():
                name = calc + "_" + q
                res[name] = max(
                    abs(getattr(settings.persistent_dict[t.name], name))
                    for t in self.tool_chain
                )
        self.store_result(res, "max( sys deviations )")
        super(SysGroupMax, self).finished()


class SysGroupAdd(SysGroup):
    def finished(self):
        res = {}
        for q in result_quantities:
            for calc in xsec_calc_name_iter():
                name = calc + "_" + q
                res[name] = sum(
                    (getattr(settings.persistent_dict[t.name], name))**2
                    for t in self.tool_chain
                )**.5
        self.store_result(res, "(sum( sys deviations**2 ))**.5")
        super(SysGroupAdd, self).finished()


####################################################################### fit ###
class SysFit(SysBase):
    pass


################################################# showering / hadronization ###
class SysIsrFsr(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoPy")
        settings.active_samples.append("TTPoHe")
        super(SysIsrFsr, self).prepare_for_systematic()


################################################################# generator ###
class SysTTMadG(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoPy")
        settings.active_samples.append("TTMadG")
        super(SysTTMadG, self).prepare_for_systematic()


class SysTTPoPy(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTMadG")
        settings.active_samples.append("TTPoPy")
        super(SysTTPoPy, self).prepare_for_systematic()


class SysMCatNLO(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoHe")
        settings.active_samples.append("TTMCNLO")
        super(SysMCatNLO, self).prepare_for_systematic()


################################################################## whiz pdf ###
from plots_xsec import XsecCalculatorChHadIsoSBID
from cmstoolsac3b import util
import cmstoolsac3b.generators as gen
from ROOT import TH1D


class XsecCalculatorBase(XsecCalculatorChHadIsoSBID):
    def __init__(self, name=None, pre=None, fid=None, post=None):
        super(XsecCalculatorBase, self).__init__(name)
        if pre:
            self.replacement_pre = pre
            self.replacement_fid = fid
            self.replacement_post = post

    def get_sig_count_name(self, orig):
        if orig == self.pre_count_name:
            return self.replacement_pre
        if orig == self.fid_count_name:
            return self.replacement_fid
        if orig == self.post_count_name:
            return self.replacement_post


class PDFUncertCombiner(ppc.PostProcTool):
    def __init__(self, name=None):
        super(PDFUncertCombiner, self).__init__(
            "XsecCalculatorChHadIsoSBID",  # fake the original XsecCalculator
        )
        self.values = []

    def get_quantity(self, i, quantity):
        if i == 0:
            return getattr(self.result, quantity)
        else:
            return getattr(
                settings.post_proc_dict["XsecCalculatorPDF_%d" % i],
                quantity
            )

    def calc_variation(self, quantity):
        pass

    def store_value(self, v):
        self.values.append(v)
        return v

    def run(self):
        self.result = settings.post_proc_dict["XsecCalculatorChHadIsoSBID"]
        for quantity in ["R", "R_fid", "xsec"]:
            self.calc_variation(quantity)
            histo = wrappers.HistoWrapper(
                util.list2histogram(
                    self.values,
                    "PDF_uncert_distr_" + quantity,
                    ";#Delta("+quantity+");CTEQ61 PDF eigenvector evaluation",
                    60
                )
            )
            del self.values[:]
            cnv = gen.canvas([[histo]])
            cnv = gen.save(cnv, lambda c: self.plot_output_dir + c.name)
            gen.consume_n_count(cnv)


# math taken from
# http://www.hep.ucl.ac.uk/pdf4lhc/PDF4LHC_practical_guide.pdf
class PDFUncertCombinerPlus(PDFUncertCombiner):
    def calc_variation(self, quantity):
        variance90 = sum(
            self.store_value(max((
                self.get_quantity(2*i-1, quantity) -
                self.get_quantity(0, quantity),
                self.get_quantity(2*i, quantity) -
                self.get_quantity(0, quantity),
                0,
            )))**2
            for i in xrange(1, 21)
        )
        nominal = getattr(self.result, quantity)
        plus = nominal + variance90**.5 / 1.64485 # 1.64.. for CL90 => CL68
        setattr(self.result, quantity, plus)


class PDFUncertCombinerMinus(PDFUncertCombiner):
    def calc_variation(self, quantity):
        variance90 = sum(
            self.store_value(max((
                self.get_quantity(0, quantity) -
                self.get_quantity(2*i-1, quantity),
                self.get_quantity(0, quantity) -
                self.get_quantity(2*i, quantity),
                0,
            )))**2
            for i in xrange(1, 21)
        )
        nominal = getattr(self.result, quantity)
        minus = nominal - variance90**.5 / 1.64485 # 1.64.. to get to CL68
        setattr(self.result, quantity, minus)


class SysWhizPDFWeightBase(SysBase):
    def prepare_for_systematic(self):
        for i in xrange(1, 41):
            self.tool_chain.append(XsecCalculatorBase(
                "XsecCalculatorPDF_%d" % i,
                "PDFWeightpre%d," % i,
                "PDFWeightfid%d," % i,
                "PDFWeightpost%d," % i,
            ))
        super(SysWhizPDFWeightBase, self).prepare_for_systematic()


class SysWhizPDFWeightPlus(SysWhizPDFWeightBase):
    def prepare_for_systematic(self):
        super(SysWhizPDFWeightPlus, self).prepare_for_systematic()
        self.tool_chain.append(PDFUncertCombinerPlus())


class SysWhizPDFWeightMinus(SysWhizPDFWeightBase):
    def prepare_for_systematic(self):
        super(SysWhizPDFWeightMinus, self).prepare_for_systematic()
        self.tool_chain.append(PDFUncertCombinerMinus())


SysWhizPDFWeight = SysGroupMax(
    "SysWhizPDFWeight",
    [
        SysWhizPDFWeightPlus,
        SysWhizPDFWeightMinus,
    ]
)


class SysWhizNNPDF(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("whiz2to5")
        settings.active_samples.append("whiz2to5_PDF")
        super(SysWhizNNPDF, self).prepare_for_systematic()


SysWhizPDF = SysGroupAdd(
    "SysWhizPDF",
    [
        SysWhizNNPDF,
        SysWhizPDFWeight,
    ]
)


#################################################################### pileup ###
def makeSysSamplesPU():
    mc_samples = settings.mc_samples()
    for name in mc_samples.iterkeys():
        makeSysSample(
            name,
            name + "_PU",
            {"puWeightInput": "PU_Run2012_73500.root"}
        )

class SysPU(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        da_samples = settings.data_samples().keys()
        pu_samples = list(s + "_PU" for s in mc_samples)
        settings.active_samples = pu_samples + da_samples
        super(SysPU, self).prepare_for_systematic()


########################################################## btag reweighting ###
def makeSysSamplesBTagWeight():
    mc_samples = settings.mc_samples()
    for name in mc_samples.iterkeys():
        makeSysSample(
            name,
            name + "_BTagWeightBCMinus",
            {}
        )
        makeSysSample(
            name,
            name + "_BTagWeightBCPlus",
            {}
        )
        makeSysSample(
            name,
            name + "_BTagWeightUDSGMinus",
            {}
        )
        makeSysSample(
            name,
            name + "_BTagWeightUDSGPlus",
            {}
        )
        settings.samples[name + "_BTagWeightBCMinus"].cfg_add_lines += (
            "process.bTagWeight.errorModeBC = -1",
        )
        settings.samples[name + "_BTagWeightBCPlus"].cfg_add_lines += (
            "process.bTagWeight.errorModeBC = +1",
        )
        settings.samples[name + "_BTagWeightUDSGMinus"].cfg_add_lines += (
            "process.bTagWeight.errorModeUDSG = -1",
        )
        settings.samples[name + "_BTagWeightUDSGPlus"].cfg_add_lines += (
            "process.bTagWeight.errorModeUDSG = +1",
        )


class SysBTagWeightBCMinus(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        da_samples = settings.data_samples().keys()
        btag_samples = list(s + "_BTagWeightBCMinus" for s in mc_samples)
        settings.active_samples = btag_samples + da_samples
        super(SysBTagWeightBCMinus, self).prepare_for_systematic()


class SysBTagWeightBCPlus(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        da_samples = settings.data_samples().keys()
        btag_samples = list(s + "_BTagWeightBCPlus" for s in mc_samples)
        settings.active_samples = btag_samples + da_samples
        super(SysBTagWeightBCPlus, self).prepare_for_systematic()


class SysBTagWeightUDSGMinus(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        da_samples = settings.data_samples().keys()
        btag_samples = list(s + "_BTagWeightUDSGMinus" for s in mc_samples)
        settings.active_samples = btag_samples + da_samples
        super(SysBTagWeightUDSGMinus, self).prepare_for_systematic()


class SysBTagWeightUDSGPlus(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        da_samples = settings.data_samples().keys()
        btag_samples = list(s + "_BTagWeightUDSGPlus" for s in mc_samples)
        settings.active_samples = btag_samples + da_samples
        super(SysBTagWeightUDSGPlus, self).prepare_for_systematic()


SysBTagWeightBC = SysGroupMax(
    "SysBTagWeightBC",
    [
        SysBTagWeightBCMinus,
        SysBTagWeightBCPlus,
    ]
)


SysBTagWeightUDSG = SysGroupMax(
    "SysBTagWeightUDSG",
    [
        SysBTagWeightUDSGMinus,
        SysBTagWeightUDSGPlus,
    ]
)


SysBTagWeight = SysGroupAdd(
    "SysBTagWeight",
    [
        SysBTagWeightBC,
        SysBTagWeightUDSG,
    ]
)


####################################################################### JEC ###
def makeSysSamplesJEC():
    for name in settings.active_samples:
        makeSysSample(
            name,
            name + "_JEC",
            {}
        )
        settings.samples[name + "_JEC"].cfg_add_lines += (
            "process.load('MyPackage.TtGamma8TeV.cfi_filterJEC')",
            "process.preSel.insert(0, process.filterJEC)",
        )


class SysJEC(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_JEC" for smp in settings.active_samples
        )
        super(SysJEC, self).prepare_for_systematic()


####################################################################### JER ###
def makeSysSamplesJER():
    for name in settings.active_samples:
        makeSysSample(
            name,
            name + "_JER",
            {}
        )
        settings.samples[name + "_JER"].cfg_add_lines += (
            "process.load('MyPackage.TtGamma8TeV.cfi_filterJER')",
            "process.preSel.insert(0, process.filterJER)",
        )


class SysJER(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_JER" for smp in settings.active_samples
        )
        super(SysJER, self).prepare_for_systematic()


######################################################## top-pt reweighting ###
def makeSysSamplesTopPt():
    for name in settings.active_samples:
        opt = settings.samples[name].cfg_builtin.get("preSelOpt")
        if opt in ("doOverlapRemoval", "go4Whiz"):
            makeSysSample(name, name + "_topPtMinus", {})
            settings.samples[name + "_topPtMinus"].cfg_add_lines.append(
                "process.topPtWeight.uncertMode = cms.untracked.int32(-1)"
            )
            makeSysSample(name, name + "_topPtPlus", {})
            settings.samples[name + "_topPtPlus"].cfg_add_lines.append(
                "process.topPtWeight.uncertMode = cms.untracked.int32(+1)"
            )


class SysTopPtMinus(SysBase):
    def prepare_for_systematic(self):
        for name in settings.active_samples[:]:
            opt = settings.samples[name].cfg_builtin.get("preSelOpt")
            if opt in ("doOverlapRemoval", "go4Whiz"):
                settings.active_samples.remove(name)
                settings.active_samples.append(name + "_topPtMinus")
        super(SysTopPtMinus, self).prepare_for_systematic()


class SysTopPtPlus(SysBase):
    def prepare_for_systematic(self):
        for name in settings.active_samples[:]:
            opt = settings.samples[name].cfg_builtin.get("preSelOpt")
            if opt in ("doOverlapRemoval", "go4Whiz"):
                settings.active_samples.remove(name)
                settings.active_samples.append(name + "_topPtPlus")
        super(SysTopPtPlus, self).prepare_for_systematic()

SysTopPt = SysGroupMax(
    "SysTopPt",
    [
        SysTopPtMinus,
        SysTopPtPlus
    ]
)


#################################################################### pileup ###
def makeSysSamplesTrig():
    mc_samples = settings.mc_samples()
    for name in mc_samples.iterkeys():
        makeSysSample(
            name,
            name + "_TrigPlus",
            {}
        )
        makeSysSample(
            name,
            name + "_TrigMinus",
            {}
        )
        settings.samples[name + "_TrigPlus"].cfg_add_lines += (
            "process.trigWeight.uncertMode = 1",
        )
        settings.samples[name + "_TrigMinus"].cfg_add_lines += (
            "process.trigWeight.uncertMode = -1",
        )

class SysTrigPlus(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        da_samples = settings.data_samples().keys()
        pu_samples = list(s + "_TrigPlus" for s in mc_samples)
        settings.active_samples = pu_samples + da_samples
        super(SysTrigPlus, self).prepare_for_systematic()


class SysTrigMinus(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        da_samples = settings.data_samples().keys()
        pu_samples = list(s + "_TrigMinus" for s in mc_samples)
        settings.active_samples = pu_samples + da_samples
        super(SysTrigMinus, self).prepare_for_systematic()


SysTrig = SysGroupAdd(
    "SysTrig",
    [
        SysTrigPlus,
        SysTrigMinus,
    ]
)


###################################################### selection efficiency ###
def sys_xsec(sample, factor):
    for s in _iterableize(sample):
        settings.samples[s].lumi *= factor
        settings.samples[s].x_sec *= factor


def sys_xsec_group(name, sample, uncert):
    if type(uncert) == tuple:
        plus, minus = uncert[0], uncert[1]
    else:
        plus, minus = uncert, uncert
    return SysGroupMax(
        name,
        [
            SysBase(name+ "Plus",None,lambda: sys_xsec(sample, 1+plus)),
            SysBase(name+"Minus",None,lambda: sys_xsec(sample, 1-minus)),
        ]
    )


#TODO: Store xsec errors in sample def
SysSelEffBkg = SysGroupAdd(
    "SysSelEffBkg",
    [
        sys_xsec_group("SysSelEffT_t",      "T_t",      (2.1/56.4, .3/56.4)),
        sys_xsec_group("SysSelEffTbar_t",   "Tbar_t",   (.9/30.7, 1.1/30.7)),
        sys_xsec_group("SysSelEffT_tW",     "T_tW",     0.3/11.1),
        sys_xsec_group("SysSelEffTbar_tW",  "Tbar_tW",  0.3/11.1),
        sys_xsec_group("SysSelEff"+top_sample,   top_sample,   (0.025,0.034)),
    ]
)

SysSelEff = SysGroupAdd(
    "SysSelEff",
    [
        sys_xsec_group("SysSelEffSig",      "whiz2to5", 0.25),
        SysSelEffBkg,
    ]
)


########################################################### overlap removal ###
def makeSysSamplesDRCut():
    makeSysSample(top_sample, top_sample+"_DRCutLow", {"cutDeltaR": 0.050})
    makeSysSample(top_sample, top_sample+"_DRCutHigh", {"cutDeltaR": 0.150})


class SysOverlapDRCutLow(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove(top_sample)
        settings.active_samples.append(top_sample+"_DRCutLow")
        super(SysOverlapDRCutLow, self).prepare_for_systematic()


class SysOverlapDRCutHigh(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove(top_sample)
        settings.active_samples.append(top_sample+"_DRCutHigh")
        super(SysOverlapDRCutHigh, self).prepare_for_systematic()

SysOverlapDRCut = SysGroupMax(
    "SysOverlapDRCut",
    [
        SysOverlapDRCutHigh,
        SysOverlapDRCutLow
    ]
)


############################################################## template fit ###
from plots_xsec import XsecCalculatorSihih
from plots_xsec import XsecCalculatorChHadIso

class SysTemplateFitSihih(SysBase):
    def prepare_for_systematic(self):
        new_chain = []
        for t in self.tool_chain:
            if t.name == "XsecCalculatorChHadIso":
                new_chain.append(XsecCalculatorSihih())
            else:
                new_chain.append(t)
        self.tool_chain = new_chain
        super(SysTemplateFitSihih, self).prepare_for_systematic()

class SysTemplateFitChHadIso(SysBase):
    def prepare_for_systematic(self):
        new_chain = []
        for t in self.tool_chain:
            if t.name == "XsecCalculatorSihih":
                new_chain.append(XsecCalculatorChHadIso())
            else:
                new_chain.append(t)
        self.tool_chain = new_chain
        super(SysTemplateFitChHadIso, self).prepare_for_systematic()


############################################### stability: et cut variation ###
def makeSysSamplesETCut():
    for name in settings.active_samples:
        makeSysSample(name, name + "_ETCutLow", {"etCutValue": 22.})
        makeSysSample(name, name + "_ETCutHigh", {"etCutValue": 28.})

class SysPhotonETCutLow(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_ETCutLow" for smp in settings.active_samples
        )
        super(SysPhotonETCutLow, self).prepare_for_systematic()


class SysPhotonETCutHigh(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_ETCutHigh" for smp in settings.active_samples
        )
        super(SysPhotonETCutHigh, self).prepare_for_systematic()

SysPhotonETCut = SysGroupMax(
    "SysPhotonETCut",
    [SysPhotonETCutLow, SysPhotonETCutHigh]
)

##################################################### stability: two b-tags ###
def makeSysSamplesBTag():
    for name in settings.active_samples:
        makeSysSample(name, name + "_BTags", {})
        settings.samples[name + "_BTags"].cfg_add_lines += (
            "process.bTagCounter.minNumber = 2",
            "process.bTagWeight.twoBTagMode = True"
        )

class SysBTags(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_BTags" for smp in settings.active_samples
        )
        super(SysBTags, self).prepare_for_systematic()



