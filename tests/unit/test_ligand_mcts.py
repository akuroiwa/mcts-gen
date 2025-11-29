import unittest
import numpy as np
import os

# Add project root to path to allow direct imports
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.mcts_gen.games.ligand_mcts import (
    LigandAction,
    LigandState,
    Evaluator,
    LigandMCTSGameState,
    load_pocket_atm_pdb
)

# RDKit is a test dependency
try:
    from rdkit import Chem
except ImportError:
    Chem = None


class TestLigandMCTS(unittest.TestCase):
    
    def setUp(self):
        """Set up a dummy pocket file for testing."""
        self.pocket_file = "test_pocket.pdb"
        with open(self.pocket_file, "w") as f:
            f.write("ATOM      1  N   ALA A   1      27.340  -2.476  34.922  1.00  0.00           N  \n")
            f.write("ATOM      2  CA  ALA A   1      28.153  -1.296  34.576  1.00  0.00           C  \n")
            f.write("ATOM      3  C   ALA A   1      27.382  -0.084  35.039  1.00  0.00           C  \n")

    def tearDown(self):
        """Clean up the dummy pocket file."""
        if os.path.exists(self.pocket_file):
            os.remove(self.pocket_file)

    @unittest.skipIf(Chem is None, "RDKit is not installed, skipping chemical tests")
    def test_evaluator_scoring(self):
        """Test the scoring functions of the Evaluator class."""
        evaluator = Evaluator(self.pocket_file)
        
        # Test with a simple molecule: benzene
        mol_benzene = Chem.MolFromSmiles("c1ccccc1")
        self.assertIsNotNone(mol_benzene)

        shape_score = evaluator.shape_score(mol_benzene)
        self.assertIsInstance(shape_score, float)
        self.assertGreaterEqual(shape_score, 0.0)

        gaussian_score = evaluator.gaussian_score(mol_benzene)
        self.assertIsInstance(gaussian_score, float)
        self.assertGreaterEqual(gaussian_score, 0.0)
        
        # Test total score which includes chemical properties
        total_score = evaluator.total_score(mol_benzene)
        self.assertIsInstance(total_score, float)
        
        # Test with another molecule: acetic acid
        mol_acetic = Chem.MolFromSmiles("CC(=O)O")
        self.assertIsNotNone(mol_acetic)
        
        total_score_acetic = evaluator.total_score(mol_acetic)
        self.assertIsInstance(total_score_acetic, float)

    @unittest.skipIf(Chem is None, "RDKit is not installed, skipping chemical tests")
    def test_ligand_state_and_action(self):
        """Test the LigandState and LigandAction classes."""
        # Initial state is empty
        initial_state = LigandState()
        self.assertIsNone(initial_state.mol)
        self.assertEqual(len(initial_state.history), 0)

        # Apply an action
        action = LigandAction(frag_smiles="C") # Methane
        new_state = initial_state.apply_action(action)
        
        self.assertIsNotNone(new_state.mol)
        self.assertEqual(new_state.to_smiles(), "C")
        self.assertEqual(len(new_state.history), 1)
        self.assertEqual(new_state.history[0], action)

        # Test cloning
        cloned_state = new_state.clone()
        self.assertEqual(cloned_state.to_smiles(), "C")
        self.assertNotEqual(id(cloned_state.mol), id(new_state.mol)) # Should be a copy

        # Apply another action to the new state
        action2 = LigandAction(frag_smiles="O") # Oxygen -> Water
        final_state = new_state.apply_action(action2)
        self.assertEqual(final_state.to_smiles(), "C.O") # CombineMols creates disconnected components
        self.assertEqual(len(final_state.history), 2)
        
        # Test terminal state
        big_mol_state = LigandState(mol=Chem.MolFromSmiles("C" * 50))
        self.assertTrue(big_mol_state.is_terminal())
        small_mol_state = LigandState(mol=Chem.MolFromSmiles("C"))
        self.assertFalse(small_mol_state.is_terminal())

    @unittest.skipIf(Chem is None, "RDKit is not installed, skipping chemical tests")
    def test_game_state_interface(self):
        """Test the LigandMCTSGameState class and its GameStateBase interface."""
        game = LigandMCTSGameState(pocket_path=self.pocket_file)

        # Test initial state
        self.assertEqual(game.getCurrentPlayer(), 1)
        self.assertFalse(game.isTerminal())
        self.assertIsInstance(game.getReward(), float)
        
        # Test getPossibleActions
        actions = game.getPossibleActions()
        self.assertIsInstance(actions, list)
        self.assertGreater(len(actions), 0)
        self.assertIsInstance(actions[0], LigandAction)

        # Test takeAction
        new_game_state = game.takeAction(actions[0])
        self.assertIsInstance(new_game_state, LigandMCTSGameState)
        self.assertNotEqual(id(game), id(new_game_state))
        self.assertNotEqual(id(game.internal_state), id(new_game_state.internal_state))
        self.assertIsNotNone(new_game_state.internal_state.mol)

        # Test reward on a non-terminal state (should be 0)
        self.assertEqual(new_game_state.getReward(), 0.0)

        # Test reward on a terminal state
        terminal_internal_state = LigandState(mol=Chem.MolFromSmiles("C" * 51), max_atoms=50)
        terminal_game_state = LigandMCTSGameState(internal_state=terminal_internal_state, pocket_path=self.pocket_file)
        self.assertTrue(terminal_game_state.isTerminal())
        reward = terminal_game_state.getReward()
        self.assertIsInstance(reward, float)
        self.assertNotEqual(reward, 0.0) # Should have a calculated score

    @unittest.skipIf(Chem is None, "RDKit is not installed, skipping chemical tests")
    def test_placeholder(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
