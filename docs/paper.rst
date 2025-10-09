.. _paper:

#################################################
Paper: AI-Augmented UCT for General Game Playing
#################################################

:author: Akihiro Kuroiwa and Gemini
:date: 2025/10/03

Abstract
********

This paper introduces `mcts-gen`, a novel framework for Monte Carlo Tree Search (MCTS) that replaces the evolutionary mechanisms of Genetic Programming (GP) with a modern AI agent. We propose an architecture centered on an "AI-Augmented UCT" algorithm, where a standard UCT search is enhanced at three key points by an external AI: terminal node evaluation (Value), dynamic search parameter tuning (Exploration), and, most significantly, action space reduction via **Policy Pruning**. This approach diverges from the popular AlphaZero model by retaining the UCT algorithm's simplicity while leveraging an AI's policy model to dramatically improve performance in games with large branching factors, such as Shogi. We demonstrate a stateful client-server model where the AI agent orchestrates the entire simulation loop, iteratively refining its strategy based on real-time performance metrics.

1. Replacing Genetic Programming with an AI Agent
==================================================

In previous works like `chess-ant`, Genetic Programming was used to evolve a strategy for tuning the MCTS `explorationConstant`. This process, while effective, involved a computationally expensive evolutionary cycle with a large population and multiple generations. Each evaluation required a full MCTS simulation, leading to significant time investment.

`mcts-gen` replaces this entire evolutionary loop with a single, intelligent AI agent. The agent maintains a single strategic model (e.g., a Python function) and iteratively refines it based on direct feedback from the search process. This AI-driven, single-strategy evolution is significantly more efficient, allowing for rapid strategy adaptation without the overhead of managing a genetic population.

The core of this interaction is a stateful simulator (`AiGpSimulator`) whose methods are exposed as MCP tools. The AI agent calls these tools iteratively, managing the simulation loop externally and enabling a tight feedback cycle of execution, analysis, and self-correction.

2. Policy Pruning: An Alternative to PUCT
==========================================

AlphaZero and its derivatives integrate a policy network directly into the selection phase of MCTS via the PUCT (Polynomial Upper Confidence Trees) formula. While powerful, this tightly couples the search algorithm with the policy model.

We propose a simpler, more decoupled approach: **Policy Pruning**. The workflow is as follows:

1.  The AI agent calls a tool (`get_possible_actions`) to retrieve all legal moves from the current node.
2.  The agent applies its internal policy model to this list, filtering out unpromising moves and creating a smaller, pruned list of candidate actions.
3.  The agent then calls the main search tool (`run_mcts_round`), passing this pruned list (`actions_to_expand`) as an argument.
4.  The MCTS engine, upon receiving this list, constrains its expansion phase to only consider the actions provided by the AI.

This method effectively uses the AI's policy as a high-level filter, dramatically reducing the branching factor of the search tree, especially in complex games like Shogi. It allows the underlying engine to remain a standard UCT implementation, simplifying the architecture while still reaping the primary benefit of a policy network.

3. UCT with AI-driven Exploration
==================================

Instead of PUCT, `mcts-gen` uses the standard UCT (Upper Confidence bounds for Trees) algorithm for node selection. The key innovation lies in how the `explorationConstant` (C in the UCT formula) is determined.

-   The AI agent is responsible for generating and maintaining a strategy (e.g., a Python function) that determines the optimal `explorationConstant` for any given game state.
-   This strategy can be complex, taking into account game-specific features (e.g., `board.is_check()`) and generic simulation metrics (e.g., `improvement` of the UCT value).
-   The AI executes this strategy to choose a constant for each simulation loop and refines the strategy code based on performance, effectively learning how to best balance exploration and exploitation.

4. Other Differences from AlphaZero
====================================

-   **Decoupled Logic:** The MCTS engine and the AI "brain" are fully decoupled. The engine provides generic tools, and the AI uses them to implement its own, potentially complex, search logic.
-   **Stateful Interaction:** Unlike a stateless model, the server maintains the MCTS tree instance across multiple tool calls, allowing the AI to build upon previous search results within a single turn.
-   **Explicit Strategy:** The AI's exploration strategy is an explicit, human-readable piece of code, which can be logged and analyzed, offering greater transparency than the implicit weights of a neural network.

5. The Challenge of Game Logic Generation
==========================================

The `mcts-gen` framework is designed to be generic. This requires the creation of game-specific logic files (`*_mcts.py`) that inherit from a `GameStateBase` abstract class. This task has proven to be complex for both humans and AI agents due to the need for a deep understanding of two separate APIs: the game library (e.g., `python-shogi`) and the `GameStateBase` interface.

Our experience shows that this process is not a simple, one-shot generation. It requires iterative trial and error, debugging, and a precise understanding of concepts like object copying (`deepcopy`), return value conventions, and API-specific methods (e.g., `board.outcome()` vs. `board.is_checkmate()`).

The use of a framework like `spec-kit` is highly recommended for this process. By defining the requirements in structured markdown files (`spec.md`, `plan.md`, `tasks.md`), the AI can follow a clear, test-driven development (TDD) cycle, breaking down the complex task into manageable steps and verifying each one, which has proven essential for success.

6. Comparison with `chess-ant`'s GP Model
============================================

-   **`chess-ant`:** The Genetic Programming model in `chess-ant` relies on a large-scale evolutionary simulation. For the evaluation of each individual in the population, key instance variables used for statistics are reset, but the underlying MCTS search tree is maintained. This process, where a full MCTS simulation is run for each individual across many generations, is computationally massive.
-   **`mcts-gen`:** The AI agent replaces the entire population. It maintains a *single* strategy and iteratively improves it. The AI drives a main loop where each iteration calls the `run_mcts_round` tool. This tool executes a single MCTS round (selection, expansion, evaluation, backpropagation). The MCTS instance is preserved across these calls, allowing the search tree to grow. This is equivalent to one MCTS simulation in `chess-ant`, but the strategy refinement is done intelligently by the AI after each round, rather than through generational evolution. The result is a significantly more efficient search process, especially when combined with Policy Pruning.

7. References
==============

- **OpenSpiel (for AlphaZero Algorithm implementation details):**
  `https://github.com/google-deepmind/open_spiel <https://github.com/google-deepmind/open_spiel>`_

- **Monte-Carlo Tree Search Solver (Paper):**
  Winands, Mark & Björnsson, Yngvi & Saito, Jahn-Takeshi. (2008). Monte-Carlo Tree Search Solver. `10.1007/978-3-540-87608-3_3 <https://www.researchgate.net/publication/220962507_Monte-Carlo_Tree_Search_Solver>`_.

- **Related Projects & Libraries:**
  - `pbsinclair42/MCTS <https://github.com/pbsinclair42/MCTS>`_
  - `akuroiwa/mcts-solver <https://github.com/akuroiwa/mcts-solver>`_
  - `akuroiwa/chess-ant <https://github.com/akuroiwa/chess-ant>`_
  - `chess-ant documentation <https://chess-ant.readthedocs.io/>`_ (Contains an extensive list of references on its paper page)
  - `gunyarakun/python-shogi <https://github.com/gunyarakun/python-shogi>`_
