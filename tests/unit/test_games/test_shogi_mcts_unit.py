import pytest
from mcts_gen.games.shogi_mcts import ShogiGameState

def test_get_state_summary_kif():
    """
    Tests if get_state_summary correctly returns a KIF string.
    """
    # Create a game state
    state = ShogiGameState()

    # Make a few moves
    moves = ["7g7f", "3c3d", "8h2b+"]
    for move_usi in moves:
        state = state.takeAction(move_usi)

    # Get the summary
    summary = state.get_state_summary()

    # Assertions
    assert "kif" in summary
    assert isinstance(summary["kif"], str)
    assert "1 ７六歩(77)" in summary["kif"]
    assert "2 ３四歩(33)" in summary["kif"]
    assert "3 ２二角成(88)" in summary["kif"]
