# Quickstart Guide

**Status**: Draft

This guide provides a quick overview of the key user-facing changes implemented in this feature.

---

### 1. Installation

#### Standard Installation

The core package can be installed directly using pip:
```bash
pip install mcts-gen
```

#### Installation with Game-Specific Dependencies

To include support for specific games, you can install optional dependencies (extras). For example, to install with support for Shogi:

```bash
pip install mcts-gen[shogi]
```
This will automatically install the `python-shogi` library alongside the core `mcts-gen` package.

---

### 2. FastMCP Server Setup for Gemini

To allow the Gemini agent to use the MCTS-Gen tools, you must register the FastMCP server with your Gemini CLI environment.

Create a file named `settings.json` with the following content:

```json
{
    "fastmcp_servers": [
        {
            "name": "mcts_gen",
            "path": "/path/to/your/mcts-gen/repo/fastmcp_tool.py"
        }
    ]
}
```

**Important**: Replace `/path/to/your/mcts-gen/repo/` with the absolute path to this project's root directory on your system.

You can place this `settings.json` file in one of two locations:

1.  **Project-Specific**: `./.gemini/settings.json` (inside this project directory)
2.  **Global**: `~/.gemini/settings.json` (in your home directory)

For more advanced setup options and information, please refer to the official FastMCP documentation: [https://gofastmcp.com/integrations/gemini-cli](https://gofastmcp.com/integrations/gemini-cli)

---

### 3. For Maintainers: How to Release a New Version

The package publication process is automated using GitHub Actions.

#### a) Releasing to TestPyPI (for testing)

To release a version to the TestPyPI repository for verification, create and push a git tag with a `-test` suffix.

```bash
# Example for version 0.1.0
git tag v0.1.0-test1
git push origin v0.1.0-test1
```

#### b) Releasing to PyPI (Official)

To perform an official release, create and push a git tag that follows the semantic versioning format (e.g., `vX.Y.Z`).

```bash
# Example for version 0.1.0
git tag v0.1.0
git push origin v0.1.0
```

Pushing the tag will trigger the GitHub Actions workflow, which automatically builds and publishes the new version to PyPI.

---
