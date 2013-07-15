
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.generators as gen
import cmstoolsac3b.wrappers as wrp
import cmstoolsac3b.decorator as dec
import cmstoolsac3b.settings as settings
from cmstoolsac3b.rendering import BottomPlotRatio

from PyQt4 import QtCore
from ROOT import TF1, TPaveText
import itertools


class TemplateFitTool(ppt.FSStackPlotter):

    def __init__(self, name = None):
        super(TemplateFitTool, self).__init__(name)
        self.name_real  = ""
        self.name_fake  = ""
        self.name_data  = ""
        self.name_histo = ""

    def configure(self):
        super(TemplateFitTool,self).configure()
        self.save_name_lambda = lambda wrp: self.plot_output_dir + wrp.name.split("_")[1]

    def find_x_range(self, data_hist):
        x_min = data_hist.GetXaxis().GetXmin()
        x_max = data_hist.GetXaxis().GetXmax()
        for i in xrange(data_hist.GetNbinsX()):
            if data_hist.GetBinContent(i):
                x_min = data_hist.GetXaxis().GetBinLowEdge(i)
                break
        for i in xrange(data_hist.GetNbinsX() - 1, 0, -1):
            if data_hist.GetBinContent(i):
                x_max = data_hist.GetXaxis().GetBinUpEdge(i)
                break
        self.x_min = x_min
        self.x_max = x_max

    def build_fit_function(self, template_wrappers):
        templates = [tw.histo for tw in template_wrappers]
        size = len(templates)

        def fit_func(x, par):
            value = 0.
            for i, hist in enumerate(templates):
                value += par[i] * hist.GetBinContent(hist.FindBin(x[0]))
            return value

        tf1 = TF1(
            "FitFunc",
            fit_func,
            self.x_min,
            self.x_max,
            size
        )
        for i in xrange(0, size):
            tf1.SetParameter(i,1.)

        return tf1

    def save_fit_results(self, fit_function, templates):
        """
        """

        file = QtCore.QSettings(
            self.plot_output_dir + "FitResults.ini", 1
        )
        file.setValue("Chi2", fit_function.GetChisquare())
        file.setValue("NDF", fit_function.GetNDF())

        file.beginWriteArray("parameters")
        for i, tmplt in enumerate(templates):
            file.setArrayIndex(i)
            file.setValue("legend", tmplt.legend)
            file.setValue("value", fit_function.GetParameter(i))
            file.setValue("error", fit_function.GetParError(i))
            file.setValue("binIntegral", tmplt.histo.Integral())
        file.endArray()
        file.sync()
        del file

    def scale_templates_to_fit(self, fit_function, templates):
        for i in range(0, len(templates)):
            #TODO: use gen functions here
            templates[i].histo.Scale(fit_function.GetParameter(i))

    def make_fit_textbox(self, fit_function, templates):
        x1, x2, y2 = 0.33, 0.62, 0.88
        y1 = y2 - ((len(templates) + 1) * 0.04)

        textbox = TPaveText(x1,y1,x2,y2,"brNDC")
        textbox.SetBorderSize(1)
        textbox.SetLineColor(0)
        textbox.SetLineStyle(1)
        textbox.SetLineWidth(0)
        textbox.SetFillColor(0)
        textbox.SetFillStyle(1001)

        chi2 = (
            "#chi^{2} / NDF = "
            + str(round(fit_function.GetChisquare(),2))
            + " / "
            + str(fit_function.GetNDF())
            )
        textbox.AddText(chi2)

        text = []
        for i, tmplt in enumerate(templates):
            integral = tmplt.histo.Integral()
            text.append(
                "N_{"
                + tmplt.legend
                + "} = %d #pm %d"%(
                        integral,
                        fit_function.GetParError(i) * integral / fit_function.GetParameter(i)
                    )
                )
        for txt in reversed(text):
            textbox.AddText(txt)
        #str(round(fit_function.GetParameter(i),3))#str(round(fit_function.GetParError(i),3))
        return textbox

    def set_up_stacking(self):

        def cosmetica(wrps):
            colors = {self.name_real:409, self.name_fake:625}
            for w in wrps:
                name = settings.get_pretty_name(w.analyzer)
                w.histo.SetTitle(name)
                w.legend = name
                w.histo.SetFillColor(colors[w.analyzer])
                w.histo.SetFillStyle(1001)
                yield w

        data_lumi = settings.data_lumi_sum_wrp()
        mc_tmplts = list(gen.fs_mc_stack({
            "analyzer"  : (self.name_real,self.name_fake),
            "name"      : self.name_histo
        }))
        data_tmplts = gen.fs_filter_sort_load({
            "analyzer"  : self.name_data,
            "name"      : self.name_histo
        })

        # save template stack right away
        tmpl_decs = self.canvas_decorators[:]
        tmpl_decs.remove(BottomPlotRatio)
        tmpl_cnvs = gen.canvas(mc_tmplts, tmpl_decs)
        tmpl_cnvs = gen.save(
            tmpl_cnvs, 
            lambda w: self.plot_output_dir + w.name
        )
        self.message(
            "INFO Saved " 
            + str(gen.consume_n_count(
                tmpl_cnvs
            )) + "template stack canvases." 
        )

        # combine mc stack to single histograms
        mc_tmplts = list(cosmetica(gen.gen_prod(itertools.izip(
            (wrp.HistoWrapper(w.histo, **w.all_info()) for w in mc_tmplts),
            itertools.repeat(data_lumi)
        ))))
 
        # do fit procedure
        fitted = gen.op.sum(data_tmplts)
        self.find_x_range(fitted.histo)
        fit_func = self.build_fit_function(mc_tmplts)
        fitted.histo.Fit(fit_func, "WL M N", "", self.x_min, self.x_max)
        self.save_fit_results(fit_func, mc_tmplts)
        self.scale_templates_to_fit(fit_func, mc_tmplts)

        #TODO: Make DECORATORS INSTANCEABLE BEFORE APPLYING
        #TODO: self.first_drawed.GetXaxis().SetNoExponent()
        textboxes = {
            mc_tmplts[0].name:
                self.make_fit_textbox(fit_func, mc_tmplts)
        }
        class TextBoxDecorator(dec.Decorator):
            textbox_dict = textboxes
            def do_final_cosmetics(self):
                self.decoratee.do_final_cosmetics()
                textbox = self.textbox_dict[self.renderers[0].name]
                textbox.Draw()
        self.canvas_decorators.append(TextBoxDecorator)

        tmplt_stacks = [gen.op.stack(mc_tmplts)]
        stream_stack = [(tmplt_stacks[0], fitted)]
        self.stream_stack = gen.pool_store_items(stream_stack)


class TemplateFitToolSihih(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolSihih, self).__init__(name)
        self.name_real  = "realTemplateSihih"
        self.name_fake  = "fakeTemplateSihih"
        self.name_data  = "dataTemplateFitHistoSihih"
        self.name_histo = "sihihEB"


class TemplateFitToolChHadIso(TemplateFitTool):
    def __init__(self, name = None):
        super(TemplateFitToolChHadIso, self).__init__(name)
        self.name_real  = "realTemplateChHadIso"
        self.name_fake  = "fakeTemplateChHadIso"
        self.name_data  = "dataTemplateFitHistoChHadIso"
        self.name_histo = "ChHadIso"
