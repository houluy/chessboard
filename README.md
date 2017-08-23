# chessboard
A chessboard for board games in Python

## Init an chessboard instance
### Class Chessboard:
#### `__init__(self, board_size=3, win=3, ch_off='O', ch_def='X', ch_blank=' ', user_number=2)`
* `board_size` defines the size of the chessboard
* `win` defines the number of chess pieces to win in a line
* `ch_off` defines the character of offensive player
* `ch_def` defines the character of defensive player
* `ch_black` defines the character of default place
* `user_number` defines the number of players (No use)

#### `set_pos(self, x, y, user)`
* `x, y` are the coordinates of chess
* `user` is the order of player  

#### `set_pos_on_board_special(self, x, y, user, board=None, user_number=2)`  
* Set a chess on a specific coodinate (x, y) for user on board  
* If `board` is given, put on the `board`, else, put on the `self.pos`  

#### `print_pos(self, pos=None)`
* Print the chessboard, if `pos` is given, print `pos`, else, print `self.pos`

#### `rotate_board(self, angle, unit='radian')`  
* Rotate the chessboard _anticlockwise_ for `angle` degree/radian (based on `unit`), using the center of the chessboard as the center of rotation, e.g.,  
```
    1 2 3
  1|O|X| |
  2| | | |
  3| | | |
```
becomes  
```
    1 2 3
  1| | |O|
  2| | |X|
  3| | | |
```
when call `self.rotate_board(270, 'angle')`  

#### Chessboard:
```
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
```

#### Game:
A Game is implemented by Chessboard class. Players can set the size of chessboard and number of chess pieces conducting to winning in game.py. Run _game.py_ directly to play.
- Four In A Row: Players can play four-in-a-row by initializing the Game with `game='fourinarow'`

##### Useful functions:
1. Get the sign of an integer:
`sign = lambda a: (a>0) - (a<0)`
2. In Python 3.4, `math.cos(math.pi/2) = xxx*e(-17)`, an integer beyond **zero**  
3. Coodinate rotation formula (ANTICLOCKWISE):  
```
tx = (x - x0)*cos(theta) - (y - y0)*sin(theta) + x0  
ty = (x - x0)*sin(theta) + (y - y0)*cos(theta) + y0
```

