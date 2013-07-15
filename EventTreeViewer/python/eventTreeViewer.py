

from PyQt4 import QtGui
from DataFormats.FWLite import Events,Handle
a = QtGui.QApplication([])


class EventTreeViewer(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        super(EventTreeViewer, self).__init__(parent)
        self.setColumnCount(1)
        self.setHeaderLabels(["pdg", "status", "e", "px", "py", "pz"])
        self.insertTopLevelItems(0, [QtGui.QTreeWidgetItem()])
        self.collection = "genParticles"

    def setEventTree(self, event):
        handle = Handle("vector<reco::GenParticle>")
        event.getByLabel(self.collection, handle)
        items = []
        def fill_tree(gen_particle, parent_item):
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
                items.append(item)
                fill_tree(p, item)
        for gp in iter(handle.product()):
            if not gp.mother():
                fill_tree(gp, None)
        self.clear()
        self.insertTopLevelItems(0,items)


def event_iterator(filename, handles = None):
    """handles is a list of tuples: (varname, type, InputTag)"""
    events = Events(filename)
    if not handles: handles = []
    for evt in events.__iter__():
        for name,typ,inputtag in handles:
            handle = Handle(typ)
            evt.getByLabel(inputtag,handle)
            setattr(evt, "hndl_" + name, handle)
        yield evt


def open_viewer(filename, collection_name= None):
    evtit = event_iterator(filename)
    w = EventTreeViewer()
    if collection_name: w.collection = collection_name
    w.setEventTree(evtit.next())
    w.show()
    def skipper():
        w.setEventTree(evtit.next())
    return skipper


fname_hein_nlo = "/disk1/tholen/eventFiles/fromGrid20130618/TTNLO_000.root"
fname_hein_mg  = "/disk1/tholen/eventFiles/fromGrid20130618/TTJets_000.root"