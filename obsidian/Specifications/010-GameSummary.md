# Spec-010: Game Summary (PGN/KIF)

## Goal
Implement `get_state_summary` for Chess and Shogi to provide full game records (PGN/KIF) in the principal variation output.

## Functional Requirements
- `ChessGameState.get_state_summary()` -> returns `pgn`.
- `ShogiGameState.get_state_summary()` -> returns `kif`.
- Integration with `get_principal_variation` tool.

## Acceptance Criteria
- Valid PGN/KIF strings generated for review in external software.
- High performance (under 100ms for 100 moves).
