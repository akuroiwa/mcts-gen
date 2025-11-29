# Research: Ligand MCTS Module

## Overview
This research document outlines the key technical decisions for the `ligand-mcts-module` feature. The implementation path is straightforward and relies on established libraries and the existing `mcts-gen` architecture.

## Key Decisions

### Decision 1: Use `rdkit-pypi` for Cheminformatics
- **Decision:** All chemical informatics tasks, including molecule representation, property calculation (MolLogP, QED), and structure validation (sanitization), will be handled using the `rdkit-pypi` library.
- **Rationale:** RDKit is the de-facto industry standard for cheminformatics in Python. It is robust, well-documented, and provides all the necessary functions required by the feature's `Evaluator` class. Using a single, comprehensive library simplifies the dependency chain and ensures consistency in chemical calculations.
- **Alternatives Considered:**
    - **Open Babel:** While powerful, its Python bindings can be less intuitive than RDKit's, and RDKit has broader adoption in the machine learning and data science communities.
    - **Custom Implementation:** Implementing chemical property calculations from scratch is error-prone, time-consuming, and unnecessary given the availability of high-quality libraries like RDKit.

### Decision 2: Rely on Existing Dynamic Module Loading
- **Decision:** The new `ligand_mcts.py` game module will be loaded dynamically by the `mcts-gen` framework's `AiGpSimulator` service. No changes will be made to the core framework to "register" the new module.
- **Rationale:** The investigation of `src/mcts_gen/services/ai_gp_simulator.py` revealed an existing mechanism that uses Python's `importlib` to load a game module based on string parameters (`state_module`, `state_class`) provided by the AI agent. This is a clean, decoupled architecture that fully supports the addition of new, self-contained game modules without modifying the core application. Adhering to this existing pattern is the most robust and maintainable approach.
- **Alternatives Considered:**
    - **Static Registration:** Modifying `fastmcp_server.py` or `ai_gp_simulator.py` to include a static list or dictionary of available games. This would create unnecessary coupling, require core framework modifications for every new game, and violate the apparent design intent of the application.
