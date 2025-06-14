from domain.game.model.board import BoardState
from domain.game.model.pieces import Piece
from domain.game.model.square import Square
from infrastructure.notation.mapper.piece_mapper import NotationPieceMapper
from infrastructure.notation.mapper.square_mapper import NotationSquareMapper


class EDPBoardStateMapper:

    @staticmethod
    def epd_to_board_state(epd_string: str) -> BoardState:
        """
        Maps an Extended Position Description (https://www.chessprogramming.org/Extended_Position_Description) to a BoardState instance.
        The EPD is assumed to be valid and is not verified.
        :param epd_string: the Extended Position Description
        :return: the resulting BoardState
        """
        pieces, side_to_move, castling, en_passant, *operations = epd_string.split(' ')

        squares = EDPBoardStateMapper._pieces_to_squares(pieces)
        white_to_move = EDPBoardStateMapper._side_to_move_to_white_to_move(side_to_move)
        w_castle_short, w_castle_long, b_castle_short, b_castle_long = EDPBoardStateMapper._castling_to_flags(castling)
        en_passant_target = EDPBoardStateMapper._en_passant_to_target(en_passant)

        return BoardState(squares,
                          white_to_move,
                          w_castle_short,
                          w_castle_long,
                          b_castle_short,
                          b_castle_long,
                          en_passant_target)

    @staticmethod
    def _pieces_to_squares(pieces: str) -> dict:
        squares = {}

        ranks = pieces.split('/')
        rank = 8 + 1
        for rank_str in ranks:
            rank -= 1
            if rank_str == '8':
                # empty rank
                continue

            file = 1
            for char in rank_str:
                if char.isdigit():
                    # skip empty files
                    file += int(char)
                else:
                    # add square with piece
                    if not squares.get(file):
                        squares[file] = {}
                    squares[file][rank] = char

        return squares

    @staticmethod
    def _char_to_piece(piece_char: str) -> Piece:
        piece_type = NotationPieceMapper.string_to_piece_type(piece_char)
        if not piece_type:
            raise ValueError(f"Invalid piece {piece_char}")
        is_white = not piece_char.islower()
        return Piece(piece_type, is_white)

    @staticmethod
    def _side_to_move_to_white_to_move(side_to_move: str) -> bool:
        return side_to_move == 'w'

    @staticmethod
    def _castling_to_flags(castling: str) -> tuple[bool, bool, bool, bool]:
        w_castle_short = 'K' in castling
        w_castle_long = 'Q' in castling
        b_castle_short = 'k' in castling
        b_castle_long = 'q' in castling

        return w_castle_short, w_castle_long, b_castle_short, b_castle_long

    @staticmethod
    def _en_passant_to_target(en_passant: str) -> Square | None:
        if en_passant == '-':
            return None

        file = NotationSquareMapper.string_to_file(en_passant[0])
        rank = NotationSquareMapper.string_to_rank(en_passant[1])

        return Square(file, rank)