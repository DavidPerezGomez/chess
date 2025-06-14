import re

from domain.game.model.board import BoardState
from domain.game.model.move import Move
from domain.game.model.pieces import PieceType, Piece
from domain.game.model.square import Square
from infrastructure.notation.mapper.piece_mapper import NotationPieceMapper
from infrastructure.notation.mapper.square_mapper import NotationSquareMapper


class SANMoveMapper:

    @staticmethod
    def san_to_move(san_string: str, board_state: BoardState) -> Move | None:
        """
        Maps a Standard Algebraic Notation (https://www.chessprogramming.org/Algebraic_Chess_Notation) to a Move instance given a BoardState.
        The ACN is assumed to be valid and is not verified.
        :param san_string: the Standard Algebraic Notation
        :param board_state: the BoardState
        :return: the resulting Move
        """
        piece_move_regex = r'(N|B|R|Q|K)([a-h]|[1-8]|[a-h][1-8])?x?([a-h][1-8])'
        pawn_capture_regex = r'([a-h])([1-8])?x([a-h][1-8])(N|B|R|Q)?'
        pawn_push_regex = r'([a-h][1-8])(N|B|R|Q)?'
        short_castle_str = 'O-O'
        long_castle_str = 'O-O-O'

        if san_string == short_castle_str:
            return SANMoveMapper._generate_short_castle_move(board_state)
        elif san_string == long_castle_str:
            return SANMoveMapper._generate_long_castle_move(board_state)

        try:
            match = re.match(piece_move_regex, san_string)
            if match:
                piece = match.group(1)
                from_square = match.group(2)
                to_square = match.group(3)
                return SANMoveMapper._generate_piece_move(board_state, piece, from_square, to_square)

            match = re.match(pawn_push_regex, san_string)
            if match:
                to_square = match.group(1)
                promotion = match.group(2)
                return SANMoveMapper._generate_pawn_push_move(board_state, to_square, promotion)

            match = re.match(pawn_capture_regex, san_string)
            if match:
                from_file = match.group(1)
                from_rank = match.group(2)
                to_square = match.group(3)
                promotion = match.group(4)
                return SANMoveMapper._generate_pawn_capture_move(board_state, from_file, from_rank, to_square, promotion)
        except Exception as ex:
            print(ex)
            return None

    @staticmethod
    def _generate_short_castle_move(board_state: BoardState) -> Move:
        return Move(origin_square=Square(4, 0 if board_state.white_to_move else 7), dest_square=Square(6, 0 if board_state.white_to_move else 7))

    @staticmethod
    def _generate_long_castle_move(board_state: BoardState) -> Move:
        return Move(origin_square=Square(4, 0 if board_state.white_to_move else 7), dest_square=Square(2, 0 if board_state.white_to_move else 7))

    @staticmethod
    def _generate_piece_move(board_state: BoardState, piece_str: str, from_square_str: str|None, to_square_str: str):
        dest_square = SANMoveMapper._san_to_square(to_square_str)

        if from_square_str:
            if len(from_square_str) == 2:
                origin_square = SANMoveMapper._san_to_square(from_square_str)
            else:
                moves = board_state.get_legal_moves()
                if re.match(r'a-h', from_square_str):
                    file = NotationSquareMapper.string_to_file(from_square_str)
                    origin_square = [move.origin_square for move in moves if move.dest_square == dest_square and move.origin_square.file == file][0]
                else:
                    rank = NotationSquareMapper.string_to_rank(from_square_str)
                    origin_square = [move.origin_square for move in moves if move.dest_square == dest_square and move.origin_square.rank == rank][0]
        else:
            piece_type = NotationPieceMapper.string_to_piece_type(piece_str)
            moves = board_state.get_legal_moves()
            origin_square = [move.origin_square for move in moves if move.dest_square == dest_square and board_state.get_piece_on_square(move.origin_square).type == piece_type][0]

        return Move(origin_square=origin_square, dest_square=dest_square)

    @staticmethod
    def _generate_pawn_push_move(board_state: BoardState, to_square_str: str, promotion_str: str|None) -> Move:
        dest_square = SANMoveMapper._san_to_square(to_square_str)

        promotion_type = NotationPieceMapper.string_to_piece_type(promotion_str)
        promotion_piece = None
        if promotion_type:
            promotion_piece = Piece(type=promotion_type, is_white=board_state.white_to_move)

        moves = board_state.get_legal_moves()
        origin_square = [move.origin_square for move in moves if move.dest_square == dest_square and board_state.get_piece_on_square(move.origin_square).type == PieceType.PAWN][0]

        return Move(origin_square=origin_square, dest_square=dest_square, promotion_piece=promotion_piece)

    @staticmethod
    def _generate_pawn_capture_move(board_state: BoardState, from_file_str: str, from_rank_str: str|None, to_square_str: str, promotion_str: str) -> Move:
        dest_square = SANMoveMapper._san_to_square(to_square_str)

        promotion_type = NotationPieceMapper.string_to_piece_type(promotion_str)
        promotion_piece = None
        if promotion_type:
            promotion_piece = Piece(type=promotion_type, is_white=board_state.white_to_move)

        if from_rank_str:
            file = NotationSquareMapper.string_to_file(from_file_str)
            rank = NotationSquareMapper.string_to_rank(from_rank_str)
            origin_square = Square(file=file, rank=rank)
        else:
            moves = board_state.get_legal_moves()
            file = NotationSquareMapper.string_to_file(from_file_str)
            origin_square = [move.origin_square for move in moves if move.dest_square == dest_square and move.origin_square.file == file][0]

        en_passant = not board_state.get_piece_on_square(dest_square)

        return Move(origin_square=origin_square, dest_square=dest_square, promotion_piece=promotion_piece, en_passant=en_passant)

    @staticmethod
    def _san_to_square(san_string: str) -> Square:
        file_str = san_string[0]
        rank_str = san_string[1]

        file = NotationSquareMapper.string_to_file(file_str)
        rank = NotationSquareMapper.string_to_rank(rank_str)

        return Square(file, rank)