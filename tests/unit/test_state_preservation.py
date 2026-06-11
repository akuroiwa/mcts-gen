import unittest
from rdkit import Chem
from rdkit.Chem import AllChem
from mcts_gen.games.ligand_mcts import LigandState

class TestStatePreservation(unittest.TestCase):
    def test_mol_clone_preserves_coords(self):
        mol = Chem.MolFromSmiles("C")
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol)
        conf = mol.GetConformer()
        original_pos = conf.GetAtomPosition(0)
        new_mol = Chem.Mol(mol)
        new_pos = new_mol.GetConformer().GetAtomPosition(0)
        self.assertEqual(original_pos.x, new_pos.x)

if __name__ == "__main__":
    unittest.main()
