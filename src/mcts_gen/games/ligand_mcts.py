"""
This module implements the GameState for de novo ligand generation, guided
by a protein pocket point cloud.

This module is designed to be dynamically loaded by the mcts-gen framework.
It requires the user to have RDKit, SciPy, and NumPy installed.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict

import numpy as np

from mcts_gen.models.game_state import GameStateBase

# Attempt to import RDKit and SciPy, but do not fail if they are not present.
# A runtime check in the GameState constructor will handle their absence.
try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Descriptors, QED
except ImportError:
    Chem = None

try:
    from scipy.spatial import cKDTree
except ImportError:
    cKDTree = None


# --- Data Classes ---

@dataclass(frozen=True)
class LigandAction:
    """
    Represents a discrete action to modify a molecule, such as adding a chemical
    fragment. This class is immutable.

    Attributes:
        frag_smiles: The SMILES string of the fragment to add.
        attach_idx: The index of the atom on the existing molecule to connect to.
    """
    frag_smiles: str
    attach_idx: Optional[int] = None

    def __repr__(self) -> str:
        """Provides a clear string representation of the action."""
        return f"LigandAction(frag='{self.frag_smiles}', attach_at={self.attach_idx})"


@dataclass
class LigandState:
    """
    Represents the state of a partially or fully constructed molecule within the
    MCTS search.

    Attributes:
        mol: The RDKit molecule object. Can be None for the initial empty state.
        history: A list of LigandActions taken to reach this state.
        max_atoms: The number of heavy atoms at which the state is considered terminal.
    """
    mol: Optional[Any] = None
    history: List[LigandAction] = field(default_factory=list)
    max_atoms: int = 50

    def to_smiles(self) -> str:
        """Returns the SMILES representation of the current molecule."""
        if self.mol and Chem:
            return Chem.MolToSmiles(self.mol)
        return ""

    def clone(self) -> "LigandState":
        """Creates a deep copy of the current state for exploration."""
        new_mol = Chem.Mol(self.mol) if self.mol and Chem else None
        return LigandState(mol=new_mol, history=list(self.history), max_atoms=self.max_atoms)

    def is_terminal(self) -> bool:
        """Checks if the state is terminal (molecule has reached max size)."""
        if not self.mol or not Chem:
            return False
        return self.mol.GetNumAtoms() >= self.max_atoms

    def legal_actions(self) -> List[LigandAction]:
        """
        Returns a list of possible actions (fragment additions) from the current state.
        In a production system, this would come from a curated fragment library.
        """
        frags = ["C", "N", "O", "c1ccccc1", "C(=O)O"]  # Basic fragments for prototype
        actions = []
        
        if not self.mol or not Chem:
            # If there's no molecule, actions create one from a fragment.
            for frag in frags:
                actions.append(LigandAction(frag_smiles=frag))
        else:
            # This prototype attaches to the first few atoms for simplicity.
            # A more advanced implementation would use SMARTS patterns or other
            # chemistry-aware rules for determining valid attachment points.
            num_attach_points = min(4, self.mol.GetNumAtoms())
            for i in range(num_attach_points):
                for frag in frags:
                    actions.append(LigandAction(frag_smiles=frag, attach_idx=i))
        return actions

    def apply_action(self, action: LigandAction) -> "LigandState":
        """
        Applies an action to create a new molecular state.

        Returns:
            A new LigandState instance representing the state after the action.
        """
        if not Chem:
            raise RuntimeError("RDKit is not available, cannot apply action.")

        new_state = self.clone()
        frag = Chem.MolFromSmiles(action.frag_smiles)
        if not frag:
            return new_state  # Invalid fragment SMILES, return original state

        if not new_state.mol:
            # First action: the new state's molecule is just the fragment.
            new_state.mol = frag
        else:
            # NOTE: This is a simplified combination that creates a molecule with
            # two disconnected components. A production-level implementation
            # would use RDKit's reaction system to form a proper covalent bond
            # between the existing molecule and the new fragment.
            combo = Chem.CombineMols(new_state.mol, frag)
            new_state.mol = combo
        
        new_state.history.append(action)
        return new_state


# --- Utility Functions ---

def load_pocket_atm_pdb(path: str) -> np.ndarray:
    """
    Loads the 3D coordinates of atoms from a PDB file, targeting lines that
    start with "ATOM" or "HETATM".

    Args:
        path: The file path to the PDB file.

    Returns:
        A NumPy array of shape (N, 3) containing the 3D coordinates.
    """
    if not isinstance(path, str):
        raise TypeError("File path must be a string.")
    try:
        with open(path, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Pocket file not found at {path}")
        return np.array([])

    points = []
    for line in lines:
        if line.startswith(("ATOM", "HETATM")):
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                points.append([x, y, z])
            except (ValueError, IndexError):
                continue  # Ignore malformed lines
    return np.array(points)


def mol_to_points(mol: Any) -> np.ndarray:
    """
    Converts an RDKit molecule to a 3D point cloud of its heavy atoms.
    If the molecule lacks a 3D conformation, one is generated.

    Args:
        mol: The RDKit molecule object.

    Returns:
        A NumPy array of shape (N, 3) for the heavy atom coordinates.
    """
    if not Chem or not mol:
        return np.array([])

    if mol.GetNumConformers() == 0:
        mol_with_hs = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol_with_hs, AllChem.ETKDGv3())
        try:
            AllChem.UFFOptimizeMolecule(mol_with_hs)
        except Exception:
            pass  # Optimization can fail on some complex structures
        mol = Chem.RemoveHs(mol_with_hs)

    conformer = mol.GetConformer()
    points = [
        [pos.x, pos.y, pos.z]
        for atom in mol.GetAtoms()
        if atom.GetAtomicNum() > 1  # Ignore hydrogen atoms
        for pos in [conformer.GetAtomPosition(atom.GetIdx())]
    ]
    return np.array(points)


# --- Scoring Functions ---

def usr_descriptor(points: np.ndarray) -> np.ndarray:
    """
    Calculates the Ultrafast Shape Recognition (USR) descriptor for a point cloud.
    The descriptor contains the mean and standard deviation of distances from the
    centroid, providing a compact representation of the cloud's shape.

    Args:
        points: A NumPy array of shape (N, 3).

    Returns:
        A 3-element NumPy array containing [mean, std_dev, max_dist].
    """
    if points.ndim != 2 or points.shape[0] == 0:
        return np.zeros(3)
    centroid = points.mean(axis=0)
    distances = np.linalg.norm(points - centroid, axis=1)
    return np.array([distances.mean(), distances.std(), distances.max()])


def gaussian_overlap(points_a: np.ndarray, points_b: np.ndarray, sigma: float = 1.0) -> float:
    """
    Calculates the Gaussian overlap between two point clouds, a measure of
    3D shape similarity.

    Args:
        points_a: The first point cloud.
        points_b: The second point cloud.
        sigma: The width of the Gaussian.

    Returns:
        A float representing the normalized overlap score.
    """
    if points_a.size == 0 or points_b.size == 0:
        return 0.0

    if cKDTree and points_a.shape[0] * points_b.shape[0] > 100_000:
        tree = cKDTree(points_b)
        cutoff = 3.0 * sigma
        total_overlap = 0.0
        for point_a in points_a:
            indices = tree.query_ball_point(point_a, cutoff)
            if not indices:
                continue
            d_sq = np.sum((points_b[indices] - point_a) ** 2, axis=1)
            total_overlap += np.sum(np.exp(-d_sq / (2.0 * sigma**2)))
    else:
        d_sq = np.sum((points_a[:, np.newaxis, :] - points_b[np.newaxis, :, :]) ** 2, axis=2)
        total_overlap = float(np.sum(np.exp(-d_sq / (2.0 * sigma**2))))

    return total_overlap / np.sqrt(points_a.shape[0] * points_b.shape[0])


# --- Core Logic ---

class Evaluator:
    """
    Scores a molecule based on shape complementarity to a protein pocket and
    desirable chemical properties.

    Attributes:
        pocket_points: A NumPy array of the target pocket's 3D coordinates.
        pocket_usr: The USR descriptor of the target pocket.
        sigma: The sigma value for Gaussian overlap calculations.
        weights: A dictionary of weights for combining different score components.
    """

    def __init__(self, pocket_path: str, sigma: float = 1.0):
        if not pocket_path or not isinstance(pocket_path, str):
            raise ValueError("A valid pocket_path string must be provided.")
        
        self.pocket_points = load_pocket_atm_pdb(pocket_path)
        if self.pocket_points.size == 0:
            raise ValueError(f"Could not load pocket points from {pocket_path}.")

        self.pocket_usr = usr_descriptor(self.pocket_points)
        self.sigma = sigma

        self.weights = {
            "shape": 1.0,
            "gaussian": 1.0,
            "logp": -0.2,
            "qed": 2.0,
            "penalty": -1.0,
        }

    def shape_score(self, mol: Any) -> float:
        """Calculates a shape similarity score based on USR descriptors."""
        mol_points = mol_to_points(mol)
        if mol_points.size == 0:
            return 0.0
        
        mol_usr = usr_descriptor(mol_points)
        dist = np.linalg.norm(mol_usr - self.pocket_usr)
        return 1.0 / (1.0 + dist)

    def gaussian_score(self, mol: Any) -> float:
        """Calculates the 3D Gaussian overlap score."""
        mol_points = mol_to_points(mol)
        if mol_points.size == 0:
            return 0.0
        return gaussian_overlap(mol_points, self.pocket_points, self.sigma)

    def _chemical_penalties(self, mol: Any) -> float:
        """
        Calculates scores and penalties based on chemical properties (QED, LogP)
        and basic structural rules.
        """
        if not Chem or not mol:
            return self.weights.get("penalty", -1.0)
        
        try:
            if not (50 < Descriptors.ExactMolWt(mol) < 800):
                return self.weights.get("penalty", -1.0)
            
            qed_score = QED.qed(mol)
            logp_score = Descriptors.MolLogP(mol)
            
            # Penalize deviation from an ideal logP of ~2.5
            logp_penalty = self.weights.get("logp", -0.2) * abs(logp_score - 2.5)
            
            return self.weights.get("qed", 2.0) * qed_score + logp_penalty

        except Exception:
            # Catches errors from RDKit functions (e.g., sanitization)
            return self.weights.get("penalty", -1.0)

    def total_score(self, mol: Any) -> float:
        """
        Calculates the final weighted score for a molecule, combining shape,
        Gaussian overlap, and chemical property scores.
        """
        chem_score = self._chemical_penalties(mol)
        if chem_score < 0:
            return chem_score

        shape = self.shape_score(mol)
        gaussian = self.gaussian_score(mol)

        return (self.weights.get("shape", 1.0) * shape +
                self.weights.get("gaussian", 1.0) * gaussian +
                chem_score)


class LigandMCTSGameState(GameStateBase):
    """
    GameState implementation for ligand generation that fits the mcts-gen framework.
    This class orchestrates the state transitions and reward calculations for the
    ligand generation "game".

    Attributes:
        evaluator: An Evaluator instance used for scoring.
        internal_state: The LigandState object holding the current molecule.
    """
    def __init__(self, pocket_path: Optional[str] = None, internal_state: Optional[LigandState] = None, evaluator: Optional[Evaluator] = None):
        if not Chem:
            raise ImportError("RDKit is required for ligand generation but is not installed. Please run 'pip install rdkit-pypi'.")

        if evaluator:
            self.evaluator = evaluator
        else:
            if not pocket_path:
                raise ValueError("A pocket_path must be provided if an evaluator is not given.")
            self.evaluator = Evaluator(pocket_path)
        
        self.internal_state = internal_state if internal_state is not None else LigandState()

    def getCurrentPlayer(self) -> int:
        """Returns the current player. Always 1 for this single-player 'game'."""
        return 1

    def isTerminal(self) -> bool:
        """Delegates the terminal state check to the internal LigandState."""
        return self.internal_state.is_terminal()

    def getPossibleActions(self) -> List[LigandAction]:
        """Delegates action generation to the internal LigandState."""
        return self.internal_state.legal_actions()

    def takeAction(self, action: LigandAction) -> "LigandMCTSGameState":
        """
        Applies an action and returns a new game state.

        Args:
            action: The LigandAction to apply.

        Returns:
            A new LigandMCTSGameState instance representing the subsequent state.
        """
        if not isinstance(action, LigandAction):
            raise TypeError("Action must be an instance of LigandAction.")

        new_internal_state = self.internal_state.apply_action(action)
        return LigandMCTSGameState(internal_state=new_internal_state, evaluator=self.evaluator)

    def getReward(self) -> float:
        """
        Returns the reward for the current state. The reward is only calculated
        for a terminal state, otherwise it's 0.
        """
        if not self.isTerminal():
            return 0.0
        
        return self.evaluator.total_score(self.internal_state.mol)

    def __repr__(self) -> str:
        """Provides a developer-friendly representation of the game state."""
        smiles = self.internal_state.to_smiles()
        return f'LigandMCTSGameState(smiles="{smiles}")'
