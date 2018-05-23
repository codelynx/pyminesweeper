# Mine Sweeeper with PYGAME

`pyminesweeper` is a game written in Python with PyGame.  The purpose of this source code is
for me (Kaz Yoshikawa) to learn Python 2.x.  You can click to open a cell, or you can right
click to toggle flags.  You may find number of bombs in upper right bar (assuming your flags
are all correct).  The game is end if you opened any bomb in a cell, or you located and defused
all bombs on the board.  It does not offer you to play again, but it is just sufficient
for learning python language.

Unlike typical minesweeper, this code reveals one of the largest safe cell cluster on the
board in the beginning of the game.  So you don't have to cross your finger to click a few 
cells randomly to test your luck.


## Configurations

you may change number of cells on board, and number of bombs by changing the following lines

```
NUM_OF_ROWS = 10
NUM_OF_COLS = 20
NUM_OF_BOMBS = 15

```

Enjoy 😀

Kaz Yoshikawa


## Screenshots

![alt tag](https://raw.github.com/kyoshikawa/pyminesweeper/master/shots/shot1.png)
![alt tag](https://raw.github.com/kyoshikawa/pyminesweeper/master/shots/shot2.png)


## License

The MIT License (MIT)

Copyright (c) 2018 Kaz Yoshikawa (kaz.yoshikawa@gmail.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.



