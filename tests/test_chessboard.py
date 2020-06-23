import unittest
import chessboard


class TestChessboard(unittest.TestCase):
    def setUp(self):
        self.chessboard = chessboard.Chessboard()

    def test_getset_pos(self):
        pos = (1, 1)
        self.chessboard.set_pos(pos)
        target = [[0, 0, 0], [0, 2, 0], [0, 0, 0]]
        self.assertEqual(self.chessboard.pos, target)
        self.assertEqual(self.chessboard[pos], 2)

    #@unittest.skip('')
    def test_validate_pos(self):
        self.chessboard.set_pos((1, 1))
        invalid_pos = [
            (1, 1),
        ]

        for p in invalid_pos:
            self.assertRaises(chessboard.PositionError, self.chessboard.validate_pos, p)
        valid_pos = [
            (2, 2),
        ]
        for p in valid_pos:
            self.assertTrue(self.chessboard.validate_pos(p))

        #self.assertRaises(ValueError, self.chessboard.validate_pos, (1.0, 2.0))

    def test_process_ipt(self):
        invalid_ipt = [
            '1, -1',
            '-1, 2',
            '1',
            'hi',
            'c,d',
            '1,d',
#            '200, 200',
            '0, 0',
            '0, 1',
            '1, 0',
            '1.1, 1.2',
            '1 1, 2 3',
        ]
        for i in invalid_ipt:
            self.assertRaises(ValueError, self.chessboard.process_ipt, i)

        outofrange_ipt = [
            '4, 4',
            '200, 1',
        ]
        for i in outofrange_ipt:
            self.assertRaises(ValueError, self.chessboard.process_ipt, i)

        valid_ipt = {
            '1, 1': (0, 0),
            '1, 2': (0, 1),
            '3, 3': (2, 2),
        }

        for k, v in valid_ipt.items():
            self.assertEqual(self.chessboard.process_ipt(k), v)
    
    def test_checkwinbystep(self):
        self.chessboard.clear()

    def test_state(self):
        self.chessboard.clear()
        self.chessboard.set_pos((1, 1))
        self.chessboard.set_pos((2, 2))
        self.chessboard.set_pos((0, 0))
        target = [2, 0, 0, 0, 2, 0, 0, 0, 2]
        self.assertEqual(self.chessboard.state, target)

    def test_action(self):
        self.chessboard.clear()
        self.chessboard.set_pos((1, 1))
        target = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)] 
        self.assertCountEqual(self.chessboard.available_actions, target)
        self.assertCountEqual(self.chessboard.positions(self.chessboard.pos), target)
        self.chessboard.set_pos((2, 2))
        target = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)] 
        self.assertCountEqual(self.chessboard.available_actions, target)
        self.assertCountEqual(self.chessboard.positions(self.chessboard.pos), target)
        self.chessboard.set_pos((0, 0))
        target = [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)] 
        self.assertCountEqual(self.chessboard.available_actions, target)
        self.assertCountEqual(self.chessboard.positions(self.chessboard.pos), target)
        self.chessboard.clear()
        target = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)] 
        self.assertCountEqual(self.chessboard.available_actions, target)
        self.assertCountEqual(self.chessboard.positions(self.chessboard.pos), target)

    def test_state2board(self):
        state = [1, 0, 0, 0, 2, 0, 0, 0, 2]
        board = [[1, 0, 0], [0, 2, 0], [0, 0, 2]]
        self.assertEqual(self.chessboard.state2board(state), board)
        state = [1, 2, 0, 1, 2, 0, 1, 1, 2, 2, 1, 1, 1, 0, 0, 0]
        board = [[1, 2, 0, 1], [2, 0, 1, 1], [2, 2, 1, 1], [1, 0, 0, 0]]
        self.assertEqual(self.chessboard.state2board(state), board)

