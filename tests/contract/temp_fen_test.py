# tests/contract/temp_fen_test.py

from mcts_gen.games.chess_mcts import ChessGameState

def test_user_fen_terminality():
    user_fen = "R6k/4pprp/8/8/8/8/1B2PPPP/R6K w - - 0 1"
    state = ChessGameState(fen=user_fen)
    is_terminal = state.isTerminal()
    print(f"FEN: {user_fen}")
    print(f"Is terminal? {is_terminal}")
    assert not is_terminal # Asserting that it is NOT terminal, as expected.
