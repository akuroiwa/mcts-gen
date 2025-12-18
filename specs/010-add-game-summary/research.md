# Research for 010-add-game-summary

## 1. How to Generate KIF from `python-shogi`

### Decision
To generate KIF (Kihu Format) strings for Shogi game states, the `shogi.KIF.Exporter` class from the `python-shogi` library will be used.

### Rationale
The `shogi.KIF.Exporter` is the idiomatic and built-in method provided by the `python-shogi` library for exporting a game's history from a `shogi.Board` object into the standard KIF format. 

The research confirmed that the `Exporter` can be initialized with a `board` object and its `export_kif()` method returns the full KIF string, including the move history. This directly and robustly satisfies the requirement (FR4) to provide a full KIF record.

Example usage:
```python
import shogi
import shogi.KIF

# Assume 'board' is a shogi.Board() object with move history
kif_exporter = shogi.KIF.Exporter(board)
kif_string = kif_exporter.export_kif()
# The kif_string is now ready to be returned in the summary.
```

This approach is significantly more reliable and simpler than manually constructing the KIF string from the move list.

### Alternatives Considered
-   **Manual KIF String Construction**: This was briefly considered. It would involve iterating through the `board.move_stack` and formatting each move into the KIF text format. This was rejected due to its complexity, high risk of formatting errors, and the fact that the library already provides a dedicated, reliable solution.

---

## 2. How to Generate PGN from `python-chess`

### Decision
To generate PGN strings for Chess game states, the `chess.pgn.Game.from_board()` method, in combination with a `chess.pgn.StringExporter`, will be used.

### Rationale
The `python-chess` library provides a comprehensive `pgn` module for this purpose. The standard approach is to create a `Game` object from the board's history and then use a `StringExporter` to write it out.

Example usage:
```python
import chess.pgn

# Assume 'board' is a chess.Board() object with move history
game = chess.pgn.Game.from_board(board)
pgn_string = str(game) 
# The pgn_string is now ready to be returned.
```

This directly satisfies requirement FR2.

### Alternatives Considered
- None, as this is the standard and recommended method provided by the library.
