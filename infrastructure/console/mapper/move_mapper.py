from domain.game.model.move import Move
from domain.game.model.pieces import Piece
from infrastructure.console.mapper.square_mapper import ConsoleSquareMapper


class ConsoleMoveMapper:

    @staticmethod
    def move_to_string(move: Move) -> str:
        return '{}->{}'.format(
            ConsoleSquareMapper.square_to_string(move.origin_square),
            ConsoleSquareMapper.square_to_string(move.dest_square))

    @staticmethod
    def piece_to_string(piece: Piece) -> str:
        piece_str = piece.type.value
        if piece.is_white:
            piece_str = piece_str.lower()
        return piece_str