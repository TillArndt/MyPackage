
import copy
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.settings as settings
import cmstoolsac3b.wrappers as wrappers


def makeSysSample(old_name, new_name, dict_update):
    new_smp = copy.deepcopy(settings.samples[old_name])
    new_smp.name = new_name
    # TODO: why does deepcopy not work???
    new_smp.cfg_builtin = settings.samples[old_name].cfg_builtin.copy()
    new_smp.cfg_builtin.update(dict_update)
    settings.samples[new_name] = new_smp


class SysBase(ppc.PostProcChainSystematics):
    def finish_with_systematic(self):
        new = settings.post_proc_dict["x_sec_result"]
        old = self.old_result
        res = abs(old.R - new.R) / old.R
        name = self.__class__.__name__
        settings.persistent_dict[name] = res
        self.message("INFO " + name + " / %: " + str(res * 100.))
        wrp = wrappers.FloatWrapper(res, name=name)
        wrp.formula = "abs(old.R - new.R) / old.R"
        wrp.write_info_file(settings.dir_result + "sys_uncert_result.info")


class SysIsrFsr(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTJets")
        settings.active_samples.remove("TTJetsSignal")
        settings.active_samples.append("TTNLO")
        settings.active_samples.append("TTNLOSignal")
        self.old_result = settings.post_proc_dict["x_sec_result"]


class SysPU(SysBase):
    def prepare_for_systematic(self):
        mc_samples = settings.mc_samples().keys()
        pu_samples = list(s + "_PU" for s in mc_samples)
        for s in mc_samples:
            settings.active_samples.remove(s)
        settings.active_samples += pu_samples
        self.old_result = settings.post_proc_dict["x_sec_result"]

def makeSysSamplesPU():
    mc_samples = settings.mc_samples()
    for name, smp_old in mc_samples.iteritems():
        makeSysSample(
            name,
            name + "_PU",
            {"puWeightInput": "PU_Run2012_73500.root"}
        )


class SysSelEffBase(ppc.PostProcChainSystematics):
    def finish_with_systematic(self):
        new = settings.post_proc_dict["x_sec_result"]
        old = self.old_result
        res     = abs(old.R - new.R) / old.R
        res_MC  = abs(old.R_MC - new.R_MC) / old.R_MC
        name = self.__class__.__name__
        settings.persistent_dict[name] = res
        settings.persistent_dict[name+"MC"] = res_MC
        self.message("INFO " + name + " / %: " + str(res * 100.))
        self.message("INFO " + name + "MC / %: " + str(res_MC * 100.))
        wrp = wrappers.FloatWrapper(res, name=name)
        wrp.formula = "abs(old.R - new.R) / old.R"
        wrp.write_info_file(settings.dir_result + "sys_uncert_result.info")
        wrp = wrappers.FloatWrapper(res_MC, name=name+"MC")
        wrp.formula = "abs(old.R_MC - new.R_MC) / old.R_MC"
        wrp.write_info_file(settings.dir_result + "sys_uncert_result_MC.info")


class SysSelEffPlus(SysSelEffBase):
    def prepare_for_systematic(self):
        settings.samples["whiz2to5"].lumi *= 1.25
        settings.samples["whiz2to5"].x_sec *= 1.25
        self.old_result = settings.post_proc_dict["x_sec_result"]


class SysSelEffMinus(SysSelEffBase):
    def prepare_for_systematic(self):
        settings.samples["whiz2to5"].lumi *= 0.75
        settings.samples["whiz2to5"].x_sec *= 0.75
        self.old_result = settings.post_proc_dict["x_sec_result"]


class SysOverlapDRCutLow(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTJets")
        settings.active_samples.remove("TTJetsSignal")
        settings.active_samples.append("TTJets_DRCutLow")
        settings.active_samples.append("TTJetsSignal_DRCutLow")
        self.old_result = settings.post_proc_dict["x_sec_result"]


class SysOverlapDRCutHigh(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples.remove("TTJets")
        settings.active_samples.remove("TTJetsSignal")
        settings.active_samples.append("TTJets_DRCutHigh")
        settings.active_samples.append("TTJetsSignal_DRCutHigh")
        self.old_result = settings.post_proc_dict["x_sec_result"]

def makeSysSamplesDRCut():
    makeSysSample("TTJets", "TTJets_DRCutLow", {"cutDeltaR": 0.050})
    makeSysSample("TTJets", "TTJets_DRCutHigh", {"cutDeltaR": 0.150})
    makeSysSample("TTJetsSignal", "TTJetsSignal_DRCutLow", {"cutDeltaR": 0.050})
    makeSysSample("TTJetsSignal", "TTJetsSignal_DRCutHigh", {"cutDeltaR": 0.150})


class SysPhotonETCutLow(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_ETCutLow" for smp in settings.active_samples
        )
        self.old_result = settings.post_proc_dict["x_sec_result"]


class SysPhotonETCutHigh(SysBase):
    def prepare_for_systematic(self):
        settings.active_samples = list(
            smp + "_ETCutHigh" for smp in settings.active_samples
        )
        self.old_result = settings.post_proc_dict["x_sec_result"]

def makeSysSamplesETCut():
    for name in settings.active_samples:
        makeSysSample(name, name + "_ETCutLow", {"etCutValue": 22.})
        makeSysSample(name, name + "_ETCutHigh", {"etCutValue": 28.})

from plots_xsec import XsecCalculatorChHadIso
class SysTemplateFit(SysBase):
    def prepare_for_systematic(self):
        new_chain = []
        for t in self.tool_chain:
            if t.name == "XsecCalculatorSihih":
                new_chain.append(XsecCalculatorChHadIso())
            else:
                new_chain.append(t)
        self.tool_chain = new_chain
        self.old_result = settings.post_proc_dict["x_sec_result"]