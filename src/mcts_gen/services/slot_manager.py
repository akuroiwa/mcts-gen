from typing import Dict, Optional
from ..services.mcts_engine import McpMcts

class SlotManager:
    """Manages multiple MCTS search contexts (slots)."""
    def __init__(self):
        self.slots: Dict[str, McpMcts] = {}
        self.active_slot: str = "main"

    def set_slot(self, slot_id: str, engine: McpMcts):
        """Sets or updates an engine for a specific slot."""
        self.slots[slot_id] = engine

    def get_slot(self, slot_id: str) -> Optional[McpMcts]:
        """Retrieves the engine for a specific slot."""
        return self.slots.get(slot_id)

    def activate_slot(self, slot_id: str) -> bool:
        """Swaps the active search context."""
        if slot_id in self.slots:
            self.active_slot = slot_id
            return True
        return False

    def list_slots(self) -> list[str]:
        """Returns a list of all slot identifiers."""
        return list(self.slots.keys())
