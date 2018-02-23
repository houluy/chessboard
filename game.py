import sys
from chessboard import Chessboard, PositionError
from colorline import cprint

from functools import partial

eprint = partial(cprint, color='r', bcolor='c', mode='highlight')

def main():
    while True:
        game_name = input('Please input the game name: ')
        try:
            board = Chessboard(game_name=game_name)
        except ValueError as e:
            eprint(e)
            continue
        else:
            break

    board.print_pos()
    while True:
        player_number = board.get_player()
        cprint('Player {}\'s turn: '.format(player_number), color='y', bcolor='c', end='')
        ipt = input('')
        try:
            pos = board.handle_input(ipt, check=True)
        except Exception as e:
            eprint(e)
            board.print_pos()
            continue
        if pos is True:
            cprint('player {} wins'.format(player_number), color='y', bcolor='b')
            board.print_pos()
            sys.exit(0)
        board.print_pos(coordinates=pos)
        #print(str(board))

if __name__ == '__main__':
    main()
