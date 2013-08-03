
import cmstoolsac3b.postproctools as ppt
import cmstoolsac3b.rendering as rnd
import cmstoolsac3b.generators as gen

class MatchQualityStack(ppt.FSStackPlotter):

    def configure(self):
        self.canvas_decorators = [
            rnd.Legend
        ]
        self.filter_dict = {
            "analyzer":"matchQualitySihih",
        }

    def set_up_stacking(self):
        stream_stack = gen.fs_mc_stack(self.filter_dict)
        self.stream_stack = gen.pool_store_items(stream_stack)

