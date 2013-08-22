

from PyQt4 import QtGui
from DataFormats.FWLite import Events,Handle
a = QtGui.QApplication([])


class EventTreeViewer(QtGui.QTreeWidget):
    def __init__(self, parent=None):
        super(EventTreeViewer, self).__init__(parent)
        self.setColumnCount(1)
        self.setHeaderLabels(["pdg", "status", "e", "px", "py", "pz"])
        self.insertTopLevelItems(0, [QtGui.QTreeWidgetItem()])
        self.collection = "genParticles"

    def setEventTree(self, event, expand_key_func=None):
        self.clear()
        handle = Handle("vector<reco::GenParticle>")
        event.getByLabel(self.collection, handle)
        def fill_tree(gen_particle, parent_item):
            expanded = False
            for p in xrange(gen_particle.numberOfDaughters()):
                p = gen_particle.daughter(p)
                item = QtGui.QTreeWidgetItem(
                    parent_item,
                    [
                        "%d" % p.pdgId(),
                        "%d" % p.status(),
                        "%f" % p.energy(),
                        "%f" % p.px(),
                        "%f" % p.py(),
                        "%f" % p.pz(),
                    ]
                )
                if not parent_item:
                    self.addTopLevelItem(item)
                if expand_key_func and expand_key_func(p):
                    expanded = True
                expanded = fill_tree(p, item) or expanded
            if parent_item and expanded:
                parent_item.setExpanded(True)
            return expanded

        for gp in iter(handle.product()):
            if not gp.mother():
                fill_tree(gp, None)


def event_iterator(filename, handles=None):
    """handles is a list of tuples: (varname, type, InputTag)"""
    events = Events(filename)
    if not handles: handles = []
    for evt in events.__iter__():
        for name,typ,inputtag in handles:
            handle = Handle(typ)
            evt.getByLabel(inputtag, handle)
            setattr(evt, "hndl_" + name, handle)
        yield evt


def open_viewer(filename, expand_key_func=None, collection_name=None):
    evtit = event_iterator(filename)
    w = EventTreeViewer()
    if collection_name: w.collection = collection_name
    def skipper():
        w.setEventTree(evtit.next(), expand_key_func)
    skipper()
    w.show()
    return skipper


fname_hein_whiz = "/disk1/tholen/eventFiles/backup/whiz_000.root"
fname_hein_nlo  = "/disk1/tholen/eventFiles/fromGrid20130618/TTNLO_000.root"
fname_hein_mg   = "/disk1/tholen/eventFiles/fromGrid20130618/TTJets_000.root"

def expand_photons_25(particle):
    return particle.pdgId() == 22 and particle.et() > 25.