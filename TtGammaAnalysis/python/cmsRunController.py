
from PyQt4 import QtCore
from MyPackage.TtGammaAnalysis.cmsRunProcess import cmsRunProcess
import MyPackage.TtGammaAnalysis.myUtility as util


class cmsRunController(QtCore.QObject):
    def __init__(self, qsetting):
        super(cmsRunController, self).__init__()
        self.qsetting = qsetting
        self.waitingPros = []
        self.runningPros = []
        self.finishedPros = []
        self.failedPros = []
        self.setUpProcesses()


    #signal emited when lists are changed
    processListsUpdated = QtCore.pyqtSignal()


    def setUpProcesses(self):
        qset = self.qsetting

        #load all cfg file setups
        cfgFileAbbrevs = qset.childGroups()
        for cfgFile in cfgFileAbbrevs:
            if qset.value(cfgFile + "/enable").toBool():
                qset.beginGroup(cfgFile)

                #load all cmsRun starts
                cmsRunConfAbbrevs = qset.childGroups()
                for cmsRunConf in cmsRunConfAbbrevs:
                    if qset.value(cmsRunConf + "/enable").toBool():
                        process = cmsRunProcess(cmsRunConf)
                        process.prepareRunConf(qset)
                        self.waitingPros.append(process)
                qset.endGroup()
                self.waitingPros.append("cfgFileEnd") #mark cfg file end
        self.processListsUpdated.emit()


    def startProcesses(self):
        
        #check if launch is possible
        if (len(self.waitingPros) == 0 or len(self.runningPros)
                  >= self.qsettings.value("maxProcesses",2).toInt()):
            return
            
        #block until cfg file is fully done
        if self.waitingPros[0] == "cfgFileEnd":
            if len(self.runningPros) > 0:
                return
            else:
                self.waitingPros.pop(0)

        #now start processing
        process = self.waitingPros.pop(0)
        process.finished.connect(self.finishProcess)
        process.start()
        self.runningPros.append(process)
        self.processListsUpdated.emit()

        #recursively
        self.startProcesses()

    def finishProcesses(self):

        #remove finished processes from self.runningPros
        for process in self.runningPros[:]:
            if process.state() == 0:
                self.runningPros.remove(process)
                if process.exitCode() == 0:
                    self.finishedPros.append(process)
                else:
                    self.failedPros.append(process)
                    
        self.processListsUpdated.emit()

        #see if there is new processes to start
        self.startProcesses()
 
