import unittest

from PyQt4 import QtCore
from MyPackage.TtGammaAnalysis.CmsRunCutflowParser import CmsRunCutflowParser

class MyTest(unittest.TestCase):

    def test_read_trigger_report(self):
        parser = CmsRunCutflowParser(QtCore.QSettings("test.ini",1))
        parser.read_trigger_report("ttgamma_whizard")
        self.assertEqual(parser.trigger_report[5], 'TrigReport     1    1       2601        696       1905          0 p2\n')


    def test_parse_cutflow_Given(self):
        qset = QtCore.QSettings("outputLogs/photonSelection.ini", 1)
        qset.setValue("parserMode", "Given")
        qset.setValue("ttgamma_whizard/p/photonsFromElsewhere/Passed",233)
        parser = CmsRunCutflowParser(qset)
        parser.parse_cutflow("ttgamma_whizard")
        self.assertTrue(qset.allKeys().contains(
            "ttgamma_whizard/p/photonsFromElsewhere/Passed")
        )
        self.assertEqual(qset.value("ttgamma_whizard/p/photonsFromElsewhere/Passed").toInt(), (235, True))
        self.assertFalse(qset.contains("ttgamma_whizard/p2/myLargePtPhotons/Passed"))


    def test_parse_cutflow_All(self):
        qset = QtCore.QSettings("outputLogs/photonSelection2.ini", 1)
        qset.setValue("parserMode", "All")
        parser = CmsRunCutflowParser(qset)
        parser.parse_cutflow("ttgamma_whizard")
        self.assertTrue(qset.allKeys().contains(
            "ttgamma_whizard/p/photonsFromElsewhere/Passed")
        )
        self.assertEqual(qset.value("ttgamma_whizard/p/photonsFromElsewhere/Passed").toInt(), (235, True))
        

def main():
    
    testSuite = unittest.TestSuite()
    testSuite.addTests(unittest.makeSuite(MyTest))

    import doctest
    import  MyPackage.TtGammaAnalysis.CmsRunCutflowParser as crp
    testSuite.addTest(doctest.DocTestSuite(crp))

    unittest.TextTestRunner(verbosity = 2).run(testSuite)


if __name__ == '__main__':
    main()

