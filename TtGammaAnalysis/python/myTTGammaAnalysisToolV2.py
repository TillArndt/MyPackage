__author__ = 'Heiner Tholen'

from ROOT import TGraph, TGraphErrors, TGraphAsymmErrors, TF1, gStyle, \
    TCanvas, TArrow, TPaveLabel, TPaveText, TLatex, TFile, \
    kRed, kYellow, kGreen, kWhite
from UserCode.RWTH3b.cmsRunController.classes.CRPostProcessor import CRPostProcTool
from UserCode.RWTH3b.cmsRunController.classes.CRRootStyle import CRRootStyle
root_style = CRRootStyle()

class MyTTGammaAnalysisToolV2(CRPostProcTool):
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
            #self.make_RN_plot("two2three")
            self.make_RN_plot("two2five")
            self.make_RN_plot("two2seven")


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


    def make_RN_plot(self, name):
        """
        """

        self.message.emit(self, "INFO Making R_N plot")

        root_style.DIR_PLOTS_R = root_style.DIR_PLOTS + "R-Plots/"
        root_style.create_folders()

        # get cutflow histos from fileservice NOT SCALED TO LUMI
        file_cutflow_23 = TFile(
            root_style.DIR_FILESERVICE + name + ".root",
            "READ"
        )
        file_cutflow_43 = TFile(
            root_style.DIR_FILESERVICE + name + "_43.root",
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

        frame = TGraph(2)
        dy = RN_43 - RN_23
        frame.SetPoint(0, 0., RN_43 + dy)
        frame.SetPoint(1, 1.4, RN_23 - dy)
        frame.SetMarkerColor(kWhite)
        frame.SetTitle("")#R_{N,MC} vs. q_{top};q_top / e;R")
        frame.GetYaxis().SetNoExponent()

        canvas = TCanvas("R_ratio", "R_ratio")
        frame.Draw("AP")
        graph_mc.Draw("Psame")
        func_p.Draw("FCsame")
        func_m.Draw("FCsame")
        func.Draw("same")
        #graph_data.Draw("P")

        pt = TPaveText(0.2,0.6,0.5,0.80,"brNDC")
        pt.SetBorderSize(1)
        pt.SetTextAlign(12)
        pt.SetTextSize(0.04)
        pt.AddText("R = a #upoint q_{top}^{2} + c")
        pt.AddText("a = (%.2f"%(a*1000) + " #pm %.2f)#upoint 10^{-3}"%(err_a*1000))
        pt.AddText("c = (%.2f"%(c*1000) + " #pm %.2f)#upoint 10^{-3}"%(err_c*1000))
        pt.Draw()

        canvas.Modified()
        canvas.Update()
        canvas.SaveAs(root_style.DIR_PLOTS_R + "/RN_ratio_" + name + ".root")
        canvas.SaveAs(root_style.DIR_PLOTS_R + "/RN_ratio_" + name + ".png")
        canvas.SaveAs(root_style.DIR_PLOTS_R + "/RN_ratio_" + name + ".eps")

