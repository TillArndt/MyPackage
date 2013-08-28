
import cmstoolsac3b.settings as settings
import cmstoolsac3b.postprocessing as pp

class CounterReader(pp.PostProcTool):
    """Reads event count from sample logs."""
    has_output_dir = False
    can_reuse = False

    def run(self):
        samples = settings.samples.keys()
        search_string = "EventCountPrinter:"
        for p in settings.cmsRun_procs:
            if not p.name in samples:
                continue
            if not p.successful():
                continue
            sample = settings.samples[p.name]
            sample.log_event_counts = {}
            with open(p.log_filename) as f:
                for line in f:
                    if search_string in line:
                        tokens = line.split()
                        count = float(tokens[-1])
                        label = tokens[tokens.index("label") + 2]
                        sample.log_event_counts[label] = count


class TopPtWeightNorm(pp.PostProcTool):
    """Average top pt weight is not zero. This tool fixes sample norm."""
    has_output_dir = False
    can_reuse = False

    def run(self):
        token = "AverageTopPtWeight,"
        finished_procs = list(
            p
                for p in settings.cmsRun_procs
                if p.successful()
        )
        for p in finished_procs:
            av_weight = p.sample.log_event_counts.get(token)
            if av_weight:
                p.sample.n_events   *= av_weight
                p.sample.lumi       *= av_weight


class SampleEventCount(pp.PostProcTool):
    """Sets number of input events on samples."""

    def __init__(self, name = None):
        super(SampleEventCount, self).__init__(name)
        if not hasattr(self, "counter_token"):
            self.counter_token = "EventCountPrinter:"

    def run(self):
        finished_procs = list(
            p
            for p in settings.cmsRun_procs
            if p.successful()
        )
        for p in finished_procs:
            if p.sample.is_data:
                continue
            if p.sample.n_events is not -1:
                continue
            with open(p.log_filename) as f:
                for line in f:
                    if self.counter_token in line:
                        n_events = int(line.split()[-1])
                        p.sample.n_events = n_events
                        p.sample.lumi = n_events / p.sample.x_sec
                        self.message(
                            "INFO: Setting number of events for "
                            + p.name + " to " + str(n_events)
                        )
                        break

