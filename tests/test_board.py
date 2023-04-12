"""Test Module for Tic Tac Toe Class."""
# pylint: disable=protected-access
import pytest

import numpy as np
from .src.board import TicTacToe


@pytest.mark.parametrize("board_size", list(range(-1, 2)))
def test_board_fails(board_size: int):
    """Test that board size <= 2 doesn't work.

    Args:
        board_size (int): size of n x n board.
    """
    message = "Board size less than 3 is not allowed"
    with pytest.raises(Exception, match=message):
        TicTacToe(board_size=board_size)


@pytest.mark.parametrize("player_index,last_played_by", [(1, 2), (2, 1)])
def test_check_valid_move_pass(player_index, last_played_by):
    """Check valid move returns empty list."""
    board = TicTacToe(3)
    board.last_played_by = last_played_by
    message = board.check_valid_move(
        player_index=player_index, x_coordinate=1, y_coordinate=1
    )
    assert not message


@pytest.mark.parametrize("player_index,last_played_by", [(1, 2), (2, 1)])
def test_check_valid_move_fails_with_bad_placement(player_index, last_played_by):
    """Check valid move fails when a place is already taken by another player."""
    board = TicTacToe(3)
    board.last_played_by = last_played_by
    board.board[1, 1] = 1
    messages = board.check_valid_move(
        player_index=player_index, x_coordinate=1, y_coordinate=1
    )

    assert len(messages) == 1
    assert messages[0] == "Position: 1, 1 is already taken!"


@pytest.mark.parametrize("x_coord,y_coord", [(10, 2), (5, 0), (-1, 1)])
def test_check_valid_move_fails_with_x_out_of_bounds(x_coord, y_coord):
    """Test check_valid_move fails when out of bounds is passed."""
    board = TicTacToe(3)
    board.last_played_by = 1
    messages = board.check_valid_move(
        player_index=2, x_coordinate=x_coord, y_coordinate=y_coord
    )

    assert len(messages) == 1
    assert messages[0] == f"x_coord: {x_coord} is out of bounds."


@pytest.mark.parametrize("x_coord,y_coord", [(0, -5), (1, 100), (2, 7)])
def test_check_valid_move_fails_with_y_out_of_bounds(x_coord, y_coord):
    """Test check_valid_move fails when out of bounds is passed."""
    board = TicTacToe(3)
    board.last_played_by = 1
    messages = board.check_valid_move(
        player_index=2, x_coordinate=x_coord, y_coordinate=y_coord
    )

    assert len(messages) == 1
    assert messages[0] == f"y_coord: {y_coord} is out of bounds."


@pytest.mark.parametrize("x_coord,y_coord", [(-1, -5), (-10, 100), (5, -7), (10, 10)])
def test_check_valid_move_fails_with_both_coords_out_of_bounds(x_coord, y_coord):
    """Test check_valid_move fails when out of bounds is passed."""
    board = TicTacToe(3)
    board.last_played_by = 1
    messages = board.check_valid_move(
        player_index=2, x_coordinate=x_coord, y_coordinate=y_coord
    )

    assert len(messages) == 2
    assert messages[0] == f"x_coord: {x_coord} is out of bounds."
    assert messages[1] == f"y_coord: {y_coord} is out of bounds."


@pytest.mark.parametrize(
    "player_index,x_coord,y_coord", [(4, 1, 1), (-10, 1, 0), ("a", 0, 0)]
)
def test_check_valid_move_fails_with_invalid_player_only(
    player_index, x_coord, y_coord
):
    """Test check_valid_move fails when out of bounds is passed."""
    board = TicTacToe(3)
    board.last_played_by = 1
    messages = board.check_valid_move(
        player_index=player_index, x_coordinate=x_coord, y_coordinate=y_coord
    )

    assert len(messages) == 1
    assert messages[0] == f"Invalid Player index. Must be in {board.player_indexes}"


@pytest.mark.parametrize(
    "player_index,x_coord,y_coord", [(1, 1, 1), (1, 1, 0), (1, 0, 0)]
)
def test_check_valid_move_fails_with_consecutive_player_only(
    player_index, x_coord, y_coord
):
    """Test check_valid_move fails when out of bounds is passed."""
    board = TicTacToe(3)
    board.last_played_by = 1
    messages = board.check_valid_move(
        player_index=player_index, x_coordinate=x_coord, y_coordinate=y_coord
    )

    assert len(messages) == 1
    assert (
        messages[0] == f"Player {player_index} has just been. Time for another player!"
    )


@pytest.mark.parametrize(
    "player_index,last_played_by, x_coord,y_coord,expected_messages",
    [
        (
            1,
            1,
            10,
            -1,
            [
                "Player 1 has just been. Time for another player!",
                "x_coord: 10 is out of bounds.",
                "y_coord: -1 is out of bounds.",
            ],
        ),
        (
            10,
            10,
            -10,
            7,
            [
                "Invalid Player index. Must be in [1, 2]",
                "Player 10 has just been. Time for another player!",
                "x_coord: -10 is out of bounds.",
                "y_coord: 7 is out of bounds.",
            ],
        ),
    ],
)
def test_check_valid_move_fails_with_multiple_messages_with_out_of_bounds(
    player_index, last_played_by, x_coord, y_coord, expected_messages
):
    """Test check_valid_move fails when out of bounds is passed."""
    board = TicTacToe(3)
    board.last_played_by = last_played_by
    messages = board.check_valid_move(
        player_index=player_index, x_coordinate=x_coord, y_coordinate=y_coord
    )

    assert messages == expected_messages


@pytest.mark.parametrize(
    "player_index,last_played_by, x_coord,y_coord,expected_messages",
    [
        (
            100,
            100,
            0,
            1,
            [
                "Invalid Player index. Must be in [1, 2]",
                "Player 100 has just been. Time for another player!",
                "Position: 0, 1 is already taken!",
            ],
        ),
        (
            10,
            10,
            1,
            1,
            [
                "Invalid Player index. Must be in [1, 2]",
                "Player 10 has just been. Time for another player!",
                "Position: 1, 1 is already taken!",
            ],
        ),
    ],
)
def test_check_valid_move_fails_with_multiple_messages_with_invalid_placement(
    player_index, last_played_by, x_coord, y_coord, expected_messages
):
    """Test check_valid_move fails when out of bounds is passed."""
    board = TicTacToe(3)
    board.last_played_by = last_played_by
    board.board[x_coord, y_coord] = 1
    messages = board.check_valid_move(
        player_index=player_index, x_coordinate=x_coord, y_coordinate=y_coord
    )

    assert messages == expected_messages


def test_board_recursive_simple_diagonal():
    """Test simple case of recursive path finding in diagonal direction"""
    board = TicTacToe(3)
    board.board[0, 0] = 1
    board.board[1, 1] = 1
    board.board[2, 2] = 1
    path = [[1, 1]]
    board.last_played_by = 1
    board._find_path([1, 1], (1, 1), path)
    assert len(path) == 3


def test_board_recursive_simple_horizontal():
    """Test simple case of recursive path finding in horizontal direction."""
    board = TicTacToe(3)
    board.board[0, 0] = 1
    board.board[0, 1] = 1
    board.board[0, 2] = 1
    path = [[0, 1]]
    board.last_played_by = 1
    board._find_path([0, 1], (0, 1), path)
    assert len(path) == 3


def test_board_recursive_simple_vertical():
    """Test simple case of recursive path finding in vertical direction."""
    board = TicTacToe(3)
    board.board[0, 0] = 1
    board.board[1, 0] = 1
    board.board[2, 0] = 1
    path = [[0, 1]]
    board.last_played_by = 1
    board._find_path([0, 0], (1, 0), path)
    assert len(path) == 3


def test_board_recursive_short_path_diagonal():
    """Test recursive path finding short path in diagonal direction."""
    board = TicTacToe(3)
    board.board[0, 0] = 1
    board.board[1, 1] = 1
    board.board[2, 2] = 0
    path = [[1, 1]]
    board.last_played_by = 1
    board._find_path([1, 1], (1, 1), path)
    assert len(path) == 2


def test_board_recursive_short_path_horizontal():
    """Test recursive path finding short path in horizontal direction."""
    board = TicTacToe(3)
    board.board[0, 0] = 1
    board.board[0, 1] = 1
    board.board[0, 2] = 0
    path = [[0, 1]]
    board.last_played_by = 1
    board._find_path([0, 1], (0, 1), path)
    assert len(path) == 2


def test_board_recursive_short_path_vertical():
    """Test recursive path finding short path in vertical direction."""
    board = TicTacToe(3)
    board.board[1, 0] = 1
    board.board[2, 0] = 1
    board.board[0, 0] = 0
    path = [[0, 1]]
    board.last_played_by = 1
    board._find_path([1, 0], (1, 0), path)
    assert len(path) == 2


def test_recursive_function_in_four_connected_scenario():
    """Test recursive path finding for larger board."""
    board = TicTacToe()
    board.board = np.array(
        [
            [1.0, 2.0, 1.0],
            [
                2.0,
                2.0,
                2.0,
            ],
            [
                0.0,
                1.0,
                0.0,
            ],
        ]
    )
    board.last_played_by = 2
    path = [[1, 0]]
    board._find_path([1, 0], (0, 1), path)
    assert len(path) == 3
