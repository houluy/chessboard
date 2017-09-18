# Chessboard Class
import copy
import math
import sys
from itertools import combinations_with_replacement as comb
from colorline import cprint

ASC_ONE = ord('1')
ASC_A = ord('A')
MAX_NUM = 9
DIR_NUM = 4
sign = lambda a: (a > 10**(-10)) - (a < -10**(-10))

class PositionError(Exception):
    pass

class Chessboard:
    def __init__(self, board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', user_number=2, game_name=None):
        #self.step = 0 #Game step
        self.seq  = 1 #1 means offensive pos, while 2 means defensive pos 
        self.character = {1:ch_off, 2:ch_def, 0:ch_blank}
        self.seq_dict = {}
        self.graph = []
        if game_name == 'Gomoku':
            self.board_size = 15
            self.win = 5
            self.user_number = 2
        elif game_name == 'tictactoe':
            self.board_size = 3
            self.win = 3
            self.user_number = 2
        elif game_name == 'fourinarow':
            self.board_size = 7
            self.win = 4
            self.user_number = 2
        else:
            self.board_size = board_size
            self.win = win
            self.user_number = user_number
        self.pos_range = range(self.board_size)
        self.pos = [[0 for _ in self.pos_range] for _ in self.pos_range]
        self.check = {}
        self._game_round = 1
        self.history = {}
        self.angle = [_*math.pi/4 for _ in range(DIR_NUM)]
        self.asc_range = list(range(ASC_ONE, ASC_ONE + min(MAX_NUM, self.board_size)))
        if self.board_size > MAX_NUM:
            self.asc_range += list(range(ASC_A, ASC_A + self.board_size - MAX_NUM))

    @property
    def game_round(self):
        return self._game_round

    @game_round.setter
    def game_round(self, game_round):
        self._game_round = game_round

    def get_board(self):
        return self.pos

    def undo(self, times=1):
        if times >= self._game_round:
            raise ValueError('Too many undos!')
        else:
            self._game_round = self._game_round - times
            self.pos = self.history[self._game_round]

    def rotate_board(self, angle, unit='radian'):
        '''Rotate the chessboard for a specific angle,
        angle must be integral multiple of pi/2(90 degree)'''
        if unit == 'angle':
            angle = angle*math.pi/180

        angle %= 2*math.pi
        if angle not in [0, math.pi/2, math.pi, math.pi*3/2]:
            raise ValueError('Angle must be integral multiple of pi/2(90 degree)')

        new_pos = [[0 for _ in self.pos_range] for _ in self.pos_range]
        cos_ang = math.cos(angle)
        sin_ang = math.sin(angle)
        center = (self.board_size - 1)/2
        for x, y in comb(self.pos_range, 2):
            xt = int((x - center)*cos_ang - (y - center)*sin_ang + center)
            yt = int((x - center)*sin_ang + (y - center)*cos_ang + center)
            new_pos[xt][yt] = self.pos[x][y]
        return new_pos

    def print_pos(self, coordinates, pos=None):
        '''Print the chessboard'''
        if not pos:
            pos = self.pos
        print(coordinates)
        self.graph = [list(map(self._transform, pos[i])) for i in self.pos_range]
        xaxis = ' '.join([chr(ASC_ONE + _) for _ in range(min(self.board_size, MAX_NUM))])
        if (self.board_size > MAX_NUM):
            xaxis += ' '
            xaxis += ' '.join([chr(ASC_A + _ - MAX_NUM) for _ in range(MAX_NUM, self.board_size)])
        print('  ', end='')
        print(xaxis)
        for i in range(self.board_size):
            out = '|'.join(self.graph[i])
            if i < MAX_NUM:
                print(chr(i + ASC_ONE), end='')
            else:
                print(chr(i - MAX_NUM + ASC_A), end='')
            print('|', end='')
            #Colorful print
            if coordinates[0] == i:
                for j in range(self.board_size):
                    if j == coordinates[1]:
                        new_print = cprint
                        params = {
                            'color': 'r',
                            'bcolor': 'w',
                        }
                    else:
                        new_print = print
                        params = {}
                    new_print(self._transform(pos[i][j]), end='', **params)
                    print('|', end='') 
                else:
                    print()
            else:
                print(out, end='')
                print('|')

    def asc2pos(self, ch):
        if isinstance(ch, str):
            ch = ord(ch)
        return ch - ASC_ONE if ch - ASC_ONE + 1 <= MAX_NUM else MAX_NUM + ch - ASC_A

    def get_player(self):
        return 2 - self._game_round % 2
    
    def set_pos(self, x, y, user=None, check=False):
        '''Set a chess'''
        if isinstance(x, str):
            x, y = self.asc2pos(x), self.asc2pos(y)
        else:
            x -= 1
            y -= 1
        if not user:
            user = self.get_player()
        if x not in self.pos_range or y not in self.pos_range or user not in range(1, self.user_number + 1): 
            raise ValueError('Position or user value is out of range')
        elif self.pos[x][y] != 0:
            raise PositionError('There is a chess piece on that position')
        else:
            self.history[self._game_round] = copy.deepcopy(self.pos)
            self.pos[x][y] = user
            if check:
                winning = self.check_win_by_step(x, y, user)
                if winning is True:
                    return winning
            self._game_round += 1
            return (x, y)

    def set_pos_on_board_special(self, board, x, y, user, user_number=2):
        '''Set a chess based on a specific chessboard'''
        if isinstance(x, str):
            x, y = self.asc2pos(x), self.asc2pos(y)
        else:
            x -= 1
            y -= 1
        board_size = len(board[0])
        if x not in range(board_size) or y not in range(board_size) or user not in range(1, user_number + 1): 
            raise ValueError('Position or user value is out of range')
        elif board[x][y] != 0:
            raise PositionError('There is a chess piece on that position')
        else:
            board[x][y] = user
            return board

    def _transform(self, val):
        return self.character.get(val)

    def clear(self):
        '''Clear a chessboard'''
        self.pos = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.graph = copy.deepcopy(self.pos)

    def check_win(self):
        '''Check the eight direction of (x, y) for a line
        Eight direction
        1 2 3
        4 X 5
        6 7 8
        Border: 0 ~ self.board_size-1
        '''
        pass

    def handle_input(self, input_str, user=None, check=False):
        '''Transfer user input to valid chess position'''
        input_str = input_str.replace(' ', '')
        pos_str = input_str.split(',')
        if not user:
            user = self.get_player()
        if (len(pos_str) != 2):
            raise PositionError('Error number of coordinates or commands!')
        if pos_str[0] == 'u':
            try:
                self.undo(int(pos_str[1]))
            except ValueError as e:
                raise e
            else:
                return None
        x, y = pos_str
        try:
            result = self.set_pos(x, y, user, check)
        except (ValueError, PositionError) as e:
            raise e
        else:
            return result

    def distance(self, piecex, piecey):
        '''Return the distance of chess piece X and Y (Chebyshev Distance)'''
        return max(abs(piecex[0] - piecey[0]), abs(piecex[1], piecey[1]))

    def check_win_by_step(self, x, y, user, line_number=None):
        '''Check winners by current step'''
        if not line_number:
            line_number = self.win
        for ang in self.angle:
            angs = [ang, ang + math.pi]
            line_num = 1
            radius = 1
            direction = [1, 1]
            while True:
                if line_num == line_number:
                    return True
                if direction == [0, 0]:
                    break
                for ind, a in enumerate(angs):
                    target_x = int(x + radius*(sign(math.cos(a)))) if direction[ind] else -1
                    target_y = int(y - radius*(sign(math.sin(a)))) if direction[ind] else -1
                    #print('angle: {}, cos: {}, sin: {}, radius: {}, line_num: {}, ind: {}, direction: {}, target_x: {}, target_y: {}'.format(a/math.pi, math.cos(a), math.sin(a), radius, line_num, ind, direction[ind], target_x + 1, target_y + 1))
                    if target_x < 0 or target_y < 0 or target_x > self.board_size - 1 or target_y > self.board_size - 1:
                        direction[ind] = 0
                    elif self.pos[target_x][target_y] == user:
                        line_num += 1
                    else:
                        direction[ind] = 0
                else:
                    radius += 1
        else:
            return (x, y)

class ChessboardExtension(Chessboard):
    '''Provide extended methods for Class Chessboard'''
    def __init__(self, board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', user_number=2, game_name=None):
        super().__init__(board_size=board_size, win=win, ch_off=ch_off, ch_def=ch_def, ch_blank=ch_blank, user_number=user_number, game_name=game_name)

    def compare_board(self, src_board, dst_board):
        '''Compare two chessboard'''
        if src_board == dst_board:
            return True
        else:
            #May return details
            return False

if __name__ == '__main__':
    cb = Chessboard(game_name='Gomoku')
    while True:
        pos = input('Input:')
        a = cb.handle_input(pos, check=True)
        if a is True:
            print('player {} wins'.format(cb.get_player()))
            sys.exit(0)
        cb.print_pos(coordinates=a)
