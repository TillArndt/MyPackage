__author__ = 'Heiner Tholen'

import unittest
import doctest
import MyPackage.TtGammaAnalysis.CmsRunHistoStacker as crhs
from MyPackage.TtGammaAnalysis.CmsRunHistoStacker import CmsRunHistoStacker


class MyTest(unittest.TestCase):
    pass


def main():
    """
    Run the tests.
    """

    testSuite = unittest.TestSuite()
    testSuite.addTest(doctest.DocTestSuite(crhs))

    unittest.TextTestRunner(verbosity = 2).run(testSuite)


if __name__ == "__main__":
    main()

