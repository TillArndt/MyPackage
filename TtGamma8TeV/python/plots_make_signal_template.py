
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postprocessing as ppc
import cmstoolsac3b.postproctools as ppt
import plots_commons as com
import re

################################################# simply plot stacks
class DataMCSigTemplate(ppt.FSStackPlotter):
    def set_up_stacking(self):
        super(DataMCSigTemplate, self).set_up_stacking()

        # save bare histograms
        def save_histos(wrps):
            for wrp in wrps:
                w = wrp[0]
                name = settings.dir_result + w.analyzer
                w.write_root_file(name + ".root")
                w.write_info_file(name + ".info")
                yield wrp
        self.stream_stack = save_histos(self.stream_stack)

plotter = DataMCSigTemplate()
plotter.filter_dict = {
    "analyzer" : (
        re.compile("photonSigTemplate"),
    ),
    "name"     : "histo",
}
plotter.canvas_decorators.append(com.LumiTitleBox)

# reminder: the plotter leaves the histos in the pool

SigTemplateChain = ppc.PostProcChain(
    "SigTemplateChain",
    [
        plotter,
    ]
)