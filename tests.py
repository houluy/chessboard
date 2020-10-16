import unittest
import tests

suite = unittest.TestSuite()
suite.addTest(tests.TestChessboard("test_columns"))
runner = unittest.TextTestRunner()
runner.run(suite)
