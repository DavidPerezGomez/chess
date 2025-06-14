from __future__ import annotations

from copy import deepcopy

from domain.game.model.pieces import Piece
from domain.game.model.square import Square


class Move:

    def __init__(self,
                 origin_square: Square,
                 dest_square: Square,
                 promotion_piece: Piece = None,
                 en_passant: bool = False,
                 castle_short: bool = False,
                 castle_long: bool = False):
        self._origin_square = origin_square
        self._dest_square = dest_square
        self._promotion_piece = promotion_piece
        self._castle_short = castle_short
        self._castle_long = castle_long
        self._en_passant = en_passant

    def __deepcopy__(self, memo=None) -> Move:
        return Move(
            origin_square = deepcopy(self.origin_square),
            dest_square = deepcopy(self.dest_square),
            promotion_piece = deepcopy(self.promotion_piece),
            en_passant = self.en_passant,
            castle_short = self.castle_short,
            castle_long = self.castle_long,
        )

    def __str__(self):
        return f'{str(self.origin_square)} -> {str(self.dest_square)}'

    def __eq__(self, other: Move) -> bool:
        return self._origin_square == other.origin_square and self._dest_square == other.dest_square and self._promotion_piece == other.promotion_piece and self._en_passant == other.en_passant and self.castle_short == other.castle_short and self._castle_long == other.castle_long

    def __hash__(self) -> int:
        return 100000 * hash(self._origin_square) + 1000 * hash(self._dest_square) + 100 * int(self.castle_short) + 10 * int(self.castle_long) + int(self._en_passant)

    @property
    def origin_square(self) -> Square:
        return self._origin_square

    @property
    def dest_square(self) -> Square:
        return self._dest_square

    @property
    def promotion_piece(self) -> Piece:
        return self._promotion_piece

    @property
    def en_passant(self) -> bool:
        return self._en_passant

    @property
    def castle_short(self) -> bool:
        return self._castle_short

    @property
    def castle_long(self) -> bool:
        return self._castle_long