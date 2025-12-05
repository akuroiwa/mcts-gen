import pytest
from mcts_gen.fastmcp_server import mcp, mcts_autonomous_search
from fastmcp import Context
from fastmcp.prompts.prompt import PromptMessage

@pytest.mark.anyio
async def test_mcts_autonomous_search_prompt_content():
    """
    Tests that the 'mcts_autonomous_search' prompt function
    generates the correct workflow instructions by calling its render() method.
    """
    # Create a context object required by the render method
    ctx = Context(mcp)

    # A decorated prompt object is not callable directly.
    # We must use its render() method.
    messages = await mcts_autonomous_search.render({
        "goal": "test the prompt",
        "ctx": ctx
    })

    # Assert that we got messages back
    assert messages is not None
    assert isinstance(messages, list)
    assert len(messages) > 0

    # Flatten the content for easier searching
    full_content = "".join(
        msg.content.text for msg in messages if isinstance(msg, PromptMessage) and hasattr(msg.content, 'text')
    )

    # Assert that key workflow steps are in the prompt content
    assert "**Phase 1: Investigation**" in full_content
    assert "Analyze the Game Module" in full_content
    assert "Find the GameState Class" in full_content
    assert "**Phase 2: Initialization**" in full_content
    assert "Gather Arguments" in full_content
    assert "reinitialize_mcts" in full_content
    assert "**Phase 3: Execution**" in full_content
    assert "Implement a Search Loop" in full_content
    assert "get_best_move" in full_content