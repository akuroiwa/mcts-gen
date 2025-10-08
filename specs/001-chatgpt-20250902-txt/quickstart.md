# Quickstart Guide

This guide explains how to use the Generic MCTS Framework in its two primary modes: Local Execution and Client-Server.

## Overview

The framework is designed for flexibility:

1.  **Local Execution**: Use the MCTS engine as a Python library directly within your scripts. Ideal for simple simulations, testing, or integration into a single application.
2.  **Client-Server Mode**: Run the MCTS engine as a persistent Web API service. Ideal for web frontends, multi-client applications, or providing "MCTS as a Service".

---

## Mode 1: Local Execution

### 1. Define Your Game

Create a Python file (e.g., `mygame_mcts.py`) and define a class that inherits from `GameStateBase`. The AI agent can also be prompted to generate this file for you.

```python
# mygame_mcts.py
# Option A: Manually include GameStateBase
from abc import ABC, abstractmethod

class GameStateBase(ABC):
    # ... (full abstract class definition) ...

class MyGameState(GameStateBase):
    def __init__(self):
        # ... your game's constructor ...

    # ... implement all abstract methods ...
```

### 2. Run a Search

Use the `McpMcts` class in your Python script to run a search.

```python
from mcp_mcts_server import McpMcts, AntLionTreeNode # Assuming these are the class names
from mygame_mcts import MyGameState

# 1. Initialize
initial_state = MyGameState()
mcts_engine = McpMcts(iterationLimit=1000)
mcts_engine.root = AntLionTreeNode(initial_state, None)

# 2. Run search loop
for _ in range(1000):
    mcts_engine.executeRound(explorationConstant=1.4)

# 3. Get best move
best_child = mcts_engine.getBestChild(mcts_engine.root, 0.0)
best_action = next(a for a, n in mcts_engine.root.children.items() if n is best_child)

print(f"Best action: {best_action}")
```

### 3. Interactive REPL

Use the `mcp_repl.py` script for interactive sessions. First, create a `config.json`:

```json
{
  "state_module": "mygame_mcts",
  "state_class": "MyGameState",
  "iterationLimit": 1000,
  "explorationConstant": 1.4
}
```

Then run the REPL:

```bash
python mcp_repl.py
>> step 1000
>> best
Best action: ...
>> quit
```

---

## Mode 2: Client-Server

### 1. Start the Server

Run the FastAPI server from your terminal.

```bash
# AUTH_ENABLED=false is the default for local runs
uvicorn mcp_api_server:app --reload --port 8000
```

### 2. Interact via API

You can use tools like `curl` or any HTTP client to interact with the server.

**Initialize the game:**
```bash
curl -X POST http://localhost:8000/init -H "Content-Type: application/json" -d '
{
  "state_module": "mygame_mcts",
  "state_class": "MyGameState"
}'
```

**Run 100 search steps:**
```bash
curl -X POST http://localhost:8000/step -H "Content-Type: application/json" -d '
{
  "n": 100,
  "exploration": 1.4
}'
```

**Get the best move:**
```bash
curl http://localhost:8000/best
```

### 3. Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Initialize
requests.post(f"{BASE_URL}/init", json={
    "state_module": "mygame_mcts",
    "state_class": "MyGameState"
})

# Provide AI prediction
requests.post(f"{BASE_URL}/prediction", json={
    "policy": {"move1": 0.8, "move2": 0.2},
    "value": 0.75
})

# Run search
requests.post(f"{BASE_URL}/step", json={"n": 100})

# Get result
response = requests.get(f"{BASE_URL}/best")
print(response.json())
```

---

## AI-Powered Code Generation

The AI agent is capable of generating the necessary game logic files for you.

- **Action**: Ask the AI to "create a game environment for [Your Game Name]".
- **`spec-kit`**: For complex games, the AI should prompt you to use `spec-kit` to better define the game rules and requirements before generating the code. This ensures the generated code is accurate.
- **Output**: The AI will provide the `*_mcts.py` file and a corresponding `config.json` file, ready to be used with the local REPL or the API server.
