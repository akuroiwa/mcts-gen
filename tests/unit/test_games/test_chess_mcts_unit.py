import pytest
from src.mcts_gen.games.chess_mcts import ChessGameState

def test_get_state_summary_pgn():
    """
    Tests if get_state_summary correctly returns a PGN string.
    """
    # Create a game state
    state = ChessGameState()

    # Make a few moves
    moves = ["e2e4", "e7e5", "g1f3", "b8c6"]
    for move_uci in moves:
        state = state.takeAction(move_uci)

    # Get the summary
    summary = state.get_state_summary()

    # Assertions
    assert "pgn" in summary
    assert isinstance(summary["pgn"], str)
    # The PGN includes headers, so we check for the moves within the string
    assert "1. e4 e5 2. Nf3 Nc6" in summary["pgn"]
