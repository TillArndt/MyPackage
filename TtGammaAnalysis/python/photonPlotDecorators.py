
from UserCode.RWTH3b.cmsRunController.classes.CRDecorator import CRDecorator

class CRSingleStacker_crtlPlts_CrtlFilteta_histo(CRDecorator):
    """
    move legend.
    """

    def prepare_to_save_log(self):
        self.decoratee.prepare_to_save_log()
        self.legend.SetX1NDC(0.43)
        self.legend.SetX2NDC(0.67)
        self.legend.SetY1NDC(0.04)
        self.legend.SetY2NDC(0.36)


class CRSingleStacker_crtlPlts_CrtlFiltptrelDrjet_histo(CRDecorator):
    """
    move legend.
    """

    def prepare_to_save_log(self):
        self.decoratee.prepare_to_save_log()
        self.legend.SetX1NDC(0.33)
        self.legend.SetX2NDC(0.57)
        self.legend.SetY1NDC(0.04)
        self.legend.SetY2NDC(0.36)


class CRSingleStacker_crtlPlts_CrtlFiltdrmuon_histo(CRDecorator):
    """
    move legend.
    """

    def prepare_to_save_log(self):
        self.decoratee.prepare_to_save_log()
        self.legend.SetX1NDC(0.33)
        self.legend.SetX2NDC(0.57)
        self.legend.SetY1NDC(0.04)
        self.legend.SetY2NDC(0.36)


class CRSingleStacker_crtlPlts_CrtlFilthaspixelseeds_histo(CRDecorator):
    """
    move legend.
    """

    def prepare_to_save_log(self):
        self.decoratee.prepare_to_save_log()
        self.legend.SetX1NDC(0.23)
        self.legend.SetX2NDC(0.47)
        self.legend.SetY1NDC(0.04)
        self.legend.SetY2NDC(0.36)


class CRSingleStacker_cutflow_analyzeSelection_cutflow(CRDecorator):
    """
    adjust ratio plot
    """

    def configure(self):

        rp = self.get_decorator("CRRatioPlotDataMC")
        rp.dec_par["y_min"] = 0.5
        rp.dec_par["y_max"] = 1.8

#        ar = self.insert_decorator("CRAxisRangeX")
#        ar.dec_par["low"] = 0
#        ar.dec_par["high"] = 10

        self.decoratee.configure()


class CRSingleTemplateHistoWorker_compare357_NoShower_analyzeSelection_cutflow(CRDecorator):

#    def configure(self):
#        ar = self.insert_decorator("CRAxisRangeX")
#        ar.dec_par["low"] = 0
#        ar.dec_par["high"] = 10
#        self.decoratee.configure()

    def do_final_cosmetics(self):
        self.decoratee.do_final_cosmetics()
        #self.first_drawed.GetYaxis().SetMoreLogLabels()
        self.first_drawed.SetMaximum(self.y_max * 1.4)


class CRSingleTemplateHistoWorker_compare357_YesShower_analyzeSelection_cutflow(
    CRSingleTemplateHistoWorker_compare357_NoShower_analyzeSelection_cutflow
): pass


from ROOT import TCanvas

class AdjustRatioInShowerThree(CRDecorator):

    def configure(self):
        canvas_name = self.get_canvas_name()
        if canvas_name.count("ShowerThree"):
            ratio_dec = self.get_decorator("CRRatioHistoPlotter")
            if canvas_name.count("cutflow"):
                ratio_dec.dec_par["y_min"] = 1.5
                ratio_dec.dec_par["y_max"] = 4.5
            else:
                ratio_dec.dec_par["y_min"] = 1.
                ratio_dec.dec_par["y_max"] = 5.5

        self.decoratee.configure()


    def draw_full_plot(self):
        name = self.get_canvas_name()
        self.canvas = TCanvas(name, name, 500, 500)
        self.main_pad = self.canvas
        self.decoratee.draw_full_plot()

