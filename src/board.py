"""Module implementing Tic Tac Toe game."""
from typing import List, Tuple

import numpy as np

class TicTacToe:
    """The representation of the board and the state."""

    def __init__(self, board_size=3, win_length=3):
        """Init for Tic Tac Toe Class."""
        if board_size <= 2:
            raise Exception("Board size less than 3 is not allowed")

        if win_length > board_size:
            raise Exception("Win length must be less than board size.")

        self.board_size = board_size
        self.win_length = win_length
        self.board = np.zeros([board_size, board_size])
        self.player_indexes = [1, 2]
        self.last_played_by = None
        self._neighbours = (
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, 1),
            (0, -1),
            (1, 1),
            (1, 0),
            (1, -1),
        )

    def reset_board(self):
        """Resets the board to starting position."""
        self.board = np.zeros([self.board_size, self.board_size])
        self.last_played_by = None

    def is_index_bound(self, coordinate: int) -> bool:
        """Checks if the given position 'x' is within the bounds of the board dimmension.

        Args:
            coordinate (int): The position to be played

        Returns:
            bool: True if it is within the board dimmension, False otherwise.
        """
        if coordinate >= self.board_size or coordinate < 0:
            return False
        return True

    def is_player_valid(self, player_index: int) -> bool:
        """Checks if the player index is acceptable by the definition of the player indexes.

        Args:
            player_index (int): The index of the player of the current move.

        Returns:
            bool: True if the player index is True, False otherwise.
        """
        if player_index not in self.player_indexes:
            return False
        return True

    def is_grid_occupied(self, x_coordinate: int, y_coordinate: int) -> bool:
        """Checks if a position on the board is already been played before.

        Args:
            x_coordinate (int): The x dimension of the board
            y_coordinate (int): The x dimension of the board
        Returns:
            bool: True if its occupied, False otherwise
        """
        if self.board[x_coordinate, y_coordinate] != 0:
            return True
        return False

    def is_consecutive_player(self, player_index: int) -> bool:
        """Checks if the move is played by the same player consecutively.

        Args:
            player_index (int): The index of the player playing the move

        Returns:
            bool: True if it is consecutive, False otherwise.
        """
        if self.last_played_by and self.last_played_by == player_index:
            return True
        return False

    def get_winner(self, x_coordinate: int, y_coordinate: int) -> int:
        """Return the player index of the winner, if there is one. Return 0 otherwise.

        Args:
            x_coordinate (int): x coordinate of last placed point.
            y_coordinate (int): y coordinate of last placed point
        Returns:
            int: The player index of the winner, if there is one otherwise 0.
        """
        edges = list(self._neighbours)
        while len(edges) > 0:
            edge = edges.pop()
            path_start = self._take_step_in_direction(
                [x_coordinate, y_coordinate], edge
            )

            if not self.is_index_bound(path_start[0]) or not self.is_index_bound(
                path_start[1]
            ):
                continue
            if self.board[path_start[0], path_start[1]] != self.last_played_by:
                continue

            path = [[x_coordinate, y_coordinate]]
            self._find_path([x_coordinate, y_coordinate], edge, path)
            if len(path) == self.win_length:
                return self.last_played_by

            reflection = (edge[0] * -1, edge[1] * -1)
            if reflection in edges:
                edges.remove(reflection)
        return 0

    def check_valid_move(
        self, player_index: int, x_coordinate: int, y_coordinate: int
    ) -> List:
        """Check if the current move (x, y) by the player 'player_index' is valid.

        Please implement this.

        Args:
            player_index (int): The index of the player of the current move.
            x_coordinate (int): The x position.
            y_coordinate (int): The y position.

        Returns:
            List: All the errors that are found during the validation, [] otherwise.
        """
        messages = []
        if not self.is_player_valid(player_index):
            messages.append(f"Invalid Player index. Must be in {self.player_indexes}")

        if self.is_consecutive_player(player_index):
            messages.append(
                f"Player {player_index} has just been. Time for another player!"
            )

        coordinates_in_bounds = True
        if not self.is_index_bound(x_coordinate):
            messages.append(f"x_coord: {x_coordinate} is out of bounds.")
            coordinates_in_bounds = False

        if not self.is_index_bound(y_coordinate):
            messages.append(f"y_coord: {y_coordinate} is out of bounds.")
            coordinates_in_bounds = False

        if not coordinates_in_bounds:
            return messages

        if self.is_grid_occupied(x_coordinate, y_coordinate):
            messages.append(
                f"Position: {x_coordinate}, {y_coordinate} is already taken!"
            )
        return messages

    def __str__(self):
        """Return string representation of board when printing the class."""
        return str(self.board)

    def play_one_step(
        self, player_index: int, x_coordinate: int, y_coordinate: int
    ) -> int:
        """Plays one step of the game.

        This function should validate the move and also see if the move wins the board.

        Args:
            player_index (int): The index of the player of the current move.
            x_coordinate (int): The x position.
            y_coordinate (int): The y position.

        Raises:
            Exception: If the move is invalid

        Returns:
            int: The index of the winning player, 0 otherwise
        """
        messages = self.check_valid_move(player_index, x_coordinate, y_coordinate)
        if messages:
            raise Exception(f"The move is illegal : {','.join(messages)}")

        self.board[x_coordinate, y_coordinate] = player_index
        self.last_played_by = player_index

        print(self)

        won_player = self.get_winner(x_coordinate, y_coordinate)
        if won_player != 0:
            print(f"Game won by {won_player}")
            return won_player
        return 0

    # pylint: disable=inconsistent-return-statements
    def _find_path(
        self, start: List[int], edge: Tuple, current_path: List[List[int]]
    ) -> None:
        """Recursive method for finding the longest path from initial point.

        Args:
            start (list): [x, y] coordinates of the start of the recursion
            edge (tuple): tuple of direction vectors to take a step.
            current_path (list): current path found during recursion.

        Returns:
            The recursion will change the current_path list in place.
        """
        point = start.copy()
        point = self._take_step_in_direction(point, edge)

        # Path has looped on itself, return the path found
        if point in current_path:
            return current_path

        if len(current_path) == self.win_length:
            return current_path

        point_out_of_bounds = not self.is_index_bound(
            point[0]
        ) or not self.is_index_bound(point[1])

        if not point_out_of_bounds and (
            self.board[point[0], point[1]] == self.last_played_by
        ):
            current_path.append(point)
            return self._find_path(point, edge, current_path)

        # Reflect edge and try other direction
        edge = (edge[0] * -1, edge[1] * -1)
        next_point = self._take_step_in_direction(current_path[0], edge)
        next_point_out_of_bounds = not self.is_index_bound(
            next_point[0]
        ) or not self.is_index_bound(next_point[1])

        if next_point_out_of_bounds:
            return current_path

        if self.board[next_point[0], next_point[1]] != self.last_played_by:
            return current_path

        return self._find_path(current_path[0]*2, edge, current_path)

    # pylint: disable=inconsistent-return-statements

    @staticmethod
    def _take_step_in_direction(point: List[int], edge: Tuple) -> list:
        """Move point to next point via a direction vector, edge."""
        new_point = [np.nan] * 2
        new_point[0] = point[0] + edge[0]
        new_point[1] = point[1] + edge[1]
        return new_point
