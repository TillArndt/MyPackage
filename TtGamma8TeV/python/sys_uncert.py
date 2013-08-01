
import copy
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.settings as settings
import cmstoolsac3b.wrappers as wrappers
from cmstoolsac3b.generators import _iterableize


################################################## base class / preparation ###
def makeSysSample(old_name, new_name, dict_update):
    """Utility method for generating systematic samples."""
    new_smp = copy.deepcopy(settings.samples[old_name])
    new_smp.name = new_name
    # TODO: why does deepcopy not work???
    new_smp.cfg_builtin = settings.samples[old_name].cfg_builtin.copy()
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
        self.old_result = settings.post_proc_dict["x_sec_result"]

    def finish_with_systematic(self):
        new = settings.post_proc_dict["x_sec_result"]
        old = self.old_result
        res = abs((new.R - old.R) / old.R)
        name = self.name
        settings.persistent_dict[name] = res
        self.message("INFO " + name + " / %: " + str(res * 100.))
        wrp = wrappers.FloatWrapper(res, name=name)
        wrp.formula = "(new.R - old.R) / old.R"
        wrp.write_info_file(settings.dir_result + "sys_uncert_result.info")


#class SysBaseMC(SysBase):
#    def finish_with_systematic(self):
#        new = settings.post_proc_dict["x_sec_result"]
#        old = self.old_result
#        res_MC  = abs(old.R_MC - new.R_MC / old.R_MC)
#        name = self.name
#        settings.persistent_dict[name] = res_MC
#        self.message("INFO " + name + "/ %: " + str(res_MC * 100.))
#        wrp = wrappers.FloatWrapper(res_MC, name=name+"MC")
#        wrp.formula = "(new.R_MC - old.R_MC) / old.R_MC"
#        wrp.write_info_file(settings.dir_result + "sys_uncert_result_MC.info")


class SysGroup(ppc.PostProcChain):
    def push_tools(self, tools):
        for t in self.tool_chain:
            if isinstance(t, SysGroup):
                t.push_tools(tools)
            else:
                t.add_tools(tools)
        return self

    def store_result(self, result, formula):
        name = self.name
        settings.persistent_dict[name] = result
        self.message("INFO " + name + " / %: " + str(result * 100.))
        wrp = wrappers.FloatWrapper(result, name=name)
        wrp.formula = formula
        wrp.write_info_file(settings.dir_result + "sys_uncert_result.info")


class SysGroupMax(SysGroup):
    """Groups systematics together. Takes largest deviation as result."""
    def finished(self):
        res = max(
            abs(settings.persistent_dict[t.name])
            for t in self.tool_chain
        )
        self.store_result(res, "max( sys deviations )")
        super(SysGroupMax, self).finished()


class SysGroupAdd(SysGroup):
    def finished(self):
        res = sum(
            (settings.persistent_dict[t.name])**2
            for t in self.tool_chain
        )**.5
        self.store_result(res, "(sum( sys deviations**2 ))**.5")
        super(SysGroupAdd, self).finished()



################################################################# isr / fsr ###
class SysIsrFsr(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTJets")
        settings.active_samples.append("TTNLO")
#        settings.active_samples.remove("TTJetsSignal")
#        settings.active_samples.append("TTNLOSignal")
        super(SysIsrFsr, self).prepare_for_systematic()


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

#SysSelEffSigMC = SysGroupMax(
#    "SysSelEffSigMC",
#    [
#        SysBaseMC("SysSelEffSigMCPlus", None,lambda:sys_xsec("whiz2to5", 1.25)),
#        SysBaseMC("SysSelEffSigMCMinus",None,lambda:sys_xsec("whiz2to5", 0.75)),
#    ]
#)

#TODO: Store xsec errors in sample def
SysSelEffBkg = SysGroupAdd(
    "SysSelEffBkg",
    [
        sys_xsec_group("SysSelEffT_t",      "T_t",      (2.1/56.4, .3/56.4)),
        sys_xsec_group("SysSelEffTbar_t",   "Tbar_t",   (.9/30.7, 1.1/30.7)),
        sys_xsec_group("SysSelEffT_tW",     "T_tW",     0.3/11.1),
        sys_xsec_group("SysSelEffTbar_tW",  "Tbar_tW",  0.3/11.1),
        sys_xsec_group("SysSelEffTTJets",   "TTJets",   (0.025,0.034)),
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
    makeSysSample("TTJets", "TTJets_DRCutLow", {"cutDeltaR": 0.050})
    makeSysSample("TTJets", "TTJets_DRCutHigh", {"cutDeltaR": 0.150})
#    makeSysSample("TTJetsSignal", "TTJetsSignal_DRCutLow", {"cutDeltaR": 0.050})
#    makeSysSample("TTJetsSignal", "TTJetsSignal_DRCutHigh", {"cutDeltaR": 0.150})

class SysOverlapDRCutLow(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTJets")
        settings.active_samples.append("TTJets_DRCutLow")
#        settings.active_samples.remove("TTJetsSignal")
#        settings.active_samples.append("TTJetsSignal_DRCutLow")
        super(SysOverlapDRCutLow, self).prepare_for_systematic()


class SysOverlapDRCutHigh(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTJets")
        settings.active_samples.append("TTJets_DRCutHigh")
#        settings.active_samples.remove("TTJetsSignal")
#        settings.active_samples.append("TTJetsSignal_DRCutHigh")
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
        makeSysSample(name, name + "_2BTags", {})
        settings.samples[name + "_2BTags"].cfg_add_lines.append(
            "process.bTagCounter.minNumber = 2"
        )

class SysTwoBTags(SysBase):
    def prepare_for_systematics(self):
        settings.active_samples = list(
            smp + "_2BTags" for smp in settings.active_samples
        )
        super(SysTwoBTags, self).prepare_for_systematic()