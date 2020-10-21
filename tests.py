import unittest
import tests

suite = unittest.TestSuite()
suite.addTest(tests.TestChessboard("test_columns"))
suite.addTest(tests.TestFourinarowChessboar("test_state"))
#suite.addTest(tests.TestFourinarowChessboar("test_getrowbycolumn"))
suite.addTest(tests.TestFourinarowChessboar("test_single_ipt"))
runner = unittest.TextTestRunner()
runner.run(suite)
