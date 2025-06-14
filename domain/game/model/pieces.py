from __future__ import annotations

from enum import Enum


class PieceType(Enum):
    PAWN = 'P'
    KNIGHT = 'N'
    BISHOP = 'B'
    ROOK = 'R'
    QUEEN = 'Q'
    KING = 'K'


class Piece:

    def __init__(self, type: PieceType, is_white: bool):
        self._type = type
        self._is_white = is_white

    def __eq__(self, other: Piece) -> bool:
        return self._type == other.type and self._is_white == other.is_white

    def __deepcopy__(self, memo=None) -> Piece:
        return Piece(type=self._type, is_white=self._is_white)

    def __hash__(self) -> int:
        return 10 * ord(self._type.value) + int(self._is_white)

    @property
    def type(self) -> PieceType:
        return self._type

    @property
    def is_white(self) -> bool:
        return self._is_white