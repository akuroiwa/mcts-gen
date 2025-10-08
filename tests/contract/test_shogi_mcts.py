
import shogi
from src.mcts_gen.games.shogi_mcts import ShogiGameState

def test_shogi_take_action():
    """Tests that ShogiGameState.takeAction can execute without errors."""
    # 1. Create an initial state
    initial_state = ShogiGameState(sfen="")

    # 2. Get a legal move object
    legal_moves = initial_state.getPossibleActions()
    assert len(legal_moves) > 0
    action_to_take = shogi.Move.from_usi(legal_moves[0]) # Convert USI string to Move object

    # 3. Call takeAction
    try:
        new_state = initial_state.takeAction(action_to_take)
        # 4. Check the result
        assert new_state is not None
        assert isinstance(new_state, ShogiGameState)
        assert new_state.board != initial_state.board
    except Exception as e:
        assert False, f"takeAction failed with an unexpected error: {e}"
