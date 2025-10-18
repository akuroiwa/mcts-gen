# tests/contract/test_chess_mcts.py

import pytest

# This import will fail until T003 is complete, which is expected for TDD.
from mcts_gen.games.chess_mcts import ChessGameState

@pytest.fixture
def start_pos_fen():
    """FEN for the standard chess starting position."""
    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

@pytest.fixture
def puzzle_pos_fen():
    """A mate-in-3 puzzle position from the quickstart guide."""
    return "1r3rk1/p1p1q1pp/3b1n2/4p3/8/2N1B3/PPP1QPPP/2KR3R w - - 1 16"

def test_initialization_default():
    """Test that the board initializes to the start position by default."""
    state = ChessGameState()
    assert state.board.fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_initialization_with_fen(puzzle_pos_fen):
    """Test that the board initializes correctly from a FEN string."""
    state = ChessGameState(fen=puzzle_pos_fen)
    assert state.board.fen() == puzzle_pos_fen

def test_get_current_player(start_pos_fen, puzzle_pos_fen):
    """Test that the current player is identified correctly."""
    state_white_turn = ChessGameState(fen=start_pos_fen)
    assert state_white_turn.getCurrentPlayer() == 1  # White

    state_black_turn = state_white_turn.takeAction("e2e4")
    assert state_black_turn.getCurrentPlayer() == -1 # Black

def test_get_possible_actions(start_pos_fen):
    """Test that possible actions are returned as a list of UCI strings."""
    state = ChessGameState(fen=start_pos_fen)
    actions = state.getPossibleActions()
    assert isinstance(actions, list)
    assert len(actions) == 20 # 16 pawn moves + 4 knight moves
    assert "g1f3" in actions
    assert "e2e4" in actions

def test_take_action(start_pos_fen):
    """Test that taking an action returns a new state with the move applied."""
    state1 = ChessGameState(fen=start_pos_fen)
    move = "e2e4"
    state2 = state1.takeAction(move)

    # Verify the new state is a different object
    assert state1 is not state2
    # Verify the move was made
    assert state2.board.fen() != state1.board.fen()
    assert "e7e5" in state2.getPossibleActions()


def test_is_terminal():
    """Test terminal state detection."""
    # Non-terminal state
    non_terminal_state = ChessGameState()
    assert not non_terminal_state.isTerminal()

    # Terminal state (checkmate)
    mate_fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
    final_state = ChessGameState(fen=mate_fen)
    assert final_state.isTerminal()

def test_get_reward():
    """Test reward calculation for terminal states."""
    # Non-terminal state
    non_terminal_state = ChessGameState()
    assert non_terminal_state.getReward() == 0.0

    # White wins (black is to move but is in checkmate)
    # This FEN is confirmed from the interactive move sequence.
    white_wins_fen = "R6k/4pprp/8/8/8/8/1B2PPPP/R6K b - - 1 2"
    white_wins_state = ChessGameState(fen=white_wins_fen)
    # Since it's black's turn when the state is created, the perspective (self.color) is Black.
    # The result is a win for White ("1-0"), so from Black's perspective, the reward is -1.0.
    assert white_wins_state.getReward() == -1.0

    # Draw (stalemate)
    stalemate_fen = "8/8/8/8/8/8/5k2/7K w - - 0 1"
    stalemate_state = ChessGameState(fen=stalemate_fen).takeAction("h1h2") # Not a stalemate yet
    stalemate_state = stalemate_state.takeAction("f2f1")
    # Now it's white's turn and white has no moves. Stalemate.
    assert stalemate_state.isTerminal()
    assert stalemate_state.getReward() == 0.0

def test_to_dict(puzzle_pos_fen):
    """Test serialization to a dictionary."""
    state = ChessGameState(fen=puzzle_pos_fen)
    state_dict = state.to_dict()
    assert state_dict == {"fen": puzzle_pos_fen}
