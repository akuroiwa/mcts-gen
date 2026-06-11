# Data Model: MOPAC Integration and Fragment Refactor

## Entities

### FragmentLibrary
A deduplicated collection of building blocks.
- **smiles_set**: `set[str]` - Unique SMILES strings of all available fragments.
- **fragments**: `List[Mol]` - (Transient) RDKit Mol objects generated for the current simulation.

### LigandAction
Represents the choice of a fragment to attach.
- **frag_smiles**: `str` - The unique identifier (SMILES) of the fragment.
- **attach_idx**: `Optional[int]` - Target atom index on the base molecule.
- **orientation_idx**: `int` - Index for conformational diversity.

### MopacResult
Data extracted from MOPAC execution.
- **heat_of_formation**: `float` - Energy in kcal/mol.
- **is_valid**: `bool` - True if the calculation completed successfully.
- **raw_output**: `str` - Full MOPAC log for debugging.

## State Transitions

1. **Initialization**: Load material file -> BRICS Decompose -> `set` of SMILES -> `FragmentLibrary`.
2. **Expansion**: `getPossibleActions()` -> Cross product of `FragmentLibrary.smiles_set` x `attach_idx` x `orientation_idx`.
3. **Application**: `takeAction()` -> Clone parent `Mol` -> Append fragment `Mol` (from SMILES) -> Create new `LigandState`.
4. **Evaluation**: `isTerminal()` -> Check Shape Complementarity -> If OK, call `MopacEvaluator` -> Update total reward.
