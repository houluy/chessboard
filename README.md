# chessboard
A chessboard module for board games in Linux command-line

Use  
```
pip install chessboardCLI
```

to install it.  

The full docs is provided [here](http://chessboardm.readthedocs.io/).

##### Useful functions:
1. Get the sign of an integer:
`sign = lambda a: (a>0) - (a<0)`
2. In Python 3.4, `math.cos(math.pi/2) = xxx*e(-17)`, a value beyond **zero**  
3. Coodinate rotation formula (ANTICLOCKWISE):  
```
tx = (x - x0)*cos(theta) - (y - y0)*sin(theta) + x0  
ty = (x - x0)*sin(theta) + (y - y0)*cos(theta) + y0
```

