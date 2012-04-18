__author__ = 'Heiner Tholen'

from UserCode.RWTH3b.cmsRunController.classes.CRPostProcessor import CRSimpleHistoTool

class myTTGammaAnalysisTool(CRSimpleHistoTool):

    def work(self, histo):


        print histo.GetName()
