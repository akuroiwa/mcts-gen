import os
import subprocess
import tempfile
import re
import sys
from typing import Optional
from rdkit import Chem
from ..models.mopac import MopacResult

class MopacEvaluator:
    """Handles execution of MOPAC2022 and parsing of its results."""
    
    def __init__(self, mopac_path: str = "mopac"):
        self.mopac_path = mopac_path

    def _mol_to_mopac_input(self, mol: Chem.Mol, keywords: str = "PM7 1SCF") -> str:
        """Converts an RDKit Mol object to a MOPAC input string (XYZ format)."""
        if mol.GetNumConformers() == 0:
            # Generate a 3D conformation if none exists
            from rdkit.Chem import AllChem
            mol = Chem.AddHs(mol)
            AllChem.EmbedMolecule(mol, AllChem.ETKDG())
            mol = Chem.RemoveHs(mol)

        conf = mol.GetConformer()
        lines = [keywords, "MCTS-Gen generated molecule", ""]
        
        for atom in mol.GetAtoms():
            pos = conf.GetAtomPosition(atom.GetIdx())
            symbol = atom.GetSymbol()
            # MOPAC input format: Symbol x flag y flag z flag
            # flag 1 means optimize, flag 0 means fixed. We use 1SCF, so flag doesn't matter much but we set 1.
            lines.append(f"{symbol:<2} {pos.x:>10.5f} 1 {pos.y:>10.5f} 1 {pos.z:>10.5f} 1")
        
        return "\n".join(lines) + "\n"

    def evaluate(self, mol: Chem.Mol, timeout: int = 5) -> MopacResult:
        """Runs MOPAC on the given molecule and returns the parsed result."""
        if not mol or mol.GetNumAtoms() == 0:
            return MopacResult(heat_of_formation=0.0, is_valid=False, raw_output="Empty molecule", status="failed")

        input_str = self._mol_to_mopac_input(mol)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.mop")
            output_file = os.path.join(tmpdir, "input.out")
            
            with open(input_file, "w") as f:
                f.write(input_str)
            
            try:
                # Run MOPAC
                result = subprocess.run(
                    [self.mopac_path, "input.mop"],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                
                if not os.path.exists(output_file):
                    return MopacResult(
                        heat_of_formation=0.0, 
                        is_valid=False, 
                        raw_output=result.stderr or "Output file not generated", 
                        status="failed"
                    )
                
                with open(output_file, "r") as f:
                    output_text = f.read()
                
                # Parse Heat of Formation
                # Typical line: FINAL HEAT OF FORMATION =         -123.45678 KCAL/MOL =     -516.54321 KJ/MOL
                match = re.search(r"FINAL HEAT OF FORMATION\s+=\s+(-?\d+\.\d+)\s+KCAL/MOL", output_text)
                if match:
                    hof = float(match.group(1))
                    return MopacResult(heat_of_formation=hof, is_valid=True, raw_output=output_text, status="success")
                else:
                    return MopacResult(
                        heat_of_formation=0.0, 
                        is_valid=False, 
                        raw_output=output_text, 
                        status="failed"
                    )
                    
            except subprocess.TimeoutExpired:
                return MopacResult(heat_of_formation=0.0, is_valid=False, raw_output="Timed out", status="failed")
            except Exception as e:
                return MopacResult(heat_of_formation=0.0, is_valid=False, raw_output=str(e), status="failed")
