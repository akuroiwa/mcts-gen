import unittest
import numpy as np
import os
import pandas as pd

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

        # Files for external source tests
        self.test_data_dir = "test_data"
        os.makedirs(self.test_data_dir, exist_ok=True)
        
        self.smiles_file = os.path.join(self.test_data_dir, "molecules.smi")
        with open(self.smiles_file, "w") as f:
            f.write("CCO\n")
            f.write("c1ccccc1\n")
            f.write("CNC(=O)c1ccc(C)cc1\n")

        self.sdf_file = os.path.join(self.test_data_dir, "molecules.sdf")
        mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O") # Aspirin
        writer = Chem.SDWriter(self.sdf_file)
        writer.write(mol)
        writer.close()

        self.csv_file = os.path.join(self.test_data_dir, "molecules.csv")
        pd.DataFrame({"smiles": ["C", "CC", "CCC"]}).to_csv(self.csv_file, index=False)

        self.malformed_smiles_file = os.path.join(self.test_data_dir, "malformed.smi")
        with open(self.malformed_smiles_file, "w") as f:
            f.write("this is not a valid smiles string\n")

    def tearDown(self):
        """Clean up the dummy pocket file."""
        if os.path.exists(self.pocket_file):
            os.remove(self.pocket_file)
        if os.path.exists(self.test_data_dir):
            import shutil
            shutil.rmtree(self.test_data_dir)

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
    def test_initialization_with_source_molecule_path(self):
        """(T003) Test initialization with a valid source_molecule_path."""
        game = LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path=self.smiles_file)
        self.assertIsInstance(game, LigandMCTSGameState)
        actions = game.getPossibleActions()
        self.assertIsInstance(actions, list)
        self.assertGreater(len(actions), 0)
        self.assertIsInstance(actions[0], LigandAction)

    @unittest.skipIf(Chem is None, "RDKit is not installed, skipping chemical tests")
    def test_molecule_parsing_from_different_formats(self):
        """(T004) Test initialization from different file formats."""
        # Test with .smi
        game_smi = LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path=self.smiles_file)
        self.assertGreater(len(game_smi.getPossibleActions()), 0)
        
        # Test with .sdf
        game_sdf = LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path=self.sdf_file)
        self.assertGreater(len(game_sdf.getPossibleActions()), 0)

        # Test with .csv
        game_csv = LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path=self.csv_file)
        self.assertGreater(len(game_csv.getPossibleActions()), 0)

    @unittest.skipIf(Chem is None, "RDKit is not installed, skipping chemical tests")
    def test_error_handling_for_invalid_paths(self):
        """(T005) Test error handling for invalid file paths and malformed files."""
        with self.assertRaises(FileNotFoundError):
            LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path="non_existent_file.smi")
        
        with self.assertRaises(ValueError):
            LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path=self.malformed_smiles_file)

    @unittest.skipIf(Chem is None, "RDKit is not installed, skipping chemical tests")
    def test_brics_fragmentation_produces_fragments(self):
        """(T006) Test that BRICS fragmentation produces a non-empty list of actions."""
        game = LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path=self.smiles_file)
        actions = game.getPossibleActions()
        self.assertGreater(len(actions), 0)

        # Check for a known fragment from Aspirin
        game_aspirin = LigandMCTSGameState(pocket_path=self.pocket_file, source_molecule_path=self.sdf_file)
        aspirin_actions = game_aspirin.getPossibleActions()
        # One possible BRICS fragment of Aspirin is the salicylic acid part.
        # This is a weak test as the SMILES can vary. A better test would be canonical smiles.
        # For now, just checking if we get a good number of fragments.
        self.assertGreater(len(aspirin_actions), 1)


if __name__ == '__main__':
    unittest.main()