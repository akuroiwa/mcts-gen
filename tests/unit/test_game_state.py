
import pytest
from mcts_gen.models.game_state import GameStateBase

def test_game_state_base_is_abstract():
    """Tests that GameStateBase cannot be instantiated directly."""
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        GameStateBase()

def test_concrete_game_state_requires_methods():
    """Tests that a concrete class must implement all abstract methods."""

    # This class is incomplete
    class IncompleteState(GameStateBase):
        def getCurrentPlayer(self):
            return 1

    with pytest.raises(TypeError):
        IncompleteState()

    # This class is complete
    class CompleteState(GameStateBase):
        def getCurrentPlayer(self):
            return 1
        def getPossibleActions(self):
            return ["a", "b"]
        def takeAction(self, action):
            return self
        def isTerminal(self):
            return False
        def getReward(self):
            return 0.0

    # This should instantiate without error
    instance = CompleteState()
    assert instance is not None
    assert instance.getCurrentPlayer() == 1
