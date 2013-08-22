
import copy
import cmstoolsac3b.settings as settings
import cmstoolsac3b.wrappers as wrappers
import cmstoolsac3b.generators as gen
import cmstoolsac3b.postprocessing as ppc

class RealPhotonsABCD(ppc.PostProcTool):
    def configure(self):
        self.data_sihih = gen.op.sum(
            gen.fs_filter_sort_load({
                "analyzer"  : "dataTemplateFitHistoSihih",
                "name"      : "sihihEB",
                "is_data"   : True,
                })
        )
        self.data_sihih_bkg = gen.op.sum(
            gen.fs_filter_sort_load({
                "analyzer"  : "Nm1PlotSihihChHadIsoInv",
                "name"      : "histo",
                "is_data"   : True,
                })
        )

    def run(self):
        self.configure()

        # store result
        self.result = copy.deepcopy(
            settings.post_proc_dict["RealTightIdPurityCount"]
        )
        r = self.result

        # fetch all histograms
        data_sihih          = self.data_sihih
        data_sihih_bkg      = self.data_sihih_bkg
        mc_chhadiso_real    =  gen.op.merge(
            gen.fs_filter_sort_load({
                "analyzer"  : "realNm2PlotchargedHadronIsoEB",
                "name"      : "histo",
            })
        )
        mc_chhadiso_fake    = gen.op.merge(
            gen.fs_filter_sort_load({
                "analyzer"  : "fakeNm2PlotchargedHadronIsoEB",
                "name"      : "histo",
            })
        )

        # throw away wrappers
        data_sihih          = data_sihih.histo
        data_sihih_bkg      = data_sihih_bkg.histo
        mc_chhadiso_real    = mc_chhadiso_real.histo
        mc_chhadiso_fake    = mc_chhadiso_fake.histo

        # get bin numbers (c: chhadiso, s: sihih)
        b_c_low     = mc_chhadiso_real.FindBin(2.)
        b_c_high    = mc_chhadiso_real.FindBin(6.)
        b_s_high    = data_sihih.GetNbinsX()
        b_s_011p    = data_sihih.FindBin(0.011001) # bin above 0.011
        b_s_011m    = b_s_011p - 1
        b_s_low     = 1

        # signal contamination in chhadiso sideband region
        # (data_sihih_bkg is filled from this region)
        r.chhad_sb_real = mc_chhadiso_real.Integral(b_c_low, b_c_high)
        r.chhad_sb_fake = mc_chhadiso_fake.Integral(b_c_low, b_c_high)
        r.sb_sig_cont   = r.chhad_sb_real / (r.chhad_sb_real + r.chhad_sb_fake)

        # sihih integrals, lower and higher than 0.011
        r.data_gt_011 = data_sihih.Integral(b_s_011p, b_s_high)
        r.data_lt_011 = data_sihih.Integral(b_s_low, b_s_011m)
        r.bkg_gt_011  = data_sihih_bkg.Integral(b_s_011p, b_s_high)
        r.bkg_lt_011  = data_sihih_bkg.Integral(b_s_low, b_s_011m)

        # background normalization factor from sihih sideband
        r.bkg_norm    = r.data_gt_011 / r.bkg_gt_011

        # number of misidentified photons in signal region
        r.n_bkg       = r.bkg_lt_011     * r.bkg_norm * (1 - r.sb_sig_cont)
        r.n_bkg_err   = r.bkg_lt_011**.5 * r.bkg_norm * (1 - r.sb_sig_cont)

        # number of correctly identified photons in signal region
        r.n_sig       = r.data_lt_011 - r.n_bkg
        r.n_sig_err   = (r.data_lt_011 + r.n_bkg_err)**.5

        # now correct for the non-ttgamma events with a real photon
        r.n_sig_ttgam = r.n_sig * r.pur_ttgam
        r.n_sig_ttgam_err = r.n_sig_err * r.pur_ttgam


class RealPhotonsABCDMC(RealPhotonsABCD):
    def configure(self):
        data_lumi = settings.data_lumi_sum_wrp()
        self.data_sihih = gen.op.prod((
            gen.op.merge(
                gen.fs_filter_sort_load({
                    "analyzer"  : "dataTemplateFitHistoSihih",
                    "name"      : "sihihEB",
                    "is_data"   : False,
                })
            ),
            data_lumi
        ))
        self.data_sihih_bkg = gen.op.prod((
            gen.op.merge(
                gen.fs_filter_sort_load({
                    "analyzer"  : "Nm1PlotSihihChHadIsoInv",
                    "name"      : "histo",
                    "is_data"   : False,
                })
            ),
            data_lumi
        ))


