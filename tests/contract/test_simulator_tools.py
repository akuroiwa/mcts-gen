
import pytest
from unittest.mock import MagicMock, patch

from mcts_gen.services.ai_gp_simulator import AiGpSimulator
from fastmcp import FastMCP

@pytest.fixture
def simulator() -> AiGpSimulator:
    mcp = FastMCP()
    sim = AiGpSimulator(mcp)
    sim.reinitialize_mcts(
        state_module="mcts_gen.games.dummy_game",
        state_class="TicTacToeDummy"
    )
    return sim

def test_get_possible_actions(simulator: AiGpSimulator):
    actions_result = simulator.get_possible_actions()
    assert "error" not in actions_result
    assert len(actions_result.get("possible_actions", [])) == 9

def test_policy_pruning(simulator: AiGpSimulator):
    assert simulator.engine is not None
    with patch.object(simulator.engine, 'expand', wraps=simulator.engine.expand) as mock_expand:
        simulator.run_mcts_round(exploration_constant=1.4, actions_to_expand=[0, 8])
        assert len(simulator.engine.root.children) <= 2
        child_actions = [action for action in simulator.engine.root.children.keys()]
        assert all(action in [0, 8] for action in child_actions)

def test_improvement_metric(simulator: AiGpSimulator):
    """Tests that the 'improvement' metric is calculated correctly across rounds."""
    assert simulator.engine is not None

    with patch.object(simulator.engine, 'getBestChild') as mock_get_best_child:
        # --- Round 1: Establish a baseline UCT value of 0.5 ---
        mock_child_1 = MagicMock()
        mock_child_1.totalReward = 5
        mock_child_1.numVisits = 10
        mock_get_best_child.return_value = mock_child_1
        
        result1 = simulator.run_mcts_round(exploration_constant=1.4)
        stats1 = result1.get("simulation_stats", {})
        assert stats1.get("improvement") == 2  # First run is always an improvement
        assert stats1.get("eaten") == pytest.approx(0.5)

        # --- Round 2: UCT value improves to 0.8 ---
        mock_child_2 = MagicMock()
        mock_child_2.totalReward = 8
        mock_child_2.numVisits = 10
        mock_get_best_child.return_value = mock_child_2

        result2 = simulator.run_mcts_round(exploration_constant=1.4)
        stats2 = result2.get("simulation_stats", {})
        assert stats2.get("improvement") == 2  # 0.8 > 0.5, so it's an improvement
        assert stats2.get("eaten") == pytest.approx(0.8)

        # --- Round 3: UCT value stays the same ---
        mock_get_best_child.return_value = mock_child_2 # Return the same 0.8 value

        result3 = simulator.run_mcts_round(exploration_constant=1.4)
        stats3 = result3.get("simulation_stats", {})
        assert stats3.get("improvement") == 1  # 0.8 == 0.8, so it's the same
        assert stats3.get("eaten") == pytest.approx(0.8)

        # --- Round 4: UCT value decreases to 0.4 ---
        mock_child_3 = MagicMock()
        mock_child_3.totalReward = 4
        mock_child_3.numVisits = 10
        mock_get_best_child.return_value = mock_child_3

        result4 = simulator.run_mcts_round(exploration_constant=1.4)
        stats4 = result4.get("simulation_stats", {})
        assert stats4.get("improvement") == 0  # 0.4 < 0.8, so it's not an improvement
        assert stats4.get("eaten") == pytest.approx(0.4)
