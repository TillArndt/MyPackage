__author__ = 'Heiner Tholen'

from ROOT import TGraph, TGraphErrors, TGraphAsymmErrors, TF1, gStyle, \
    TCanvas, TArrow, TPaveLabel, TPaveText, TFile, \
    kRed, kYellow, kGreen, kWhite
from UserCode.RWTH3b.cmsRunController.classes.CRPostProcessor import CRSimpleHistoTool
from UserCode.RWTH3b.cmsRunController.classes.CRRootStyle import CRRootStyle
root_style = CRRootStyle()

class MyTTGammaAnalysisTool(CRSimpleHistoTool):
    """
    Calculate q_top from measurement.

    When called after a single process, superclass method start(..) is invoked,
    which passes histograms to work(...). In work, event-numbers are collected.
    After all processes do_final_calculation(...) is called.
    """

    def configure(self):
        """
        Numbers are initialized.
        """

        # (leave switches as provided)

        # Numbers for calculation
        self.N_tt_mc_sel        = 0.
        self.N_tt_sig_sel       = 0.
        self.N_tt_43_sel        = 0.

        self.N_ttgamma_sig_all  = 0.
        self.N_ttgamma_sig_sel  = 0.
        self.N_ttgamma_mc_sel   = 0.
        self.N_ttgamma_43_sel   = 0.

        self.N_tt_data_sel      = 0.
        self.N_ttgamma_data_sel = 0.

        # two2three
#        self.R_whiz_23          = 0.00285
#        self.err_R_whiz_23      = 0.0002
#        self.R_whiz_43          = 0.00732
#        self.err_R_whiz_43      = 0.0007

        # two2seven
        sigma_tt        = 165800.
        relerr_sigma_tt = 0.0802
        sigma_23        = 73.384
        relerr_sigma_23 = 0.0109
        sigma_43        = 88.09
        relerr_sigma_43 = 0.013
        self.R_whiz_23          = sigma_23 / sigma_tt
        self.err_R_whiz_23      = self.R_whiz_23 * relerr_sigma_tt
        self.R_whiz_43          = sigma_43 / sigma_tt
        self.err_R_whiz_43      = self.R_whiz_43 * relerr_sigma_tt

        self.only_folders = ["analyzeSelection"]

        # constants
        self.PRESEL_BIN = "photonInputDummy"
        self.ENDSEL_BIN = "PhotonFilthadronicoverem"


    def start(self, process):
        """
        """

        if type(process) != list:
            CRSimpleHistoTool.start(self, process)
        else:
            self.do_final_calculation()
            self.make_sqrt_R_plot()
            self.make_R_plot()
            #self.make_RN_plot()


    def work(self, histo):
        """
        """

        if not histo.GetName() == "cutflow":
            return

        endsel_bin = histo.GetXaxis().FindBin(self.ENDSEL_BIN)
        presel_bin  = histo.GetXaxis().FindBin(self.PRESEL_BIN)

        name   = self.process.name
        self.main_settings.beginGroup(name)
        legend = str(self.main_settings.value("legend").toString())
        lumi, parse_ok = self.main_settings.value("lumi").toDouble()
        if self.main_settings.value("/isData", False).toBool():
            # data
            self.N_tt_data_sel      += histo.GetBinContent(presel_bin)
            self.N_ttgamma_data_sel += histo.GetBinContent(endsel_bin)

        elif self.main_settings.value("isOverlayMc", False).toBool():
            # overlay mc
            self.N_tt_43_sel      += histo.GetBinContent(presel_bin)
            self.N_ttgamma_43_sel += histo.GetBinContent(endsel_bin)

        else:
            # mc
            if legend == "t#bar{t}#gamma #mu+Jets (Signal)":
                self.N_tt_mc_sel       += histo.GetBinContent(presel_bin)   / lumi
                self.N_tt_sig_sel      += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_sig_all += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_sig_sel += histo.GetBinContent(endsel_bin)   / lumi
                self.N_ttgamma_mc_sel  += histo.GetBinContent(endsel_bin)   / lumi

            elif legend == "t#bar{t} inclusive":
                self.N_tt_mc_sel       += histo.GetBinContent(presel_bin)   / lumi
                self.N_tt_sig_sel      += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_mc_sel  += histo.GetBinContent(endsel_bin)   / lumi

            else:
                self.N_tt_mc_sel       += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_mc_sel  += histo.GetBinContent(endsel_bin)   / lumi

        self.main_settings.endGroup() # name


    def do_final_calculation(self):
        """
        """

        # denominator (propto tt-cross section)
        purity_tt           = self.N_tt_sig_sel / self.N_tt_mc_sel
        R_data_denominator  = self.N_tt_data_sel * purity_tt

        # nominator (propto ttgamma-cross section)
        purity_ttgamma      = self.N_ttgamma_sig_sel / self.N_ttgamma_mc_sel
        efficiency_ttgamma  = self.N_ttgamma_sig_sel / self.N_ttgamma_sig_all
        R_data_nominator    = self.N_ttgamma_data_sel * purity_ttgamma\
                                / efficiency_ttgamma

        # sqrt and error (only stat. error)
        self.R_data                 = R_data_nominator / R_data_denominator
        rel_err_N_ttgamma_data_sel  = 1 / (self.N_ttgamma_data_sel**.5)
        self.err_R_data             = self.R_data * rel_err_N_ttgamma_data_sel
        self.sqrt_R_data            = self.R_data**.5
        self.err_sqrt_R_data        = 0.5 * self.err_R_data / self.R_data**.5

        # print out
        self.message.emit(self, "INFO: N_ttgamma_data_sel   = " + str(self.N_ttgamma_data_sel))
        self.message.emit(self, "INFO: pur_tt               = " + str(purity_tt))
        self.message.emit(self, "INFO: pur_ttg              = " + str(purity_ttgamma))
        self.message.emit(self, "INFO: eff_ttg              = " + str(efficiency_ttgamma))
        self.message.emit(self, "INFO: R_data_nom           = " + str(R_data_nominator))
        self.message.emit(self, "INFO: R_data_den           = " + str(R_data_denominator))
        self.message.emit(self, "INFO: R_data               = "
                                + str(self.R_data) + " +- " + str(self.err_R_data) + "(stat)"
        )
        self.message.emit(self, "INFO: R_EmCee              = "
                                + str(self.R_whiz_23) + " +- " + str(self.err_R_whiz_23)
        )
        self.message.emit(self, "INFO: R_mc43               = "
                                + str(self.R_whiz_43) + " +- " + str(self.err_R_whiz_43)
        )

        # compare only numbers
        self.N_ratio_mc   = self.N_ttgamma_mc_sel   / self.N_tt_mc_sel
        self.N_ratio_data = self.N_ttgamma_data_sel / self.N_tt_data_sel

        self.message.emit(self, "INFO: N_ratio_mc           = " + str(self.N_ratio_mc))
        self.message.emit(self, "INFO: N_ratio_data         = " + str(self.N_ratio_data))


    def make_sqrt_R_plot(self):
        """
        """

        # ttgamma crosssections taken from whizard calculation
        graph_mc = TGraphErrors(3)
        graph_mc.SetPoint(0, 0., 0.)
        graph_mc.SetPointError(0, 0., 0.1)
        graph_mc.SetPoint(1, 2./3., self.R_whiz_23**.5)
        graph_mc.SetPointError(1, 0., 0.5 * self.err_R_whiz_23 / self.R_whiz_23**.5)
        graph_mc.SetPoint(2, 4./3., self.R_whiz_43**.5)
        graph_mc.SetPointError(2, 0., 0.5 * self.err_R_whiz_43 / self.R_whiz_43**.5)
        graph_mc.SetTitle("")
        graph_mc.SetMarkerStyle(5)
        graph_mc.SetMarkerSize(1.3)
        #gStyle.SetOptFit()
        graph_mc.Fit("pol1")

        func        = graph_mc.GetFunction("pol1")
        p0          = func.GetParameter(0)
        p1          = func.GetParameter(1)
        err_p0      = func.GetParError(0)
        err_p1      = func.GetParError(1)
        q_top       = (self.sqrt_R_data - p0) / p1
        err_q_top   = (
              ( self.err_sqrt_R_data / p1 )**2
            + ( err_p0 / p1 )**2
            + ( err_p1 * q_top / p1 )**2
                          )**.5

        graph_data = TGraphErrors(2)
        graph_data.SetPoint(0, 0.03, self.sqrt_R_data)
        graph_data.SetPointError(0, 0., self.err_sqrt_R_data)
        graph_data.SetPoint(1, q_top, 0.014)
        graph_data.SetPointError(1, err_q_top, 0.)
        graph_data.SetLineWidth(2)
        graph_data.SetMarkerSize(1.3)
        graph_data.SetMarkerStyle(20)
        graph_data.SetLineColor(kRed + 2)
        graph_data.SetMarkerColor(kRed + 2)

        canvas = TCanvas("sqrt_R_ratio", "sqrt_R_ratio")
        graph_mc.SetTitle("#sqrt{R_{MC}} vs. q_{top}")
        graph_mc.Draw("AP")
        graph_mc.GetYaxis().SetRangeUser(0.01, 0.11)
        graph_data.Draw("P")
        #graph_data.SetTitle("R_{Data}")
        #canvas.BuildLegend()

        pl1 = TPaveLabel(0.7298,0.016,1.2064,0.0240,
            "q_{top} = %.2f"%q_top + " #pm %.2f"%err_q_top ,"br")
        pl1.SetBorderSize(1)
        pl1.SetTextSize(0.99)
        pl1.Draw()
        pl2 = TPaveLabel(0.0414,0.055,0.6042,0.0659,
            "R_{Data} = ( %.2f"%(self.R_data*1000) + " #pm %.2f"%(self.err_R_data*1000) + " )#upoint10^{-3}" ,"br")
        pl2.SetBorderSize(1)
        pl2.SetTextSize(0.4)
        pl2.Draw()
        arrow1 = TArrow(0.05295656,0.04772727,0.4190476,0.04772727,0.01,"|>")
        arrow1.SetFillColor(4)
        arrow1.SetFillStyle(1001)
        arrow1.SetLineColor(4)
        arrow1.Draw()
        arrow2 = TArrow(0.5479853,0.04363636,0.5479853,0.01795455,0.01,"|>")
        arrow2.SetFillColor(4)
        arrow2.SetFillStyle(1001)
        arrow2.SetLineColor(4)
        arrow2.Draw()
        arrow3 = TArrow(1.100576,0.1,1.013082,0.0725,0.01,"|>")
        arrow3.SetFillColor(1)
        arrow3.SetFillStyle(1001)
        arrow3.Draw()

        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(root_style.DIR_PLOTS + "/sqrt_R_ratio.root")
        canvas.SaveAs(root_style.DIR_PLOTS + "/sqrt_R_ratio.png")


    def make_R_plot(self):
        """
        """

        para_str = "[0]*x*x + [1]"
        inve_str = "sqrt( (x-[1])/[0] )"
        # ttgamma crosssections taken from whizard calculation
        graph_mc = TGraphErrors(3)
        graph_mc.SetPoint(0, -.05 , 0.0014)
        graph_mc.SetPointError(0, 0., 0.002)
        graph_mc.SetPoint(1, 2./3., self.R_whiz_23)
        graph_mc.SetPointError(1, 0., self.err_R_whiz_23)
        graph_mc.SetPoint(2, 4./3., self.R_whiz_43)
        graph_mc.SetPointError(2, 0., self.err_R_whiz_43)
        graph_mc.SetMarkerStyle(5)
        graph_mc.SetMarkerSize(1.3)

        # R = a*q**2 + c
        #a = 9./12.*(self.R_whiz_43 - self.R_whiz_23)
        #c = self.R_whiz_23 - a*4./9.
        func = TF1("parabola", para_str, -0.1, 1.5)
        #func.SetParameter(0, a)
        #func.SetParameter(1, c)
        graph_mc.Fit(func)
        a       = func.GetParameter(0)
        err_a   = func.GetParError(0)
        c       = func.GetParameter(1)
        err_c   = func.GetParError(1)

        func_p = TF1("parabola_p", para_str, -0.1, 1.5)
        func_p.SetParameter(0, a + err_a)
        func_p.SetParameter(1, c + err_c)
        func_p.SetLineWidth(0)
        func_p.SetFillColor(kYellow)
        func_m = TF1("parabola_m", para_str, -0.1, 1.5)
        func_m.SetParameter(0, a - err_a)
        func_m.SetParameter(1, c - err_c)
        func_m.SetLineWidth(0)
        func_m.SetFillColor(kRed)

        inve = TF1("inverse", inve_str, 0.001, 1.)
        inve.SetParameter(0, a)
        inve.SetParameter(1, c)
        inve_m = TF1("inverse_m", inve_str, 0.001, 1.)
        inve_m.SetParameter(0, a-err_a)
        inve_m.SetParameter(1, c-err_c)
        inve_p = TF1("inverse_p", inve_str, 0.001, 1.)
        inve_p.SetParameter(0, a+err_a)
        inve_p.SetParameter(1, c+err_a)
        q_top       = inve.Eval(self.R_data)
        err_m_q_top =   q_top - inve_p.Eval(self.R_data - self.err_R_data)
        err_p_q_top = - q_top + inve_m.Eval(self.R_data + self.err_R_data)

        graph_data = TGraphAsymmErrors(2)
        graph_data.SetPoint(0, 0.03, self.R_data)
        graph_data.SetPointError(0, 0., 0., self.err_R_data, self.err_R_data)
        graph_data.SetPoint(1, q_top, 0.0004)
        graph_data.SetPointError(1, err_m_q_top, err_p_q_top, 0., 0.)
        graph_data.SetLineWidth(2)
        graph_data.SetMarkerSize(1.3)
        graph_data.SetMarkerStyle(20)
        graph_data.SetLineColor(kRed + 2)
        graph_data.SetMarkerColor(kRed + 2)

        frame = TGraph(2)
        frame.SetPoint(0, 0., 0.0002)
        frame.SetPoint(1, 1.4, 0.001)
        frame.SetMarkerColor(kWhite)
        frame.SetTitle("R_{MC} vs. q_{top};q_top / e;R")

        canvas = TCanvas("R_ratio", "R_ratio")
        frame.Draw("AP")
        func_p.Draw("FCsame")
        func_m.Draw("FCsame")
        func.Draw("same")
        graph_mc.Draw("P")
        graph_data.Draw("P")

#        pl2 = TPaveLabel(0.05,0.00425,0.65,0.0055,
#            "R_{Data} = ( %.2f"%(self.R_data*1000) + " #pm %.2f"%(self.err_R_data*1000) + " )#upoint10^{-3}" ,"br")
#        pl2.SetBorderSize(1)
#        pl2.SetTextSize(0.4)
#        pl2.Draw()
#        pl1 = TPaveLabel(0.9,0.00075,1.4,0.002,
#            "q_{top} = %.2f"%q_top
#            + "^{+ %.2f}"%err_p_q_top
#            + "_{- %.2f}"%err_m_q_top
#            + " e","br")
#        pl1.SetBorderSize(1)
#        pl1.SetTextSize(0.4)
#        pl1.Draw()

        pt = TPaveText(1.109795,0.0008117579,1.585046,0.00105,"br")
        pt.SetBorderSize(1)
        pt.SetTextAlign(12)
        pt.SetTextSize(0.04)
        pt.AddText("R = a #upoint q_{top}^{2} + c")
        pt.AddText("a = (%.2f"%(a*1000) + " #pm %.2f)"%(err_a*1000))
        pt.AddText("c = (%.2f"%(c*1000) + " #pm %.2f)"%(err_c*1000))
        pt.Draw()

#        arrow2 =  TArrow(0.065,self.R_data,0.5,self.R_data,0.01,"|>")
#        arrow2.SetFillColor(4)
#        arrow2.SetFillStyle(1001)
#        arrow2.SetLineColor(4)
#        arrow2.SetLineWidth(2)
#        arrow2.Draw()
#        arrow3 =  TArrow(q_top,0.002,q_top,0.00087,0.01,"|>")
#        arrow3.SetFillColor(4)
#        arrow3.SetFillStyle(1001)
#        arrow3.SetLineColor(4)
#        arrow3.SetLineWidth(2)
#        arrow3.Draw()
#        arrow1 =  TArrow(0.9162637,0.007155,1.097582,0.0057825,0.01,"|>")
#        arrow1.SetFillColor(1)
#        arrow1.SetFillStyle(1001)
#        arrow1.SetLineWidth(2)
#        arrow1.Draw()

        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(root_style.DIR_PLOTS + "/R_ratio.root")
        canvas.SaveAs(root_style.DIR_PLOTS + "/R_ratio.png")


    def make_RN_plot(self):
        """
        """

        # get all numbers _with errors_ from cutflow
        file_cutflow = TFile(
            root_style.DIR_PLOTS
            + "/HistogramStacks/allStacks/stacks/analyzeSelection_cutflow.root",
            "READ"
        )

        stackmc = file_cutflow.GetKey("analyzeSelection_cutflow_mc").ReadObj()
        stack43 = file_cutflow.GetKey("analyzeSelection_cutflow_overlay_mc").ReadObj()
        stackda = file_cutflow.GetKey("analyzeSelection_cutflow_data").ReadObj()

        histo_23 = None
        histo_bg = None
        for histo in stackmc.GetHists():
            if histo.GetTitle() == "Signal":
                histo_23 = histo.Clone()
            else:
                if not histo_bg:
                    histo_bg = histo.Clone()
                else:
                    histo_bg.Add(histo)

        histo_43 = stack43.GetHists()[0].Clone()
        histo_da = stackda.GetHists()[0].Clone()

        histo_full_23 = histo_bg.Clone()
        histo_full_23.Add(histo_23)
        histo_full_43 = histo_bg.Clone()
        histo_full_43.Add(histo_43)

        # interesting bins
        delta_R_bin = histo_23.GetXaxis().FindBin(self.ENDSEL_BIN)
        presel_bin  = histo_23.GetXaxis().FindBin(self.PRESEL_BIN)

        # Get 2/3 ratio with error
        N_23_sel        = histo_full_23.GetBinContent(delta_R_bin)
        err_N_23_sel    = histo_full_23.GetBinError(delta_R_bin)
        N_23_all        = histo_full_23.GetBinContent(presel_bin)
        err_N_23_all    = histo_full_23.GetBinError(presel_bin)
        RN_23 = N_23_sel / N_23_all
        err_RN_23 = RN_23 * ( (err_N_23_sel/N_23_sel)**2
                              + (err_N_23_all/N_23_all)**2 )**.5

        # Get 4/3 ratio with error
        N_43_sel        = histo_full_43.GetBinContent(delta_R_bin)
        err_N_43_sel    = histo_full_43.GetBinError(delta_R_bin)
        N_43_all        = histo_full_43.GetBinContent(presel_bin)
        err_N_43_all    = histo_full_43.GetBinError(presel_bin)
        RN_43 = N_43_sel / N_43_all
        err_RN_43 = RN_43 * ( (err_N_43_sel/N_43_sel)**2
                              + (err_N_43_all/N_43_all)**2 )**.5

        # Get data ratio with error
        N_da_sel        = histo_da.GetBinContent(delta_R_bin)
        err_N_da_sel    = histo_da.GetBinError(delta_R_bin)
        N_da_all        = histo_da.GetBinContent(presel_bin)
        err_N_da_all    = histo_da.GetBinError(presel_bin)
        RN_da = N_da_sel / N_da_all
        err_RN_da = RN_da * ( (err_N_da_sel/N_da_sel)**2
                              + (err_N_da_all/N_da_all)**2 )**.5

        graph_mc = TGraphErrors(2)
        graph_mc.SetPoint(0, 2./3., RN_23)
        graph_mc.SetPointError(0, 0., err_RN_23)
        graph_mc.SetPoint(1, 4./3., RN_43)
        graph_mc.SetPointError(1, 0., err_RN_43)
        graph_mc.SetMarkerStyle(5)
        graph_mc.SetMarkerSize(1.3)

        # R = a*q**2 + c
        a = 9./12.*(RN_43 - RN_23)
        c = RN_23 - a*4./9.
        func = TF1("parabola", "[0]*x*x + [1]", -0.1, 1.5)
        func.SetParameter(0, a)
        func.SetParameter(1, c)
        inve = TF1("inverse", "sqrt( (x-[1])/[0] )", 0.001, 1.)
        inve.SetParameter(0, a)
        inve.SetParameter(1, c)
        q_top       = inve.Eval(RN_da)
        err_m_q_top =   q_top - inve.Eval(RN_da - err_RN_da)
        err_p_q_top = - q_top + inve.Eval(RN_da + err_RN_da)

        graph_data = TGraphAsymmErrors(2)
        graph_data.SetPoint(0, 0.03, RN_da)
        graph_data.SetPointError(0, 0., 0., err_RN_da, err_RN_da)
        graph_data.SetPoint(1, q_top, 0.0004)
        graph_data.SetPointError(1, err_m_q_top, err_p_q_top, 0., 0.)
        graph_data.SetLineWidth(2)
        graph_data.SetMarkerSize(1.3)
        graph_data.SetMarkerStyle(20)
        graph_data.SetLineColor(kRed + 2)
        graph_data.SetMarkerColor(kRed + 2)

        frame = TGraph(2)
        frame.SetPoint(0, 0., 0.)
        frame.SetPoint(1, 1.4, 0.025)
        frame.SetMarkerColor(kWhite)
        frame.SetTitle("R_{MC} vs. q_{top}")

        canvas = TCanvas("RN_ratio", "RN_ratio")
        frame.Draw("AP")
        func.Draw("same")
        graph_mc.Draw("P")
        graph_data.Draw("P")

        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(root_style.DIR_PLOTS + "/RN_ratio.root")
        canvas.SaveAs(root_style.DIR_PLOTS + "/RN_ratio.png")





