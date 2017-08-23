.. chessboard documentation master file, created by
   sphinx-quickstart on Wed Aug 23 21:51:41 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

###########################
chessboard's documentation!
===========================

This is a chessboard display module for board games in CLI.

************
Installation
============

The `chessboardCLI` package is available on `pypi`::

    pip install chessboardCLI

Remember, the module name is `chessboard` and the package name is `chessboardCLI`.

**********
Chessboard
==========
This is what the chessboard looks like:

    1 2 3 4 5 6 7 8 9 A
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

****
Init
====

The Chessboard class::

    chessboard.Chessboard(board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', user_number=2)

* `board_size` defines the size of the chessboard
* `win` defines the number of chess pieces to win in a line
* `ch_off` defines the character of offensive player
* `ch_def` defines the character of defensive player
* `ch_black` defines the character of default place
* `user_number` defines the number of players (No use)

*******
Methods
=======

Some methods to operate the chessboard is listed  

::
    set_pos(self, x, y, user)

* `x, y` are the coordinates of chess
* `user` is the order of player  

::
    set_pos_on_board_special(self, x, y, user, board=None, user_number=2)

* Set a chess on a specific coodinate (x, y) for user on board  
* If `board` is given, put on the `board`, else, put on the `self.pos`  

::
    print_pos(self, pos=None)

* Print the chessboard, if `pos` is given, print `pos`, else, print `self.pos`

::
    rotate_board(self, angle, unit='radian')

* Rotate the chessboard *anticlockwise* for `angle` degree/radian (based on `unit`), using the center of the chessboard as the center of rotation, e.g.,  

    1 2 3
  1|O|X| |
  2| | | |
  3| | | |

becomes  

    1 2 3
  1| | |O|
  2| | |X|
  3| | | |

when call `self.rotate_board(270, 'angle')`  


.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
