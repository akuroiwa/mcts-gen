from fastmcp import FastMCP, Context
from fastmcp.prompts.prompt import PromptMessage, TextContent
from mcts_gen.services.ai_gp_simulator import AiGpSimulator

# 1. Create the core FastMCP server instance
mcp = FastMCP(
    name="mcts_gen_simulator_server"
)

# 2. Create an instance of our stateful simulator class.
#    The simulator's __init__ method will register its own methods as tools.
simulator = AiGpSimulator(mcp)

# 3. Define the built-in agent prompt using a decorator
@mcp.prompt(
    name="mcts_autonomous_search",
    description="Autonomous MCTS strategist workflow that emulates AGENTS.md content",
)
def mcts_autonomous_search(goal: str, ctx: Context) -> list[PromptMessage]:
    """
    Provides the AI with the standard workflow for running an MCTS search.
    This is the code-based version of the old AGENTS.md file.
    """
    intro = f"You are an autonomous MCTS strategist. Your goal is to find the optimal move. Task: {goal}"
    workflow = [
        "**Phase 1: Investigation**",
        "1. **Identify the Game Module**: Based on the user's request (e.g., 'ligand', 'chess'), determine the target game module file path (e.g., `src/mcts_gen/games/ligand_mcts.py`).",
        "2. **Analyze the Game Module**: Read the contents of the identified file.",
        "3. **Find the GameState Class**: Scan the file to find the class that inherits from `GameStateBase`.",
        "4. **Analyze the Constructor**: Examine the `__init__` method signature and docstring of the `GameStateBase` subclass to identify all required constructor arguments, their types, and descriptions.",

        "\n**Phase 2: Initialization**",
        "5. **Gather Arguments**: If the constructor requires arguments (like `pocket_path` for `ligand_mcts`), ask the user to provide the necessary information. For `ligand_mcts`, you should proactively estimate the `target_size` (number of heavy atoms) by analyzing the protein pocket volume. A typical drug-like ligand is 20-50 atoms.",
        "6. **Initialize Simulation**: Call the `reinitialize_mcts` tool. You must provide `state_module`, `state_class`, and `state_kwargs`.\n           - **Spatial Partitioning (Task-015):** For large protein pockets, use the `spatial_filter` argument (dict with `x_min`, `x_max`, etc.) to restrict fragment growth to a specific sub-region.\n           - **Predictive Search (Task-015):** Use the `slot_id` argument to initialize multiple searches in parallel (e.g., predicted opponent responses in Shogi/Chess).",

        "\n**Phase 3: Execution (The MCTS/GP Cycle)**",
        "Your goal is to find the best move by intelligently guiding the MCTS search. You will act like a Genetic Programming (GP) algorithm, deciding the 'Search Limit' for each stage.",
        "Follow this cycle **strictly**:",
        "",
        "1. **EXECUTE Batch**: Call `run_mcts_analysis(exploration_constant=..., num_rounds=..., actions_to_expand=...)`.",
        "   - Use `num_rounds` (e.g., 10-50) to set your 'Search Limit'.",
        "   - On subsequent rounds, use `actions_to_expand` to focus the search. You can get all possible branches via `get_possible_actions`.",
        "",
        "2. **ANALYZE Results**: The tool returns the latest `simulation_stats`.\n           - If using multiple slots, call `get_multi_slot_summary()` to compare progress.",
        "",
        "3. **DECIDE Next Step**:\n           - **Predictive Branching:** If you are confident about a future state, initialize a new `slot_id` with that state and run background analysis.\n           - **Slot Activation:** If a predicted state occurs, call `activate_mcts_slot(slot_id)` to swap contexts immediately.",
        "",
        "4. **FINALIZE**: Once the search has converged, call `get_best_move()` or `get_principal_variation()`.",
        "",
        "**CRITICAL RULE: NEVER call the same tool twice in a row in a single turn. Always analyze the output before making the next call.**",
    ]
    detail = "\n".join(workflow)
    return [
        PromptMessage(role="user", content=TextContent(type="text", text=intro)),
        PromptMessage(role="user", content=TextContent(type="text", text=detail)),
    ]

# 4. Run the server
if __name__ == "__main__":
    mcp.run()