# Chessboard Class
import copy
import math
import sys
import string 
import re
from itertools import combinations_with_replacement as comb
from itertools import product
import logging

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


class BoardUnderlayer:
    def __init__(self, board_size=3):
        self.board_size = board_size


class PositionError(Exception):
    pass


def radian_angle(radian=None, angle=None):
    assert not (radian is None and angle is None)
    if radian is not None:
        return radian * 180 / math.pi
    elif angle is not None:
        return angle * math.pi / 180


class Chessboard:
    def __init__(self, board_size=3, ch_off='O', ch_def='X', ch_blank=' ', win=3):#, pos=None, nested=False):
        self.seq  = 1 #1 means offensive pos, while 2 means defensive pos 
        self.character = {1:ch_off, 2:ch_def, 0:ch_blank}
        #self.pos_dict = {}
        self.graph = []
        self.board_size = board_size
        self.game_round = 0
        self.start_player = 1
        self.win = win
        self.logger = logging.getLogger(__name__)
        if self.board_size > MAX_LOW:
            raise ValueError(f'Board size has reached its limit ({MAX_LOW})!')
        if self.win > self.board_size:
            raise ValueError('Winning number exceeds the board size!')
        self.pos_range = range(self.board_size)
        self.pos = [[0 for _ in self.pos_range] for _ in self.pos_range]
        self.top_row = [self.board_size for _ in self.pos_range]
        self.available_actions = list(product(self.pos_range, self.pos_range))
        self.move = (-1, -1)
        #elif pos:
        #    self.win = win
        #    if isinstance(pos, str):
        #        self.board_size = int(math.sqrt(len(pos)))
        #    else:
        #        if isinstance(pos[0], list):
        #            self.board_size = len(pos)
        #        else:
        #            self.board_size = int(math.sqrt(len(pos)))
        #if pos:
        #    if isinstance(pos, str):
        #        pos = self.str2state(pos)
        #    if nested:
        #        self.pos = copy.deepcopy(pos)
        #    else:
        #        for ind, val in enumerate(pos):
        #            i, j = self.compute_coordinate(ind)
        #            self.pos[i][j] = val

        #self.count_round()
        self.player_number = 2
        self.chess_number = [0 for x in range(self.player_number)]
        self.user_pos_dict = {x:[] for x in range(1, self.player_number + 1)}
        
        self.check = {}
        self.history = {}
        self.half_angle = [_*math.pi/4 for _ in range(DIR_NUM)]
        self.full_angle = [_*math.pi/4 for _ in range(FULL_DIR_NUM)]

        self.check_re = re.compile(r'^\s*([1-9]\d*)\s*,\s*([1-9]\d*)\s*$')
        self.check_row_re = re.compile(r'^([1-9]\d*)$')
        
    def __str__(self):
        return ''.join([''.join([str(x) for x in y]) for y in self.pos])

    def __repr__(self):
        return ''.join([''.join([str(x) for x in y]) for y in self.pos])

    def __getitem__(self, pos):
        return self.pos[pos[0]][pos[1]]

    def mround(self):
        "Maximum possible round for this game"
        return self.board_size**2

    def info(self):
        self.logger.info(f"Current Player: {self.player}, last move: {self.move}")

    def celebrate(self, duel=False):
        if not duel:
            print(f"Congradulations! Player {self.player_ch} won the game!\n")
        else:
            print(f"Duel!")

    @property
    def player(self):
        return 2 - self.game_round % self.player_number

    @property
    def player_ch(self):
        return self.character[self.player]

    def process_ipt(self, ipt):
        mat = self.check_re.match(ipt)
        if mat is None:
            raise ValueError('Error format of coordinate, must be a tuple of two integers, e.g. (1, 1)')
        pos = mat.groups()
        pos = (int(pos[0]) - 1, int(pos[1]) - 1)
        if not self.within_range(pos):
            raise ValueError(f'Coordinate {pos} exceeds range of chessboard {self.board_size}')
        self.validate_pos(pos)
        return pos

    def process_single_ipt(self, ipt):
        """This function is used to process single input of row, particular for fourinarow game"""
        mat = self.check_row_re.match(ipt)
        if mat is None:
            raise ValueError('Error format of coordinate, must be a tuple of one integer, e.g., 1')
        column = int(mat.groups()[0])
        if column > self.board_size or column <= 0:
            raise ValueError(f'Coordinate {column} exceeds range of chessboard with {self.board_size}')
        row = self.get_row_by_column(column)
        if row == 0:
            raise ValueError(f'There is a chess piece!')
        pos = (row - 1, column - 1)
        return pos

    @property
    def state(self):
        return [y for x in self.pos for y in x]

    def str2state(self, pos_str):
        return [int(x) for x in pos_str]

    def get_column(self, column):
        return [_[column - 1] for _ in self.pos]

    def state2board(self, state):
        board_size = int(math.sqrt(len(state)))
        board = [[0 for x in range(board_size)] for y in range(board_size)]
        for ind, val in enumerate(state):
            row = ind // board_size
            column = ind % board_size
            board[row][column] = val
        return board

    def positions(self, board=None):
        """Return the available positions based on a board"""
        if board is None:
            return self.available_actions
        else:
            available_actions = []
            for i in self.pos_range:
                for j in self.pos_range:
                    if board[i][j] == 0:
                        available_actions.append((i, j))
            return available_actions

    def within_range(self, pos):
        if 0 <= pos[0] < self.board_size and 0 <= pos[1] < self.board_size:
            return True
        else:
            return False

    def skip_round(self, times=1):
        for i in range(times):
            self.history[self.game_round + i] = copy.deepcopy(self.pos)
        self.game_round += times

    def get_close_chess(self, current, angle, step=1):
        return (int(current[0] + step*sign(math.cos(angle))), int(current[1] - step*sign(math.sin(angle))))

    def get_all_pos(self, player):
        pos_list = []
        for x, i in enumerate(self.pos):
            for y, j in enumerate(i):
                if j == player:
                    pos_list.append((x, y))
        return pos_list

    def compute_coordinate(self, index):
        '''Compute two-dimension coordinate from one-dimension list'''
        j = index % self.board_size
        i = (index - j) // self.board_size
        return (i, j)

    def count_round(self):
        for ind_i, val_i in enumerate(self.pos):
            for ind_j, val_j in enumerate(val_i):
                if val_j != 0:
                    self.game_round += 1

    def undo(self, times=1):
        if times >= self.game_round:
            raise ValueError('Too many undos!')
        else:
            self.game_round = self.game_round - times
            self.pos = self.history[self.game_round]
    
    def print_pos(self, coordinates=None, pos=None, color='r', bcolor='k'):
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
                            'color': color,
                            #'bcolor': bcolor,
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
        if self.game_round % 2:
            return 1
        else:
            return 2

    def another_player(self, player=None):
        if not player:
            player = self.get_player()
        return 2 - (1 + player) % 2

    def another_player_str(self, player=None):
        return self.character.get(self.another_player(player))
    
    def set_pos(self, pos, validate=False):#, check=False):
        '''Set a chess'''
        if validate:
            self.validate_pos(pos)
        x, y = pos
        self.available_actions.remove(pos)
        self.move = (x + 1, y + 1)
        player = self.get_player()
        self.history[self.game_round] = copy.deepcopy(self.pos)
        self.pos[x][y] = player
        self.logger.debug(f"SET_POS -- Current player: {player}")
        if self.top_row[y] > x:
            self.top_row[y] = x
        self.user_pos_dict[player].append(pos)

    def play(self):
        finish = False
        duel = False
        max_round = self.mround()
        while not finish:
            self.game_round += 1
            self.print_pos()
            self.info()
            vpos = self.input()
            self.set_pos(vpos)
            finish = self.check_win_by_step(vpos, player=self.player)
            if self.game_round == max_round and not finish:
                duel = True
                break
        self.celebrate(duel=duel)
        self.print_pos()

    def _transform(self, val):
        return self.character.get(val)

    def clear(self):
        '''Clear a chessboard'''
        self.pos = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.graph = copy.deepcopy(self.pos)
        self.game_round = 0
        self.available_actions = list(product(self.pos_range, self.pos_range))
        self.top_row = [self.board_size for _ in self.pos_range]

    def input(self):
        ipt = input("Please input your chess position:")
        pos = self.process_ipt(ipt)
        return pos

    def check_win(self):
        '''Check the eight direction of (x, y) for a line
        Eight direction
        1 2 3
        4 X 5
        6 7 8
        Border: 0 ~ self.board_size-1
        '''
        pass

    #def validate_input(self, input_str):
    #    input_str = input_str.replace(' ', '')
    #    pos_str = input_str.split(',')
    #    pos_xy = []
    #    if pos_str[0] == 'u':
    #        try:
    #            times = int(pos_str[1])
    #        except Exception as e:
    #            raise ValueError('Error command, undo command: u, {times}')
    #        else:
    #            return ('u', times)
    #    for pos in pos_str:
    #        if len(pos) != 1:
    #            raise ValueError('Error position, form: x, y, one character at most')
    #        pos_num = self.asc2pos(pos)
    #        pos_xy.append(pos_num)

    #    #if self.game_name == 'fourinarow':
    #    #    y = pos_xy[0]
    #    #    x = 0
    #    #else:
    #    if len(pos_xy) != 2:
    #        raise ValueError('Error position, must have both x and y coordinates')
    #    x, y = pos_xy
    #    self.validate_pos((x, y))
    #    #if self.game_name == 'fourinarow':
    #    #    x = self.get_not_num(self.get_column(y)) - 1
    #    #    if x not in self.pos_range:
    #    #        raise PositionError('This column is full')
    #    return (x, y)

    def validate_pos(self, pos):
        x, y = pos
        t = self.pos[x][y]
        if t != 0:
            raise PositionError('There is a chess piece on that position')
        return True

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

    def check_win_by_step(self, pos, player, line_number=None):
        ''' Check winners by current step
            Eight direction:
                  🡔|↑|🡕 
                  ←|o|→
                  🡗|↓|🡖

            3π/4|   π   |5π/4
             π/2|   O   |3π/2
             π/4|   0   |7π/4

        (-1, -1)|(-1, 0)|(-1, 1)
         (0, -1)|(0, 0) |(0, 1)
         (1, -1)|(1, 0) |(1, 1)

            # direction = [Forward (0 ~ π), Backward (π ~ 2π)]
        '''
        if not line_number:
            line_number = self.win
        x, y = pos
        self.logger.debug(f"Current position: {(x, y)}")
        for ang in self.half_angle:
            self.win_list = [(x, y)]
            angs = [ang, ang + math.pi]
            line_num = 1
            radius = 1
            direction = [1, 1]
            while direction != [0, 0]:
                if line_num == line_number:
                    return True
                for ind, a in enumerate(angs):
                    if direction[ind]:
                        target_x = int(x + radius*(sign(math.cos(a))))
                        target_y = int(y - radius*(sign(math.sin(a))))
                    else:
                        target_x = target_y = -1
                    if target_x < 0 or target_y < 0 or target_x >= self.board_size or target_y >= self.board_size:
                        direction[ind] = 0
                    else:
                        next_pos = self.pos[target_x][target_y]
                        self.logger.debug(f"Radius: {radius}, Angle: {a * 57.2957795:.0f}, Position: {(target_x, target_y)}"
                                f"direction: {direction}, Player: {player} "
                                f"Next_pos: {next_pos}")
                        if next_pos == player:
                            self.win_list.append((target_x, target_y))
                            line_num += 1
                            self.logger.debug(f"Win_list: {self.win_list}")
                        else:
                            direction[ind] = 0
                else:
                    radius += 1
        else:
            return False

    def get_not_num(self, seq, num=0):
        '''Find the index of first non num element'''
        ind = next((i for i, x in enumerate(seq) if x != num), None)
        if ind == None:
            return self.board_size
        else:
            return ind

    def count_chess(self):
        result = [0 for x in range(self.player_number)]
        for i in self.pos:
            for j in i:
                result[j - 1] = result[j - 1] + 1 if j != 0 else result[j - 1]
        return result

    def get_row_by_column(self, column):
        '''Get the available row number of the given column
        e.g.:
            1 2 3
          1| | |X|
          2|O| |O|
          3|X| |X|
        assert get_row_by_column(1) == 1
        assert get_row_by_column(2) == 3
        assert get_row_by_column(3) == 0
        NOTE: 0 is unavailable move

        Args:
            column: The actual index of column (1, 2, 3 in the e.g.)
        Return:
            int: The actual index of top index of row (0, 1, 2, 3 in  the e.g.)
        '''
        return self.top_row[column - 1]
        

class ChessboardExtension(Chessboard):
    '''Provide extended methods for Class Chessboard'''
    def __init__(self, board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', player_number=2, game_name=None, pos=None, nested=False):
        super().__init__(
            board_size=board_size,
            win=win,
            ch_off=ch_off,
            ch_def=ch_def,
            ch_blank=ch_blank,
            player_number=player_number,
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
