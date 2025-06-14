from domain.game.model.pieces import Piece, PieceType

class ConsolePieceMapper:

    W_PAWN = '♙'
    W_KNIGHT = '♘'
    W_BISHOP = '♗'
    W_ROOK = '♖'
    W_QUEEN = '♕'
    W_KING = '♔'

    B_PAWN = '♟'
    B_KNIGHT = '♞'
    B_BISHOP = '♝'
    B_ROOK = '♜'
    B_QUEEN = '♛'
    B_KING = '♚'

    @staticmethod
    def piece_to_unicode(piece: Piece) -> str:
        if not piece:
            return ' '
        map = {
            PieceType.PAWN: lambda white: ConsolePieceMapper.W_PAWN if white else ConsolePieceMapper.B_PAWN,
            PieceType.KNIGHT: lambda white: ConsolePieceMapper.W_KNIGHT if white else ConsolePieceMapper.B_KNIGHT,
            PieceType.BISHOP: lambda white: ConsolePieceMapper.W_BISHOP if white else ConsolePieceMapper.B_BISHOP,
            PieceType.ROOK: lambda white: ConsolePieceMapper.W_ROOK if white else ConsolePieceMapper.B_ROOK,
            PieceType.QUEEN: lambda white: ConsolePieceMapper.W_QUEEN if white else ConsolePieceMapper.B_QUEEN,
            PieceType.KING: lambda white: ConsolePieceMapper.W_KING if white else ConsolePieceMapper.B_KING,
        }
        return map[piece.type](piece.is_white)

    @staticmethod
    def string_to_piece_type(string: str) -> PieceType | None:
        try:
            return PieceType(string)
        except ValueError:
            return None