Chessboard
**********

This is what the chessboard looks like:

::

    * 1 2 3 4 5 6 7 8 9 A
    1|X| | | | | | | | | |
    2| |O| | | | | | | | |
    3| | |X| | | | | | | |
    4| | | |O| | | | | | |
    5| | | | |X| | | | | |
    6| | | | | |O| | | | |
    7| | | | | | |X| | | |
    8| | | | | | | |O| | |
    9| | | | | | | | |X| |
    A| | | | | | | | | |O|

Init
****

The Chessboard class

::

    chessboard.Chessboard(board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', user_number=2)

* `board_size` defines the size of the chessboard
* `win` defines the number of chess pieces to win in a line
* `ch_off` defines the character of offensive player
* `ch_def` defines the character of defensive player
* `ch_black` defines the character of default place
* `user_number` defines the number of players (No use)

Methods
*******

Some methods to operate the chessboard is listed

::

    self.set_pos(x, y, user=None)

* `x, y` are the coordinates of chess.
* `user` is the player index.

::

    self.set_pos_on_board_special(x, y, user=None, board=None, user_number=2)

* Set a chess on a specific coodinate (x, y) for user on board
* If `board` is given, put on the `board`, else, put on the `self.pos`

::

    self.print_pos(pos=None)

* Print the chessboard, if `pos` is given, print `pos`, else, print `self.pos`

::

    self.rotate_board(angle, unit='radian')

* Rotate the chessboard *anticlockwise* for `angle` degree/radian (based on `unit`), using the center of the chessboard as the center of rotation, e.g.,

::

  * 1 2 3
  1|O|X| |
  2| | | |
  3| | | |

becomes  

::

  * 1 2 3
  1| | |O|
  2| | |X|
  3| | | |

when call `self.rotate_board(270, 'angle')`

::

    self.handle_input(input_str, user=None, check=False)

* Handle the input of user, can be *coordinates* or *commands*.
* `input_str` The input string.
* `user` The player index, can be calculated automatically.
* `check` Whether to check winner.

::

    self.undo(times=1)

* Undo 
* `times` Undo times, default 1

