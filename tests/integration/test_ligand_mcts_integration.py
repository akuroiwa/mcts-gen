import unittest
import os
import importlib

# Add project root to path to allow direct imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))


class TestLigandMCTSIntegration(unittest.TestCase):

    def setUp(self):
        """Set up a dummy pocket file for testing."""
        self.pocket_file = "integration_test_pocket.pdb"
        with open(self.pocket_file, "w") as f:
            f.write("ATOM      1  N   ALA A   1      27.340  -2.476  34.922  1.00  0.00           N  \n")
            f.write("ATOM      2  CA  ALA A   1      28.153  -1.296  34.576  1.00  0.00           C  \n")

    def tearDown(self):
        """Clean up the dummy pocket file."""
        if os.path.exists(self.pocket_file):
            os.remove(self.pocket_file)

    @unittest.skipIf(importlib.util.find_spec("rdkit") is None, "RDKit is not installed, skipping integration test")
    def test_dynamic_loading_and_simulation(self):
        """
        Tests if the ligand_mcts module can be dynamically loaded and used in a
        simulated MCTS loop.
        """
        state_module_name = "src.mcts_gen.games.ligand_mcts"
        state_class_name = "LigandMCTSGameState"

        # Dynamically import the module and class
        try:
            module = importlib.import_module(state_module_name)
            game_class = getattr(module, state_class_name)
        except (ImportError, AttributeError) as e:
            self.fail(f"Failed to dynamically load {state_class_name} from {state_module_name}: {e}")

        # Initialize the game state
        initial_state = game_class(pocket_path=self.pocket_file)
        self.assertIsNotNone(initial_state)

        # --- Simulate a few MCTS steps ---
        
        # 1. Get initial actions
        possible_actions = initial_state.getPossibleActions()
        self.assertIsInstance(possible_actions, list)
        self.assertGreater(len(possible_actions), 0)

        # 2. Take an action to get a new state (expansion)
        action_to_take = possible_actions[0]
        new_state = initial_state.takeAction(action_to_take)
        
        self.assertIsNotNone(new_state)
        self.assertNotEqual(initial_state.internal_state.to_smiles(), new_state.internal_state.to_smiles())
        
        # 3. Simulate a rollout from the new state to get a reward
        # (In a real MCTS, you'd continue, but here we just check the reward)
        current_node = new_state
        for _ in range(5): # Rollout for 5 steps
            if current_node.isTerminal():
                break
            actions = current_node.getPossibleActions()
            if not actions:
                break
            # In a real MCTS, this would be random, but we'll be deterministic for the test
            current_node = current_node.takeAction(actions[0])

        # 4. Get the reward from the final state of the rollout
        reward = current_node.getReward()
        self.assertIsInstance(reward, float)


if __name__ == '__main__':
    unittest.main()
