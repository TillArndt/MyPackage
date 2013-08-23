
import copy
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.settings as settings
import cmstoolsac3b.wrappers as wrappers
from cmstoolsac3b.generators import _iterableize
from plots_summary import result_quantities, xsec_calc_name_iter


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
        wrp.write_info_file(settings.dir_result + "sys_uncert_result.info")
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
        wrp.write_info_file(settings.dir_result + "sys_uncert_result.info")
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



################################################# showering / hadronization ###
class SysIsrFsr(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoPy")
        settings.active_samples.append("TTPoHe")
        super(SysIsrFsr, self).prepare_for_systematic()


################################################################# generator ###
class SysMadgraph(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoPy")
        settings.active_samples.append("TTMadG")
        super(SysMadgraph, self).prepare_for_systematic()


class SysMCatNLO(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoHe")
        settings.active_samples.append("TTMCNLO")
        super(SysMCatNLO, self).prepare_for_systematic()


#################################################################### pileup ###
def makeSysSamplesPU():
    mc_samples = settings.mc_samples()
    for name, smp_old in mc_samples.iteritems():
        makeSysSample(
            name,
            name + "_PU",
            {"puWeightInput": "PU_Run2012_73500.root"}
        )

class SysPU(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        pu_samples = list(s + "_PU" for s in mc_samples)
        for s in mc_samples:
            settings.active_samples.remove(s)
        settings.active_samples += pu_samples
        super(SysPU, self).prepare_for_systematic()


###################################################### selection efficiency ###
# whizard
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
        sys_xsec_group("SysSelEffTTPoPy",   "TTPoPy",   (0.025,0.034)),
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
    makeSysSample("TTPoPy", "TTPoPy_DRCutLow", {"cutDeltaR": 0.050})
    makeSysSample("TTPoPy", "TTPoPy_DRCutHigh", {"cutDeltaR": 0.150})

class SysOverlapDRCutLow(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoPy")
        settings.active_samples.append("TTPoPy_DRCutLow")
        super(SysOverlapDRCutLow, self).prepare_for_systematic()


class SysOverlapDRCutHigh(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTPoPy")
        settings.active_samples.append("TTPoPy_DRCutHigh")
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
        settings.samples[name + "_BTags"].cfg_add_lines.append(
            "process.bTagCounter.minNumber = 2"
        )

class SysBTags(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_BTags" for smp in settings.active_samples
        )
        super(SysBTags, self).prepare_for_systematic()


