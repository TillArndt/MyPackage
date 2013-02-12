
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postprocessing as pstprc
import cmstoolsac3b.generators as gen
import cmstoolsac3b.rendering as rnd
import re

class CrtlFiltTool(pstprc.PostProcTool):
    def run(self):

        stream_stack = gen.fs_mc_stack(
            {"analyzer":re.compile("CrtlFilt*")}
        )

        stream_stack = gen.pool_store_items(stream_stack)

        stream_canvas = gen.canvas(
            stream_stack,
            #[rendering.Legend]
        )

        stream_canvas = gen.save(
            stream_canvas,
            lambda wrp: self.plot_output_dir + wrp.name,
            settings.rootfile_postfixes
        )

        count = gen.consume_n_count(stream_canvas)
        self.message("INFO: "+self.name+" produced "+str(count)+" canvases.")



