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
        "5. **Gather Arguments**: If the constructor requires arguments (like `pocket_path` for `ligand_mcts`), ask the user to provide the necessary information. If no arguments are needed, proceed directly.",
        "6. **Initialize Simulation**: Call the `reinitialize_mcts` tool. You must provide `state_module` (e.g., 'mcts_gen.games.ligand_mcts') and `state_class` (e.g., 'LigandMCTSGameState'). If the game requires constructor arguments, pass them in the `state_kwargs` dictionary (e.g., `{'pocket_path': '/path/to/file.pdb'}`).",

        "\n**Phase 3: Execution**",
        "7. **Execute Search Rounds**: After successful initialization, repeatedly call the `run_mcts_round` tool **one round at a time**. Your goal is to explore the search space effectively.",
        "8. **Analyze and Repeat**: After each round, examine the `simulation_stats` output. Continue calling `run_mcts_round` until the `improvement` value in the stats is consistently low or zero, or until you have run a sufficient number of rounds (e.g., 10-20). **Do not call the tool multiple times in a single turn.**",
        "9. **Get Final Result**: Once you have finished the search rounds, call `get_best_move` to retrieve the optimal move found.",
    ]
    detail = "\n".join(workflow)
    return [
        PromptMessage(role="user", content=TextContent(type="text", text=intro)),
        PromptMessage(role="user", content=TextContent(type="text", text=detail)),
    ]

# 4. Run the server
if __name__ == "__main__":
    mcp.run()