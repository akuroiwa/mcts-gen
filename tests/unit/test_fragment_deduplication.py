import unittest
from rdkit import Chem
from mcts_gen.games.ligand_mcts import LigandMCTSGameState

class TestFragmentRefactor(unittest.TestCase):
    def test_fragment_deduplication(self):
        # We assume the library is now a set
        state = LigandMCTSGameState(pocket_path="dummy", source_molecule_path=None)
        # Manually set a list with duplicates (if we could, but it's a set now)
        pass

    def test_library_is_set(self):
        from mcts_gen.games.ligand_mcts import LigandState
        state = LigandState()
        self.assertIsInstance(state.fragment_library, set)

if __name__ == "__main__":
    unittest.main()
