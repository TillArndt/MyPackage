__author__ = 'Heiner Tholen'

import unittest

from PyQt4 import QtCore
from MyPackage.TtGammaAnalysis.CmsRunCutflowParser import CmsRunCutflowParser
import MyPackage.TtGammaAnalysis.MyUtility as util

class MyTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(MyTest, self).__init__(methodName)
        util.DIR_LOGS = "res"


    def test_read_trigger_report(self):
        parser = CmsRunCutflowParser(QtCore.QSettings("res/tmp.ini",1))
        parser.read_trigger_report("ttgamma_whizard")
        self.assertEqual(parser.trigger_report[5], 'TrigReport     1    1       2601        696       1905          0 p2\n')


    def test_parse_cutflow(self):
        qset = QtCore.QSettings("res/photonSelection.ini", 1)
        qset.beginGroup("photonSelection")
        parser = CmsRunCutflowParser(qset)
        parser.parse_cutflow("ttgamma_whizard")
        self.assertTrue(qset.allKeys().contains(
            "ttgamma_whizard/cutflow/p/myBTagRequirement/Visited")
        )
        self.assertEqual(qset.value(
            "ttgamma_whizard/cutflow/p/photonsFromElsewhere/Passed"
        ).toInt(), (235, True))
        

def main():
    
    testSuite = unittest.TestSuite()
    testSuite.addTests(unittest.makeSuite(MyTest))

    import doctest
    import MyPackage.TtGammaAnalysis.CmsRunCutflowParser as crp
    testSuite.addTest(doctest.DocTestSuite(crp))

    unittest.TextTestRunner(verbosity = 2).run(testSuite)


if __name__ == '__main__':
    main()

