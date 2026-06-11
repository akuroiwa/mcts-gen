# Research: MOPAC Integration and Fragment Management

## Decision 1: MOPAC2022 Execution Strategy

### Rationale
MOPAC2022 is an external binary. To calculate rewards, we need to generate input files, run the subprocess, and parse the results. Since the MCTS search is stateful and potentially multi-threaded (if future slots are used), we must ensure that MOPAC executions do not collide.

### Implementation Detail
- Create a dedicated `MopacEvaluator` class.
- Use `tempfile` for generating unique `.mop` and `.out` files per calculation.
- Execute via `subprocess.run` with a timeout (e.g., 5 seconds).
- Keyword: `PM7 1SCF` (PM7 Hamiltonian, One Self-Consistent Field calculation - no geometry optimization to save time and preserve RDKit conformer).

### Alternatives Considered
- **Geometry Optimization**: Let MOPAC optimize the structure. *Rejected*: Slows down the reward calculation significantly and might lead to dissociation of poorly bonded fragments.
- **RDKit-MOPAC Integration**: Use existing RDKit wrappers. *Rejected*: Often outdated or hard to configure; direct subprocess call is more reliable for MOPAC2022.

## Decision 2: Hybrid SMILES-Mol Fragment Management

### Rationale
RDKit `Mol` objects are unhashable and thus cannot be used in `set` for deduplication. SMILES strings are unique and hashable but lack 3D information.

### Implementation Detail
- **Deduplication**: Store the `fragment_library` as a `set[str]` (SMILES).
- **Action Pruning**: `LigandAction` stores the fragment SMILES. `get_possible_actions` uses this set to ensure no duplicate fragments are proposed for the same attachment point.
- **State Propagation**: `LigandState` stores the `rdkit.Chem.Mol` object. When an action is applied, we create a new `Mol` (clone), append the fragment, and generate/select conformers. This preserves 3D fidelity for MOPAC.

### Alternatives Considered
- **Mol Pickling**: Binary serialization. *Rejected*: SMILES is easier to debug and standard for fragment pool management.

## Decision 3: MOPAC Result Parsing

### Rationale
We need "FINAL HEAT OF FORMATION" from the MOPAC output.

### Implementation Detail
- Simple regex parser for the `.out` or `.arc` file.
- Look for `FINAL HEAT OF FORMATION = \s+([-+]?\d+\.\d+)`.
