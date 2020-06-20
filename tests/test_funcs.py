import unittest
import math

import chessboard

angle = [45, 90, 180, 360]
radian = [math.pi/4, math.pi/2, math.pi, 2*math.pi]


class Test_AngleRadian(unittest.TestCase):
    def test_angle2radian(self):
        for ind, a in enumerate(angle):
            self.assertEqual(chessboard.radian_angle(angle=a), radian[ind])

    def test_radian2angle(self):
        for ind, a in enumerate(radian):
            self.assertAlmostEqual(chessboard.radian_angle(radian=a), angle[ind])



if __name__ == "__main__":
    unittest.main()
