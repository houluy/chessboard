# Chessboard Class
import copy
import math
import sys
import string 
from itertools import combinations_with_replacement as comb
from colorline import cprint

ASC_ONE = ord('1')
ASC_NINE = ord('9')
ASC_A = ord('A')
ASC_Z = ord('Z')
ASC_a = ord('a')
ASC_z = ord('z')
MAX_NUM = 9
MAX_CAP = MAX_NUM + 26
MAX_LOW = MAX_CAP + 26
DIR_NUM = 4
FULL_DIR_NUM = 8
sign = lambda a: (a > 10**(-10)) - (a < -10**(-10))

class PositionError(Exception):
    pass

class Chessboard:
    def __init__(self, board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', user_number=2, game_name=None, pos=None, nested=False):
        self.seq  = 1 #1 means offensive pos, while 2 means defensive pos 
        self.character = {1:ch_off, 2:ch_def, 0:ch_blank}
        self._pos_dict = {}
        self._user_pos_dict = {x:[] for x in range(1, user_number + 1)}
        self.graph = []
        self.board_size = board_size
        self.win = win
        self.game_name = game_name
        if self.game_name:
            if game_name == 'Gomoku':
                self.board_size = 15
                self.win = 5
            elif game_name == 'tictactoe':
                self.board_size = 3
                self.win = 3
            elif game_name == 'fourinarow':
                self.board_size = 7
                self.win = 4
            elif game_name == 'normal':
                self.board_size = int(input('Board size: '))
                self.win = int(input('Winning chess number: '))
            else:
                raise ValueError('Unsupported game, please refer to docs!')
        elif pos:
            self.win = win
            if isinstance(pos, str):
                self.board_size = int(math.sqrt(len(pos)))
            else:
                if isinstance(pos[0], list):
                    self.board_size = len(pos)
                else:
                    self.board_size = int(math.sqrt(len(pos)))

        if self.board_size > MAX_LOW:
            raise ValueError('Board size has reached its limit ({})!'.format(MAX_LOW))
        if self.win > self.board_size:
            raise ValueError('Winning number exceeds the board size!')
        self.pos_range = range(self.board_size)
        self.pos = [[0 for _ in self.pos_range] for _ in self.pos_range]
        if pos:
            if isinstance(pos, str):
                pos = self.str2state(pos)
            if nested:
                self.pos = copy.deepcopy(pos)
            else:
                for ind, val in enumerate(pos):
                    i, j = self.compute_coordinate(ind)
                    self.pos[i][j] = val

        self.count_round()
        self.user_number = user_number
        self.chess_number = [0 for x in range(self.user_number)]
        
        self.check = {}
        self.history = {}
        self.angle = [_*math.pi/4 for _ in range(DIR_NUM)]
        self.full_angle = [_*math.pi/4 for _ in range(FULL_DIR_NUM)]
        
    def __str__(self):
        return ''.join([''.join([str(x) for x in y]) for y in self.pos])

    def __repr__(self):
        return ''.join([''.join([str(x) for x in y]) for y in self.pos])

    def str2state(self, pos_str):
        return [int(x) for x in pos_str]

    def get_column(self, column):
        return [_[column] for _ in self.pos]

    def _cal_key(self, pos):
        return str(pos[0]) + str(pos[1])

    @property
    def pos_dict(self):
        return self._pos_dict

    @property
    def user_pos_dict(self):
        return self._user_pos_dict

    def get_chess(self, pos):
        return self.pos[pos[0]][pos[1]]

    def within_range(self, pos):
        if 0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size:
            return True
        else:
            return False

    def skip_round(self, times=1):
        game_round = self._game_round
        for i in range(times):
            self.history[self._game_round + i] = copy.deepcopy(self.pos)
        self._game_round += times

    def get_close_chess(self, current, angle, step=1):
        return (int(current[0] + step*sign(math.cos(angle))), int(current[1] - step*sign(math.sin(angle))))

    def get_all_pos(self, user):
        pos_list = []
        for x, i in enumerate(self.pos):
            for y, j in enumerate(i):
                if j == user:
                    pos_list.append((x, y))
        return pos_list

    def compute_coordinate(self, index):
        '''Compute two-dimension coordinate from one-dimension list'''
        j = index%self.board_size
        i = (index - j) // self.board_size
        return (i, j)

    def count_round(self):
        self._game_round = 1
        for ind_i, val_i in enumerate(self.pos):
            for ind_j, val_j in enumerate(val_i):
                if val_j != 0:
                    self._game_round += 1

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
    
    def print_pos(self, coordinates=None, pos=None):
        '''Print the chessboard'''
        if not pos:
            pos = self.pos
        self.graph = [list(map(self._transform, pos[i])) for i in self.pos_range]
        xaxis = ' '.join([chr(ASC_ONE + _) for _ in range(min(self.board_size, MAX_NUM))])
        if (self.board_size > MAX_NUM):
            xaxis += ' '
            xaxis += ' '.join([chr(ASC_A + _ - MAX_NUM) for _ in range(MAX_NUM, min(self.board_size, MAX_CAP))])
        if (self.board_size > MAX_CAP):
            xaxis += ' '
            xaxis += ' '.join([chr(ASC_a + _ - MAX_CAP) for _ in range(MAX_CAP, self.board_size)])
        print('  ', end='')
        print(xaxis)
        for i in range(self.board_size):
            out = '|'.join(self.graph[i])
            if i < MAX_NUM:
                print(chr(i + ASC_ONE), end='')
            elif MAX_NUM <= i < MAX_CAP:
                print(chr(i - MAX_NUM + ASC_A), end='')
            elif MAX_CAP <= i < MAX_LOW:
                print(chr(i - MAX_CAP + ASC_a), end='')
            print('|', end='')
            #Colorful print
            if coordinates:
                for j in range(self.board_size):
                    if (i, j) in coordinates:
                        new_print = cprint
                        params = {
                            'color': 'w',
                            'bcolor': 'r',
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
        #to_cap = ch - ASC_ONE + 1
        if ASC_ONE <= ch <= ASC_NINE:
            return ch - ASC_ONE
        elif ASC_A <= ch <= ASC_Z:
            return ch - ASC_A + MAX_NUM
        elif ASC_a <= ch <= ASC_z:
            return ch - ASC_a + MAX_CAP
        else:
            return ch

    def get_player(self):
        return 2 - self._game_round % 2

    def get_player_str(self):
        return self.character.get(self.get_player())

    def another_player(self, player=None):
        if not player:
            player = self.get_player()
        return 2 - (1 + player) % 2

    def another_player_str(self, player=None):
        return self.character.get(self.another_player(player))
    
    def set_pos(self, pos, check=False):
        '''Set a chess'''
        self.validate_pos(pos)
        x, y = pos
        user = self.get_player()
        self.history[self._game_round] = copy.deepcopy(self.pos)
        self.pos[x][y] = user
        pos_str = self._cal_key(pos)
        self._pos_dict[pos_str] = user
        self._user_pos_dict[user].append(pos)
        self._game_round += 1
        if check:
            winning = self.check_win_by_step(x, y, user)
            return winning
        else:
            return (x, y)

    def get_win_list(self):
        return self.win_list

    def _transform(self, val):
        return self.character.get(val)

    def clear(self):
        '''Clear a chessboard'''
        self.pos = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.graph = copy.deepcopy(self.pos)
        self._game_round = 1

    def check_win(self):
        '''Check the eight direction of (x, y) for a line
        Eight direction
        1 2 3
        4 X 5
        6 7 8
        Border: 0 ~ self.board_size-1
        '''
        pass

    def validate_input(self, input_str, val_pos=True):
        input_str = input_str.replace(' ', '')
        pos_str = input_str.split(',')
        pos_xy = []
        if pos_str[0] == 'u':
            try:
                times = int(pos_str[1])
            except Exception as e:
                raise ValueError('Error command, undo command: u, {times}')
            else:
                return ('u', times)
        for pos in pos_str:
            if len(pos) != 1:
                raise ValueError('Error position, form: x, y, one character at most')
            pos_num = self.asc2pos(pos)
            pos_xy.append(pos_num)

        if self.game_name == 'fourinarow':
            y = pos_xy[0]
            x = 0
        else:
            if len(pos_xy) != 2:
                raise ValueError('Error position, must have both x and y coordinates')
            x, y = pos_xy
        if val_pos:
            self.validate_pos((x, y))
        if self.game_name == 'fourinarow':
            x = self.get_not_num(self.get_column(y)) - 1
            if x not in self.pos_range:
                raise PositionError('This column is full')
        return (x, y)

    def validate_pos(self, pos):
        x, y = pos
        for p in pos:
            if p not in self.pos_range:
                raise PositionError('Position value is out of board\'s range')
        if self.pos[x][y] != 0:
            raise PositionError('There is a chess piece on that position')

    def handle_input(self, input_str, place=True, check=False):
        '''Transfer user input to valid chess position'''
        user = self.get_player()
        pos = self.validate_input(input_str)
        if pos[0] == 'u':
            self.undo(pos[1])
            return pos
        if place:
            result = self.set_pos(pos, check)
            return result
        else:
            return pos

    def distance(self, piecex, piecey):
        '''Return the distance of chess piece X and Y (Chebyshev Distance)'''
        return max(abs(piecex[0] - piecey[0]), abs(piecex[1], piecey[1]))

    def check_win_by_step(self, x, y, user, line_number=None):
        '''Check winners by current step'''
        if not line_number:
            line_number = self.win
        for ang in self.angle:
            self.win_list = [(x, y)]
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
                    if target_x < 0 or target_y < 0 or target_x > self.board_size - 1 or target_y > self.board_size - 1:
                        direction[ind] = 0
                    elif self.pos[target_x][target_y] == user:
                        self.win_list.append((target_x, target_y))
                        line_num += 1
                    else:
                        direction[ind] = 0
                else:
                    radius += 1
        else:
            return (x, y)

    def get_not_num(self, seq, num=0):
        '''Find the index of first non num element'''
        ind = next((i for i, x in enumerate(seq) if x != num), None)
        if ind == None:
            return self.board_size
        else:
            return ind

    def count_chess(self):
        result = [0 for x in range(self.user_number)]
        for i in self.pos:
            for j in i:
                result[j - 1] = result[j - 1] + 1 if j != 0 else result[j - 1]
        return result

class ChessboardExtension(Chessboard):
    '''Provide extended methods for Class Chessboard'''
    def __init__(self, board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', user_number=2, game_name=None, pos=None, nested=False):
        super().__init__(
            board_size=board_size,
            win=win,
            ch_off=ch_off,
            ch_def=ch_def,
            ch_blank=ch_blank,
            user_number=user_number,
            game_name=game_name,
            pos=pos,
            nested=nested)

    def compare_board(self, dst, src=None):
        '''Compare two chessboard'''
        if not src:
            src = self.pos

        if src == dst:
            return True
        else:
            #May return details
            return False

    def diff_state(self, obj, cur=None):
        if not cur:
            cur = self.tostate()
        assert len(obj) == len(cur)

        diff_pos = []
        for i, x in enumerate(cur):
            if str(x) != str(obj[i]):
                diff_pos.append(i)
        
        return diff_pos

    def coor_trans(self, two=None, one=None):
        if two is not None:
            return two[0]*self.board_size + two[1] - 1
        elif one is not None:
            y = one%self.board_size
            x = (one - y)//self.board_size + 1
            return (x, y) 
        else:
            raise ValueError('One kind of coordinates must be given')

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

    def get_action(self, pos=None):
        if not pos:
            pos = self.pos

        available_actions = []
        for i in self.pos_range:
            for j in self.pos_range:
                if pos[i][j] == 0:
                    available_actions.append((i, j))
        return available_actions

    def tostate(self, pos=None):
        if not pos:
            pos = self.pos
        return [y for x in pos for y in x]
