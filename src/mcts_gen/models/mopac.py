from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MopacResult:
    """Represents the results parsed from a MOPAC calculation."""
    heat_of_formation: float  # Energy in kcal/mol
    is_valid: bool
    raw_output: str
    status: str = "success" # "success", "failed", "skipped"
