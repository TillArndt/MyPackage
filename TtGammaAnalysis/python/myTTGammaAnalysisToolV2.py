__author__ = 'Heiner Tholen'

from ROOT import TGraph, TGraphErrors, TGraphAsymmErrors, TF1, gStyle, \
    TCanvas, TArrow, TPaveLabel, TPaveText, TFile, \
    kRed, kYellow, kGreen, kWhite
from UserCode.RWTH3b.cmsRunController.classes.CRPostProcessor import CRPostProcTool
from UserCode.RWTH3b.cmsRunController.classes.CRRootStyle import CRRootStyle
root_style = CRRootStyle()

class MyTTGammaAnalysisTool(CRPostProcTool):
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

        # only after all steps
        self.after_every_process = False

        # two2three
#        self.R_whiz_23          = 0.00285
#        self.err_R_whiz_23      = 0.0002
#        self.R_whiz_43          = 0.00732
#        self.err_R_whiz_43      = 0.0007

        # two2seven
#        sigma_tt        = 165800.
#        relerr_sigma_tt = 0.0802
#        sigma_23        = 73.384
#        relerr_sigma_23 = 0.0109
#        sigma_43        = 88.09
#        relerr_sigma_43 = 0.013
#        self.R_whiz_23          = sigma_23 / sigma_tt
#        self.err_R_whiz_23      = self.R_whiz_23 * relerr_sigma_tt
#        self.R_whiz_43          = sigma_43 / sigma_tt
#        self.err_R_whiz_43      = self.R_whiz_43 * relerr_sigma_tt

        self.para_str = "[0]*x*x + [1]"
        self.inve_str = "sqrt( (x-[1])/[0] )"


    def start(self, process):
        """
        """

        if type(process) == list:
            self.make_RN_plot()


    def calc_ratio_from_cutflow(self, histo):
        """
        """

        histo.Sumw2()

        # interesting bins
        first_bin  = histo.GetXaxis().GetFirst()
        last_bin = histo.GetXaxis().GetLast()

        # Get 2/3 ratio with error
        N_sel        = histo.GetBinContent(last_bin)
        err_N_sel    = histo.GetBinError(last_bin)
        N_all        = histo.GetBinContent(first_bin)
        err_N_all    = histo.GetBinError(first_bin)
        RN = N_sel / N_all
        err_RN = RN * ( (err_N_sel/N_sel)**2
                              + (err_N_all/N_all)**2 )**.5

        return RN, err_RN


    def make_RN_plot(self):
        """
        """

        self.message.emit(self, "INFO Making R_N plot")

        # get cutflow histos from fileservice NOT SCALED TO LUMI
        file_cutflow_23 = TFile(
            root_style.DIR_FILESERVICE + "two2seven.root",
            "READ"
        )
        file_cutflow_43 = TFile(
            root_style.DIR_FILESERVICE + "two2seven_43.root",
            "READ"
        )
        histo_23 = file_cutflow_23.GetKey("analyzeSelection").ReadObj().GetKey("cutflow").ReadObj()
        histo_43 = file_cutflow_43.GetKey("analyzeSelection").ReadObj().GetKey("cutflow").ReadObj()

        RN_23, err_RN_23 = self.calc_ratio_from_cutflow(histo_23)
        RN_43, err_RN_43 = self.calc_ratio_from_cutflow(histo_43)

        graph_mc = TGraphErrors(2)
        graph_mc.SetPoint(0, 2./3., RN_23)
        graph_mc.SetPointError(0, 0., err_RN_23)
        graph_mc.SetPoint(1, 4./3., RN_43)
        graph_mc.SetPointError(1, 0., err_RN_43)
        graph_mc.SetMarkerStyle(5)
        graph_mc.SetMarkerSize(1.3)

        func = TF1("parabola", self.para_str, -0.1, 1.5)
        graph_mc.Fit(func)
        a       = func.GetParameter(0)
        err_a   = func.GetParError(0)
        c       = func.GetParameter(1)
        err_c   = func.GetParError(1)

        func_p = TF1("parabola_p", self.para_str, -0.1, 1.5)
        func_p.SetParameter(0, a + err_a)
        func_p.SetParameter(1, c + err_c)
        func_p.SetLineWidth(0)
        func_p.SetFillColor(kYellow)
        func_m = TF1("parabola_m", self.para_str, -0.1, 1.5)
        func_m.SetParameter(0, a - err_a)
        func_m.SetParameter(1, c - err_c)
        func_m.SetLineWidth(0)
        func_m.SetFillColor(kRed)

        canvas = TCanvas("R_ratio", "R_ratio")
        #frame.Draw("AP")
        graph_mc.Draw("AP")
        func_p.Draw("FCsame")
        func_m.Draw("FCsame")
        func.Draw("same")
        #graph_data.Draw("P")

        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(root_style.DIR_PLOTS + "/R_ratio.root")
        canvas.SaveAs(root_style.DIR_PLOTS + "/R_ratio.png")


#
#
#        histo_da = stackda.GetHists()[0].Clone()
#
#        # Get data ratio with error
#        N_da_sel        = histo_da.GetBinContent(last_bin)
#        err_N_da_sel    = histo_da.GetBinError(last_bin)
#        N_da_all        = histo_da.GetBinContent(first_bin)
#        err_N_da_all    = histo_da.GetBinError(first_bin)
#        RN_da = N_da_sel / N_da_all
#        err_RN_da = RN_da * ( (err_N_da_sel/N_da_sel)**2
#                              + (err_N_da_all/N_da_all)**2 )**.5
#        # R = a*q**2 + c
#        a = 9./12.*(RN_43 - RN_23)
#        c = RN_23 - a*4./9.
#        func = TF1("parabola", "[0]*x*x + [1]", -0.1, 1.5)
#        func.SetParameter(0, a)
#        func.SetParameter(1, c)
#        inve = TF1("inverse", "sqrt( (x-[1])/[0] )", 0.001, 1.)
#        inve.SetParameter(0, a)
#        inve.SetParameter(1, c)
#        q_top       = inve.Eval(RN_da)
#        err_m_q_top =   q_top - inve.Eval(RN_da - err_RN_da)
#        err_p_q_top = - q_top + inve.Eval(RN_da + err_RN_da)
#
#        graph_data = TGraphAsymmErrors(2)
#        graph_data.SetPoint(0, 0.03, RN_da)
#        graph_data.SetPointError(0, 0., 0., err_RN_da, err_RN_da)
#        graph_data.SetPoint(1, q_top, 0.0004)
#        graph_data.SetPointError(1, err_m_q_top, err_p_q_top, 0., 0.)
#        graph_data.SetLineWidth(2)
#        graph_data.SetMarkerSize(1.3)
#        graph_data.SetMarkerStyle(20)
#        graph_data.SetLineColor(kRed + 2)
#        graph_data.SetMarkerColor(kRed + 2)
#
#        frame = TGraph(2)
#        frame.SetPoint(0, 0., 0.)
#        frame.SetPoint(1, 1.4, 0.025)
#        frame.SetMarkerColor(kWhite)
#        frame.SetTitle("R_{MC} vs. q_{top}")
#
#        canvas = TCanvas("RN_ratio", "RN_ratio")
#        frame.Draw("AP")
#        func.Draw("same")
#        graph_mc.Draw("P")
#        graph_data.Draw("P")
#
#        canvas.Modified()
#        canvas.Update()
#        canvas.SaveAs(root_style.DIR_PLOTS + "/RN_ratio.root")
#        canvas.SaveAs(root_style.DIR_PLOTS + "/RN_ratio.png")


#file_cutflow = TFile(
#    root_style.DIR_PLOTS
#    + "/HistogramStacks/allStacks/stacks/analyzeSelection_cutflow.root",
#    "READ"
#)
#
#stackmc = file_cutflow.GetKey("analyzeSelection_cutflow_mc").ReadObj()
#histo_bg = None
#for histo in stackmc.GetHists():
#    if histo.GetTitle() != "Signal":
#        if not histo_bg:
#            histo_bg = histo.Clone()
#        else:
#            histo_bg.Add(histo)
#
#histo_full_23 = histo_bg.Clone()
#histo_full_23.Add(histo_23)
#histo_full_43 = histo_bg.Clone()
#histo_full_43.Add(histo_43)


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
        #func.SetParameter(0, a)
        #func.SetParameter(1, c)
        func = TF1("parabola", para_str, -0.1, 1.5)
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
