from domain.game.model.pieces import PieceType


class NotationPieceMapper:

    @staticmethod
    def string_to_piece_type(string: str) -> PieceType | None:
        try:
            return PieceType(string.upper())
        except ValueError:
            return None