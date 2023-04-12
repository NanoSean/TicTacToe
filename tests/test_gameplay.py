"""Module for testing Games of TicTacToe"""
import pytest

from .src.board import TicTacToe


@pytest.mark.parametrize(
    "player_indexes,x_coordinates,y_coordinates,expected",
    [
        ([1, 2, 1, 2, 1], [0, 0, 1, 2, 2], [0, 1, 1, 1, 2], 1),
        ([2, 1, 2, 1, 2], [0, 0, 1, 2, 2], [0, 1, 1, 1, 2], 2),
        ([2, 1, 2, 1, 2, 1, 2], [1, 0, 0, 2, 1, 0, 1], [1, 0, 1, 1, 2, 2, 0], 2),
        (
            [1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 0, 0, 1, 1, 2, 2, 2, 0],
            [0, 1, 2, 1, 2, 2, 1, 0, 0],
            0,
        ),
    ],
)
def test_board_size_3_scenarios(player_indexes, x_coordinates, y_coordinates, expected):
    """Test a series of game scenarios in 3x3 board"""
    board = TicTacToe()
    for i, player_index in enumerate(player_indexes):
        result = board.play_one_step(player_index, x_coordinates[i], y_coordinates[i])
        if result > 0:
            break
    assert expected == result


@pytest.mark.parametrize(
    "player_indexes,x_coordinates,y_coordinates,win_length,expected",
    [
        ([1, 2, 1, 2, 1], [0, 0, 1, 2, 2], [0, 1, 1, 1, 2], 3, 1),
        ([2, 1, 2, 1, 2], [0, 0, 1, 2, 2], [0, 1, 1, 1, 2], 3, 2),
        ([2, 1, 2, 1, 2, 1, 2], [1, 0, 0, 2, 1, 0, 1], [1, 0, 1, 1, 2, 2, 0], 3, 2),
        (
            [1, 2, 1, 2, 1, 2, 1, 2, 1],
            [1, 0, 0, 1, 1, 2, 2, 2, 0],
            [0, 1, 2, 1, 2, 2, 1, 0, 0],
            3,
            0,
        ),
        (
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 0, 0, 1, 1, 2, 2, 2, 0, 3],
            [0, 1, 2, 1, 2, 2, 1, 0, 0, 3],
            4,
            0,
        ),
        (
            [2, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 0, 0, 2, 1, 0, 1, 3, 1],
            [1, 0, 1, 1, 2, 2, 0, 2, 3],
            4,
            2,
        ),
        ([1, 2, 1, 2, 1, 2, 1], [0, 0, 1, 2, 2, 3, 3], [0, 1, 1, 1, 2, 0, 3], 4, 1),
        ([1, 2, 1, 2, 1, 2, 1], [0, 1, 0, 1, 0, 1, 0], [0, 1, 1, 2, 2, 3, 3], 4, 1),
        ([1, 2, 1, 2, 1, 2, 1], [0, 1, 1, 2, 2, 3, 3], [0, 1, 0, 1, 0, 1, 0], 4, 1),
        (
            [
                2,
                1,
                2,
                1,
                2,
                1,
                2,
            ],
            [0, 0, 1, 2, 2, 3, 3],
            [0, 1, 1, 1, 2, 0, 3],
            4,
            2,
        ),
        (
            [
                2,
                1,
                2,
                1,
                2,
                1,
                2,
            ],
            [0, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 2, 2, 3, 3],
            4,
            2,
        ),
        (
            [
                2,
                1,
                2,
                1,
                2,
                1,
                2,
            ],
            [0, 1, 1, 2, 2, 3, 3],
            [0, 1, 0, 1, 0, 1, 0],
            4,
            2,
        ),
    ],
)
def test_board_size_4_scenarios(
    player_indexes, x_coordinates, y_coordinates, win_length, expected
):
    """Test a series of game scenarios in 4x4 board."""
    board = TicTacToe(board_size=4, win_length=win_length)
    for i, player_index in enumerate(player_indexes):
        result = board.play_one_step(player_index, x_coordinates[i], y_coordinates[i])
        if result > 0:
            break
    assert expected == result
