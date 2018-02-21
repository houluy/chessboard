import sys
from chessboard import Chessboard
from colorline import cprint

def play_game():
    while True:
        game_name = input('Please input the game name: ')
        try:
            board = Chessboard(game_name=game_name)
        except ValueError as e:
            cprint(e)
            continue
        else:
            break

    board.print_pos()
    while True:
        try:
            ipt = input('Input:')
        except:
            cprint('Input Error: try again.', color='g')
            continue
        if game_name != 'fourinarow':
            try:
                a = board.handle_input(ipt, check=True)
            except Exception as e:
                cprint(e, color='g')
                board.print_pos()
                continue
        else:
            a = board.handle_input(ipt, place=False)
            if a is None:
                board.print_pos()
                continue
            column_num = int(a[0])
            current_col = [_[column_num - 1] for _ in board.pos]
            current_row = board.get_not_num(current_col)
            if current_row == 0:
                cprint('No place to put your chess!', color='g')
                continue
            else:
                try:
                    a = board.set_pos(x=current_row, y=column_num, check=True)
                except (PositionError, Exception) as e:
                    cprint(e, color='g')
                    continue
        if a is True:
            cprint('player {} wins'.format(board.get_player()), color='y', bcolor='b')
            board.print_pos()
            sys.exit(0)
        board.print_pos(coordinates=a)
        #print(str(board))

if __name__ == '__main__':
    play_game()
