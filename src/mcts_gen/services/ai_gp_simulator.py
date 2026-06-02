
import importlib
import sys
# import math
from typing import Dict, Any, List

from fastmcp import FastMCP

from ..services.mcts_engine import McpMcts
from ..services.slot_manager import SlotManager
from ..models.spatial import SpatialZone
# from ..models.game_state import GameStateBase

class AiGpSimulator:
    """
    A stateful simulator that encapsulates an MCTS engine and provides a set of
    generic, game-agnostic tools for an AI agent.
    """
    def __init__(self, mcp_instance: FastMCP):
        self.mcp = mcp_instance
        self.slots = SlotManager()
        self.simulation_state: Dict[str, Any] = {}
        self._reset_simulation_state()

        self.mcp.tool(self.reinitialize_mcts)
        self.mcp.tool(self.run_mcts_round)
        self.mcp.tool(self.get_best_move)
        self.mcp.tool(self.get_simulation_stats)
        self.mcp.tool(self.get_possible_actions)
        self.mcp.tool(self.get_principal_variation)
        self.mcp.tool(self.run_mcts_analysis)
        self.mcp.tool(self.activate_mcts_slot)
        self.mcp.tool(self.list_mcts_slots)
        self.mcp.tool(self.get_multi_slot_summary)

    @property
    def engine(self) -> McpMcts | None:
        """Dynamically retrieves the engine from the active slot."""
        return self.slots.get_slot(self.slots.active_slot)

    @engine.setter
    def engine(self, value: McpMcts):
        """Updates the engine for the active slot."""
        self.slots.set_slot(self.slots.active_slot, value)

    def _reset_simulation_state(self):
        """Resets the state variables for a single evaluation run."""
        self.simulation_state = {
            'eaten': 0.0,
            'previous_eaten': 0.0,
            'improvement': 0,
        }

    def reinitialize_mcts(self, state_module: str, state_class: str, state_kwargs: Dict[str, Any] = {}, iteration_limit: int = 100, slot_id: str = "main", spatial_filter: Dict[str, float] | None = None) -> Dict[str, Any]:
        """
        Starts a new MCTS simulation for a given game.
        
        Args:
            state_module: The python module containing the GameState class.
            state_class: The name of the GameState class.
            state_kwargs: Keyword arguments for the GameState constructor.
            iteration_limit: Search budget for the engine.
            slot_id: Identifier for the search context (defaults to "main").
            spatial_filter: Optional coordinate range (x_min, x_max, etc.) for ligand games.
        """
        try:
            # Handle Spatial Filtering (Task-015)
            if spatial_filter:
                zone = SpatialZone(**spatial_filter)
                state_kwargs['spatial_zone'] = zone

            module = importlib.import_module(state_module)
            game_class = getattr(module, state_class)
            initial_state = game_class(**state_kwargs)
            
            new_engine = McpMcts(initial_state=initial_state, iterationLimit=iteration_limit)
            self.slots.set_slot(slot_id, new_engine)
            self.slots.active_slot = slot_id
            
            self._reset_simulation_state()
            return {"status": f"MCTS re-initialized successfully in slot '{slot_id}'."}
        except Exception as e:
            return {"error": f"Failed to re-initialize MCTS: {e}"}

    def activate_mcts_slot(self, slot_id: str) -> Dict[str, Any]:
        """Swaps the active search context to a previously initialized slot."""
        if self.slots.activate_slot(slot_id):
            return {"status": f"Active slot changed to '{slot_id}'."}
        return {"error": f"Slot '{slot_id}' not found."}

    def list_mcts_slots(self) -> Dict[str, Any]:
        """Returns a list of all initialized search contexts."""
        return {"slots": self.slots.list_slots(), "active_slot": self.slots.active_slot}

    def run_mcts_round(self, exploration_constant: float, actions_to_expand: List[str] | None = None) -> Dict[str, Any]:
        """Executes a single MCTS round and updates the simulation state."""
        if not self.engine:
            return {"error": "MCTS engine not initialized."}

        self.simulation_state['previous_eaten'] = self.simulation_state['eaten']
        
        if actions_to_expand:
            # Perform string-based lookup to find the actual action objects
            try:
                real_actions = self.engine.root.state.getPossibleActions()
                action_map = {str(action): action for action in real_actions}
                actions_to_pass_to_engine = [action_map[s] for s in actions_to_expand if s in action_map]
                
                # Check for unmatched action strings to provide feedback to the AI
                unmatched = [s for s in actions_to_expand if s not in action_map]
                if unmatched:
                    sys.stderr.write(f"\n[Warning] The following actions in `actions_to_expand` were not recognized: {unmatched}\n")
                    sys.stderr.write(f"[Info] Legal action strings are: {[str(a) for a in real_actions]}\n\n")

                # If no actions matched, fallback to None to allow search to proceed (though not pruned)
                self.engine.pruned_actions = actions_to_pass_to_engine if actions_to_pass_to_engine else None
            except Exception as e:
                return {"error": f"Failed to process actions_to_expand: {e}"}
        else:
            self.engine.pruned_actions = None


        # --- MCTS 1-Round Logic ---
        node = self.engine.selectNode_num(self.engine.root, exploration_constant)
        reward = self.engine.mctsSolver(node)
        self.engine.backpropogate(node, reward)
        # --- End of 1-Round Logic ---

        # --- State Update Logic ---
        if self.engine.root.children:
            best_child = self.engine.getBestChild(self.engine.root, 0) # Use 0 exploration for pure exploitation
            if best_child and best_child.numVisits > 0:
                self.simulation_state['eaten'] = best_child.totalReward / best_child.numVisits
            else:
                self.simulation_state['eaten'] = 0.0
        else:
            self.simulation_state['eaten'] = 0.0

        if self.simulation_state['eaten'] > self.simulation_state['previous_eaten']:
            self.simulation_state['improvement'] = 2
        elif self.simulation_state['eaten'] == self.simulation_state['previous_eaten']:
            self.simulation_state['improvement'] = 1
        else:
            self.simulation_state['improvement'] = 0

        return {
            "status": "1 round executed.",
            "root_visits": self.engine.root.numVisits,
            "simulation_stats": self.simulation_state
        }

    def run_mcts_analysis(self, exploration_constant: float, num_rounds: int = 10, actions_to_expand: List[str] | None = None) -> Dict[str, Any]:
        """
        Executes a batch of MCTS rounds to improve search precision.
        This provides a 'searchLimit' functionality within a single tool call.
        
        Args:
            exploration_constant: MCTS exploration factor.
            num_rounds: Number of rounds to execute in this batch.
            actions_to_expand: Optional list of actions to focus the search on.
        """
        if not self.engine:
            return {"error": "MCTS engine not initialized."}

        for _ in range(num_rounds):
            self.run_mcts_round(exploration_constant, actions_to_expand)
        
        return {
            "status": f"Successfully executed a batch of {num_rounds} rounds.",
            "total_root_visits": self.engine.root.numVisits,
            "simulation_stats": self.simulation_state
        }

    def get_best_move(self) -> Dict[str, Any]:
        """Retrieves the best move found so far."""
        if not self.engine or not self.engine.root.children:
            return {"error": "No search performed yet."}
        best_child = self.engine.getBestChild(self.engine.root, 0)
        for action, node in self.engine.root.children.items():
            if node is best_child:
                return {"best_move": str(action)}
        return {"error": "Could not determine best move."}

    def get_simulation_stats(self) -> Dict[str, Any]:
        """Returns the current state of the simulation variables."""
        return self.simulation_state

    def get_possible_actions(self) -> Dict[str, Any]:
        """Retrieves the list of all possible actions from the current root state."""
        if not self.engine:
            return {"error": "MCTS engine not initialized."}
        try:
            actions = self.engine.root.state.getPossibleActions()
            # Return string representations to the AI agent
            return {"possible_actions": [str(a) for a in actions]}
        except Exception as e:
            return {"error": f"Failed to get possible actions: {e}"}

    def get_principal_variation(self) -> Dict[str, Any]:
        """
        Retrieves the principal variation (best sequence of moves) from the root.
        """
        if not self.engine or not self.engine.root:
            return {"error": "MCTS engine not initialized."}

        path = []
        node = self.engine.root
        while node.children:
            best_child = self.engine.getBestChild(node, 0)
            if not best_child:
                break
            
            found_action = None
            for action, child_node in node.children.items():
                if child_node is best_child:
                    found_action = action
                    break
            
            if found_action:
                path.append(str(found_action))
                node = best_child
            else:
                # Should not happen if best_child is found
                break
        
        final_state = node.state
        final_score = node.totalReward / node.numVisits if node.numVisits > 0 else 0
        
        summary = final_state.get_state_summary()
        
        # Include spatial zone metadata if it's a ligand game (Task-015)
        if hasattr(final_state, 'evaluator') and final_state.evaluator.spatial_zone:
            zone = final_state.evaluator.spatial_zone
            summary["spatial_zone"] = {
                "x_min": zone.x_min, "x_max": zone.x_max,
                "y_min": zone.y_min, "y_max": zone.y_max,
                "z_min": zone.z_min, "z_max": zone.z_max
            }

        return {
            "principal_variation": path,
            "final_score": final_score,
            "final_state_summary": summary
        }

    def get_multi_slot_summary(self) -> Dict[str, Any]:
        """Summarizes the best results from all search slots."""
        summary = {}
        original_slot = self.slots.active_slot
        
        for slot_id in self.slots.list_slots():
            self.slots.activate_slot(slot_id)
            res = self.get_principal_variation()
            if "error" not in res:
                summary[slot_id] = {
                    "score": res["final_score"],
                    "smiles": res["final_state_summary"].get("smiles"),
                    "pv_length": len(res["principal_variation"])
                }
        
        self.slots.activate_slot(original_slot)
        return {"slot_summaries": summary}

