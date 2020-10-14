import unittest
import tests

suite = unittest.TestSuite()
suite.addTest(tests.TestChessboard("test_process_ipt"))
runner = unittest.TextTestRunner()
runner.run(suite)
