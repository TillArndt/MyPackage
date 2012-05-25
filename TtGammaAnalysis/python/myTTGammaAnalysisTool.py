__author__ = 'Heiner Tholen'

from ROOT import TGraphErrors, TF1, gStyle, TCanvas, TArrow, TPaveLabel, kRed
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

        self.N_ttgamma_sig_all  = 0.
        self.N_ttgamma_sig_sel  = 0.
        self.N_ttgamma_mc_sel   = 0.

        self.N_tt_data_sel      = 0.
        self.N_ttgamma_data_sel = 0.

        self.only_folders = ["cutflow"]

        
    def start(self, process):
        """
        """

        if type(process) != list:
            CRSimpleHistoTool.start(self, process)
        else:
            self.do_final_calculation()


    def work(self, histo):
        """
        """

        if not histo.GetName() == "cutflow_selectionPath":
            return

        delta_R_bin = histo.GetXaxis().FindBin("#DeltaR(photon, jet)")
        presel_bin  = histo.GetXaxis().FindBin("preselected")

        name   = self.process.name
        self.main_settings.beginGroup(name)
        legend = str(self.main_settings.value("legend").toString())
        lumi, parse_ok = self.main_settings.value("lumi").toDouble()
        if self.main_settings.value("/isData", False).toBool():
            # data
            self.N_tt_data_sel      += histo.GetBinContent(presel_bin)
            self.N_ttgamma_data_sel += histo.GetBinContent(delta_R_bin)

        elif self.main_settings.value("isOverlayMc", False).toBool():
            # overlay mc
            pass

        else:
            # mc
            if legend == "Signal":
                self.N_tt_mc_sel       += histo.GetBinContent(presel_bin)   / lumi
                self.N_tt_sig_sel      += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_sig_all += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_sig_sel += histo.GetBinContent(delta_R_bin)  / lumi
                self.N_ttgamma_mc_sel  += histo.GetBinContent(delta_R_bin)  / lumi

            elif legend == "Semi-#mu t#bart":
                self.N_tt_mc_sel       += histo.GetBinContent(presel_bin)   / lumi
                self.N_tt_sig_sel      += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_mc_sel  += histo.GetBinContent(delta_R_bin)  / lumi

            else:
                self.N_tt_mc_sel       += histo.GetBinContent(presel_bin)   / lumi
                self.N_ttgamma_mc_sel  += histo.GetBinContent(delta_R_bin)  / lumi

        self.main_settings.endGroup() # name


    def do_final_calculation(self):
        """
        """

        # denominator (propto tt-cross section)
        purity_tt = self.N_tt_sig_sel / self.N_tt_mc_sel
        R_data_denominator = self.N_tt_data_sel * purity_tt

        # nominator (propto ttgamma-cross section)
        purity_ttgamma = self.N_ttgamma_sig_sel / self.N_ttgamma_mc_sel
        efficiency_ttgamma = self.N_ttgamma_sig_sel / self.N_ttgamma_sig_all
        R_data_nominator = self.N_ttgamma_data_sel * purity_ttgamma\
        / efficiency_ttgamma

        R_data = R_data_nominator / R_data_denominator

        # sqrt and error (only stat. error)
        rel_err_N_ttgamma_data_sel = 1 / (self.N_ttgamma_data_sel**.5)
        err_R_data = R_data * rel_err_N_ttgamma_data_sel
        sqrt_R_data     = R_data**.5
        err_sqrt_R_data = 0.5 * err_R_data / R_data**.5

        # print out
        self.message.emit(self, "INFO: pur_tt = "     + str(purity_tt))
        self.message.emit(self, "INFO: pur_ttg = "    + str(purity_ttgamma))
        self.message.emit(self, "INFO: eff_ttg = "    + str(efficiency_ttgamma))
        self.message.emit(self, "INFO: R_data_nom = " + str(R_data_nominator))
        self.message.emit(self, "INFO: R_data_den = " + str(R_data_denominator))
        self.message.emit(
            self,
            "INFO: R_data = " + str(R_data) + " +- " + str(err_R_data) + "(stat)"
        )
        self.message.emit(
            self,
            "INFO: R_EmCee = 0.00285 +- 0.0002"
        )
        self.message.emit(
            self,
            "INFO: R_mc43 = 0.00732 +- 0.0007"
        )

        # compare only numbers
        N_ratio_mc   = self.N_ttgamma_mc_sel   / self.N_tt_mc_sel
        N_ratio_data = self.N_ttgamma_data_sel / self.N_tt_data_sel

        self.message.emit(self, "INFO: N_ratio_mc = " + str(N_ratio_mc))
        self.message.emit(self, "INFO: N_ratio_data = " + str(N_ratio_data))

        graph_mc = TGraphErrors(3)
        graph_mc.SetPoint(0, 0., 0.)
        graph_mc.SetPointError(0, 0., 0.1)
        graph_mc.SetPoint(1, 2./3., 0.00285**.5)
        graph_mc.SetPointError(1, 0., 0.5 * 0.0002 / 0.00285**.5)
        graph_mc.SetPoint(2, 4./3., 0.00732**.5)
        graph_mc.SetPointError(2, 0., 0.5 * 0.0007 / 0.00732**.5)
        graph_mc.SetTitle("")
        graph_mc.SetMarkerStyle(5)
        graph_mc.SetMarkerSize(1.3)
        gStyle.SetOptFit()
        graph_mc.Fit("pol1")

        func        = graph_mc.GetFunction("pol1")
        p0          = func.GetParameter(0)
        p1          = func.GetParameter(1)
        err_p0      = func.GetParError(0)
        err_p1      = func.GetParError(1)
        q_top       = (sqrt_R_data - p0) / p1
        err_q_top   = (
              ( err_sqrt_R_data / p1 )**2
            + ( err_p0 / p1 )**2
            + ( err_p1 * q_top / p1 )**2
                          )**.5

        graph_data = TGraphErrors(2)
        graph_data.SetPoint(0, 0.03, sqrt_R_data)
        graph_data.SetPointError(0, 0., err_sqrt_R_data)
        graph_data.SetPoint(1, q_top, 0.014)
        graph_data.SetPointError(1, err_q_top, 0.)
        graph_data.SetLineWidth(2)
        graph_data.SetMarkerSize(1.3)
        graph_data.SetMarkerStyle(20)
        graph_data.SetLineColor(kRed + 2)
        graph_data.SetMarkerColor(kRed + 2)

        canvas = TCanvas("R_ratio", "R_ratio")
        graph_mc.Draw("AP")
        graph_mc.GetYaxis().SetRangeUser(0.01, 0.11)
        graph_data.Draw("P")
        graph_mc.SetTitle("#sqrt{R_{MC}} vs. q_{top}")
        #graph_data.SetTitle("R_{Data}")
        #canvas.BuildLegend()

        pl1 = TPaveLabel(0.7298,0.016,1.2064,0.0240,
            "q_{top} = %.2f"%q_top + " #pm %.2f"%err_q_top ,"br")
        pl1.SetBorderSize(1)
        pl1.SetTextSize(0.99)
        pl1.Draw()
        pl2 = TPaveLabel(0.0414,0.055,0.6042,0.0659,
            "R_{Data} = ( %.2f"%(R_data*1000) + " #pm %.2f"%(err_R_data*1000) + " )#upoint10^{-3}" ,"br")
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
        canvas.SaveAs(root_style.DIR_PLOTS + "/R_ratio.root")
        canvas.SaveAs(root_style.DIR_PLOTS + "/R_ratio.png")


