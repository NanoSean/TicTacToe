#### Recursive

The current solution in `main` is a recursive method which uses a form of Breadth First Search (BFS) and then checks
the total path that is possible to reach once a point is placed. This method has time complexity O(n).

The method can be briefly summarised as follows: 

1. We start with a list of all possible directions. 
2. Pick a direction to take a step from the current point. 
3. Check that point is in bounds and is of the same value as the player placing the point.
4. If it is then add it to path and take another step in the same direction. 
5. repeat 3. and 4. until we do not satisfy either criteria in 3. 
6. Reflect the direction of the point and repeat 3, 4, 5. 
7. We have calculated our longest path in the direction of travel and its opposite direction (connected points).
8. If it is the length of win we can end the game. Else we remove the direction and its opposite from the list of possible directions and go back to 2.

### Non-Recursive
The solution in branch `non-recursive-implementation` is a method based on updating four relative positional matrices 
per player: a `horizontal`, `vertical`, `diagonal from left to right`, `diagonal from right to left`. 

A brief explanation of this method is as follows: 
1. Place a point, the values next to it in the direction of each positional matrix are checked. 
2. These points will contain the number of consecutive points that are present of the player in the direction of the step. 
3. Update each of these matrices until the values within one of the matrices are larger to or equal to the desired winning criteria.

To do this one has to consider four scenarios at each stage: 

1. There are no consecutive points around the placed point (surrounded by zeros in relevant direction).
2. All consecutive points are below the placed point.
3. All consecutive points are above the placed point.
4. The placed point is between two existing runs of consecutive points above and below.

By checking each of these criteria we can ensure that when a run of the correct length occurs in any of the matrices,
the game has been won. 

This method is more complex in terms of code readability, hence is in a branch, but has time complexity O(1).

## How to Play
The game is designed to be played in the python console. The default game is regular Tic-Tac-Toe
(`board_size=3`, `win_length=3`). 
To play a game of Tic-Tac-Toe in the python console one can start the game off like so:

```shell
>>> from src.board import TicTacToe
>>> game = TicTacToe()
```

A player takes a move by using the `game.play_one_step(play_one_step(player_index, x_coordinate, y_coordinate))` method.
The user who is placing the point is `player_index` and its position is `x_coordinate, y_coordinate`. 
The board will appear after each step is taken, below is an example of a full game being played. 
```shell
>>> game.play_one_step(1,1,1)

[[0. 0. 0.]
 [0. 1. 0.]
 [0. 0. 0.]]
 0
 
 >>> game.play_one_step(2,0,1)
[[0. 2. 0.]
 [0. 1. 0.]
 [0. 0. 0.]]
0

>>> game.play_one_step(1,0,0)
[[1. 2. 0.]
 [0. 1. 0.]
 [0. 0. 0.]]
0

>>> game.play_one_step(2,1,2)
[[1. 2. 0.]
 [0. 1. 2.]
 [0. 0. 0.]]
0
>>> game.play_one_step(1,2,2)
[[1. 2. 0.]
 [0. 1. 2.]
 [0. 0. 1.]]
Game won by 1
```
Once the game is won, one can reset the board as follows:

```shell
>>> game.reset_board()
```

An example of a non-standard game of Tic-Tac-Toe: 
```shell 
>>> game = TicTacToe(board_size=4, win_length=3)

>>> game.play_one_step(1,2,2)
[[0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 0.]]
0

>>> game.play_one_step(2,1,1)
[[0. 0. 0. 0.]
 [0. 2. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 0.]]
0
>>> game.play_one_step(1,2,1)
[[0. 0. 0. 0.]
 [0. 2. 0. 0.]
 [0. 1. 1. 0.]
 [0. 0. 0. 0.]]
0

>>> game.play_one_step(2,2,3)
[[0. 0. 0. 0.]
 [0. 2. 0. 0.]
 [0. 1. 1. 2.]
 [0. 0. 0. 0.]]

>>> game.play_one_step(1,2,0)
[[0. 0. 0. 0.]
 [0. 2. 0. 0.]
 [1. 1. 1. 2.]
 [0. 0. 0. 0.]]
Game won by 1

```

