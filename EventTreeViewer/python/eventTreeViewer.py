








from PyQt4 import QtGui

class EventTreeViewer(QtGui.QTreeWidget):
    def __init__(self, parent = None):
        super(EventTreeViewer, self).__init__(parent)
        self.setColumnCount(1)
        self.setHeaderLabels(["hallo"])











def nothing():
    from DataFormats.FWLite import Events,Handle
    events = Events("/disk1/tholen/eventFiles/fromGrid20130601/TTJetsNLO_1.root")
    evtIter = events.__iter__()
    event = evtIter.next()
    genPartH = Handle("vector<reco::GenParticle>")
    event.getByLabel("genParticles",genPartH)
    genParts=genPartH.product()



##include "eventtreeviewer.h"
##include <QtCore/QFile>
##include <QtCore/QTextStream>
##include <QDebug>
#EventTreeViewer::EventTreeViewer(QTreeWidget *parent)
#: QTreeWidget(parent)
#{
#
#    this->setColumnCount(1);
#this->setHeaderLabels(QStringList(QString("hallo")));
#QList<QTreeWidgetItem *> items;
#QVector<QTreeWidgetItem *> itemsAtLevel(500,NULL);
#
#QFile inputFile(":/PrintTreeOutput.log");
#inputFile.open(QIODevice::ReadOnly);
#
#QTextStream in(&inputFile);
#
#while( !in.readLine().contains("decay tree")){}
#
#QTreeWidgetItem *itam = new QTreeWidgetItem((QTreeWidget*)0, QStringList(QString( in.readLine() )));
#itemsAtLevel[0]=itam;
#items.append(itam);
#
#while(true){
#    QString line=in.readLine();
#if(!line.contains("+"))break;
#int index=line.indexOf("+");
#int level=index/4+1;
#QTreeWidgetItem *itam2 = new QTreeWidgetItem(itemsAtLevel[level-1] , QStringList(QString( line.remove(0,level*4) )));
#itemsAtLevel[level]=itam2;
#items.append(itam2);
#}
#
#
#this->insertTopLevelItems(0, items);
#
#
#}
