import FWCore.ParameterSet.Config as cms
from FWCore.GuiBrowsers.ConfigToolBase import *

import PhysicsTools.PatAlgos.tools.helpers as configtools

class RunSelectionTool(ConfigToolBase):

    _label='runSelectionTool'
    _defaultParameters=dicttypes.SortedKeysDict()

    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters, 'selectionFilters', "selectionFilters",
            "Input path as string", Type=str, acceptNoneValue=True)
        self.addParameter(self._defaultParameters, 'names', cms.vstring(),
            "Output vector of pathnames", Type=cms.vstring, acceptNoneValue=False)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""

    def getDefaultParameters(self):
        return self._defaultParameters

    def _createPathsForModules(self,process):
        selectionFiltersLabel=self._parameters['selectionFilters'].value
        print getattr( process, selectionFiltersLabel ).moduleNames()
        for module in getattr( process, selectionFiltersLabel ).moduleNames():
            ModulePathTmp=cms.Path(getattr(process,"preSel") * getattr(process,module))
            modulePathLabel="ModulePath"+module
            setattr(process,modulePathLabel, ModulePathTmp)
            self._parameters['names'].value.append(modulePathLabel)


    def __call__(self, process,
                 selectionFilters            = None,
                 names                    = None
    ):
        if selectionFilters is None:
            selectionFilters = self._defaultParameters['selectionFilters'].value
        if names is None:
            names = self._defaultParameters['names'].value


        self.setParameter('selectionFilters', selectionFilters)
        self.setParameter('names', names)

        self.apply(process)




    def toolCode(self, process):
        self._createPathsForModules(process)


runSelectionTool=RunSelectionTool()