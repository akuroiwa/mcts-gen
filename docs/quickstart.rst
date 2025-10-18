.. _quickstart:

Quickstart
==========

This project provides a generic Monte Carlo Tree Search (MCTS) framework. Its core concept is the replacement of the Genetic Programming (GP) engine from ``chess-ant`` with a modern AI agent. While inspired by AlphaZero, it uses a simpler, decoupled approach: the standard UCT algorithm is augmented by an external AI agent that performs **Policy Pruning**—narrowing the search space by supplying a pre-filtered list of promising moves.

This guide covers how to install the package and configure it for use with an AI agent like the Gemini CLI.

Installation
------------

Standard Installation
~~~~~~~~~~~~~~~~~~~~~

The core package can be installed directly using pip:

.. code-block:: bash

   pip install mcts-gen

Installation with Game-Specific Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To include support for specific games, you can install optional dependencies (extras).

- **For Shogi support**:

  .. code-block:: bash

     pip install mcts-gen[shogi]

  This installs the ``python-shogi`` library.

- **For Chess support**:

  .. code-block:: bash

     pip install mcts-gen[chess]

  This installs the ``python-chess`` library.

Server Setup for Gemini CLI
---------------------------

To allow the Gemini agent to use the MCTS-Gen tools, you must register the server in your ``settings.json`` file. This allows the Gemini CLI to automatically manage the server process and provide the necessary context files.

Create or update your ``settings.json`` file with the following configuration:

.. code-block:: json

   {
     "context": {
       "fileName": [
         "src/mcts_gen/AGENTS.md",
         "GEMINI.md"
       ]
     },
     "mcpServers": {
       "mcts_gen_simulator_server": {
         "command": "python",
         "args": [
           "-m",
           "mcts_gen.fastmcp_server"
         ]
       }
     }
   }

**Note**: The ``context`` block tells the Gemini CLI to load ``AGENTS.md`` (and ``GEMINI.md`` if it exists), which is crucial for the agent to understand how to use the tools.

You can place this ``settings.json`` file in one of two locations:

1.  **Project-Specific**: ``./.gemini/settings.json`` (inside this project directory)
2.  **Global**: ``~/.gemini/settings.json`` (in your home directory)

For an alternative setup method using the ``fastmcp`` command-line tool, please see the official guide:

- `Gemini CLI 🤝 FastMCP <https://gofastmcp.com/integrations/gemini-cli>`_

Installation with `uv` (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For a faster and more modern package management experience, we recommend using `uv`.

1. **Install `pipx` and `uv`**:

   .. code-block:: bash

      # Install pipx (a tool to install and run Python applications in isolated environments)
      sudo apt install pipx

      # Install uv using pipx
      pipx install uv

2. **Set up the environment and install `mcts-gen`**:

   .. code-block:: bash

      # Create a virtual environment in your project directory
      uv venv

      # Activate the environment
      source .venv/bin/activate

      # Install mcts-gen with Shogi support
      uv pip install mcts-gen[shogi]

   To exit the virtual environment, simply run ``deactivate``.

3. **Configure `gemini-cli` with `fastmcp`**:

   Instead of manually editing ``settings.json``, you can use the ``fastmcp`` command to automatically configure the tool server.

   .. code-block:: bash

      fastmcp install gemini-cli .venv/lib/python3.12/site-packages/mcts_gen/fastmcp_server.py:mcp

   This command will automatically detect and configure the `mcts_gen` server, creating a ``.gemini/settings.json`` file for you.

   **Note on the ``:mcp`` suffix**: The ``:mcp`` at the end is required because ``fastmcp_server.py`` contains multiple objects. This suffix explicitly tells ``fastmcp`` which object is the MCP server instance to be run.

Agent Context Configuration with `uv`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you installed the package using `uv` or `pip`, the `AGENTS.md` file is included inside the package. To allow the Gemini agent to use it, you need to specify its full path in your `.gemini/settings.json` file.

Add the path to the `context.fileName` list. The exact path may vary depending on your Python version and environment.

**Example `.gemini/settings.json`:**

.. code-block:: json

   {
     "context": {
       "fileName": [
         ".venv/lib/python3.12/site-packages/mcts_gen/AGENTS.md",
         "GEMINI.md"
       ]
     },
     "mcpServers": {
       "mcts_gen_simulator_server": {
         "command": "uv",
         "args": [
           "run",
           "fastmcp",
           "run",
           ".venv/lib/python3.12/site-packages/mcts_gen/fastmcp_server.py:mcp"
         ]
       }
     }
   }

For Maintainers: How to Release a New Version
----------------------------------------------

The package publication process is automated using GitHub Actions.

Releasing to TestPyPI (for testing)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To release a version to the TestPyPI repository for verification, create and push a git tag with a ``-test`` suffix.

.. code-block:: bash

   # Example for version 0.1.0
   git tag v0.1.0-test1
   git push origin v0.1.0-test1

Releasing to PyPI (Official)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To perform an official release, create and push a git tag that follows the semantic versioning format (e.g., ``vX.Y.Z``).

.. code-block:: bash

   # Example for version 0.1.0
   git tag v0.1.0
   git push origin v0.1.0
