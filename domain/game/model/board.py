from __future__ import annotations
from copy import deepcopy
from math import copysign
from typing import Generator

from domain.game.model.pieces import Piece, PieceType
from domain.game.model.move import Move
from domain.game.model.square import Square


class BoardState:
    MAX_FILE = 7
    MIN_FILE = 0
    MAX_RANK = 7
    MIN_RANK = 0

    def __init__(self, squares: dict[int, dict[int, Piece]],
                 white_to_move: bool = True,
                 w_castle_short: bool = True,
                 w_castle_long: bool = True,
                 b_castle_short: bool = True,
                 b_castle_long: bool = True,
                 en_passant_target: Square = None):
        """
        Constructor
        :param squares: nested dictionary where the first key represent a file (column) and the second key represents a rank (row), with the value being the piece present in that square. Only squares with pieces are stored.
        :param white_to_move: True if it's white's turn to move, False otherwise
        :param w_castle_short: True if white can castle on the king's side, False otherwise
        :param w_castle_long: True if white can castle on the queen's side, False otherwise
        :param b_castle_short: True if black can castle on the king's side, False otherwise
        :param b_castle_long: True if black can castle on the queen's side, False otherwise
        """
        self._squares: dict[int, dict[int, Piece]] = squares
        self._white_to_move: bool = white_to_move
        self._w_castle_short: bool = w_castle_short
        self._w_castle_long: bool = w_castle_long
        self._b_castle_short: bool = b_castle_short
        self._b_castle_long: bool = b_castle_long
        self._en_passant_target: Square = en_passant_target

        self._is_check = None
        self._legal_moves = None

    def __deepcopy__(self, memo=None) -> BoardState:
        """
        Creates an identical copy of this BoardState
        :return: the copied BoardState
        """
        copy = BoardState(
            squares = deepcopy(self._squares),
            white_to_move = self._white_to_move,
            w_castle_short = self._w_castle_short,
            w_castle_long = self._w_castle_long,
            b_castle_short = self._b_castle_short,
            b_castle_long = self._b_castle_long,
            en_passant_target = self._en_passant_target
        )

        return copy

    @property
    def white_to_move(self):
        return self._white_to_move

    def get_legal_moves(self) -> list[Move]:
        """
        Calculates all the possible moves in the position
        :return: generator of possible moves
        """
        if self._legal_moves is not None:
            return self._legal_moves

        if not self.is_game_over():
            legal_moves = list(self._get_all_legal_moves())
        else:
            legal_moves = []

        self._legal_moves = legal_moves
        return legal_moves

    def get_legal_moves_for_piece_in_square(self, square: Square) -> Generator[Move]:
        """
        Returns all the legal moves for the piece on the given square
        :param square: square of the piece
        :return: generator of legal moves
        """
        piece = self.get_piece_on_square(square)
        moves = self._get_all_moves_for_piece(piece, square)
        for move in moves:
            if self._move_is_legal(move):
                yield move

    def perform_move(self, move: Move, update: bool = False) -> BoardState:
        """
        Performs the specified move in the position, returning the resulting position or modifying the current one
        :param move: the move to perform
        :param update: if True, the current instance is modified. Otherwise, a new BoardState instance is created and returned. Defaults to False.
        :return: the resulting BoardState
        """
        if not update:
            copy = deepcopy(self)
            return copy.perform_move(move, update=True)

        # move the piece
        piece = self.get_piece_on_square(move.origin_square)

        piece_to_set = piece if not move.promotion_piece else move.promotion_piece
        self._remove_piece(move.origin_square)
        self._set_piece(piece_to_set, move.dest_square)

        # check for en passant
        if move.en_passant:
            direction = -1 if self._white_to_move else 1
            pawn_square = move.dest_square.move(0, direction)
            self._remove_piece(pawn_square)

        # check for castling
        if move.castle_long or move.castle_short:
            direction = -1 if move.castle_long else 1
            # find the rook
            rook = None
            rook_square = None
            next_square = move.origin_square
            while not rook_square:
                next_square = next_square.move(direction, 0)
                if self.is_in_bounds(next_square):
                    rook = self.get_piece_on_square(next_square)
                    if rook and rook.type == PieceType.ROOK and rook.is_white == self._white_to_move:
                        rook_square = next_square
                else:
                    break

            if rook_square:
                # move the rook
                new_rook_square = move.dest_square.move(-direction, 0)
                self._remove_piece(rook_square)
                self._set_piece(rook, new_rook_square)

        # check for pawn double move
        if piece.type == PieceType.PAWN and abs(move.origin_square.rank - move.dest_square.rank) == 2:
            en_passant_square = move.dest_square.move(0, int(copysign(1, move.origin_square.rank - move.dest_square.rank)))
            self._en_passant_target = en_passant_square
        else:
            self._en_passant_target = None

        # check castling flags
        if piece.type == PieceType.KING:
            if self._white_to_move:
                self._w_castle_long = False
                self._w_castle_short = False
            else:
                self._b_castle_long = False
                self._b_castle_short = False

        if piece.type == PieceType.ROOK:
            if move.origin_square.file > (BoardState.MAX_FILE - BoardState.MIN_FILE) / 2:
                if self._white_to_move:
                    self._w_castle_short = False
                else:
                    self._b_castle_short = False
            else:
                if self._white_to_move:
                    self._w_castle_long = False
                else:
                    self._b_castle_long = False

        # alternate turn
        self._white_to_move = not self._white_to_move

        self._reset_calculations()
        return self

    def get_all_pieces(self) -> Generator[tuple[Piece, Square]]:
        """
        :return: a generator of tuples with all the pieces on the board and the squares they occupy
        """
        for file in self._squares.keys():
            for rank in self._squares[file].keys():
                try:
                    piece = self._squares[file][rank]
                    square = Square(file=file, rank=rank)
                    yield piece, square
                except KeyError:
                    continue

    def get_all_pieces_by_color(self, white: bool) -> Generator[tuple[Piece, Square]]:
        """
        Returns all the white or back pieces on the board
        :param white: True to return the white pieces, False for black
        :return: a generator of tuples with all the pieces on the board and the squares they occupy
        """
        for file in self._squares.keys():
            for rank in self._squares[file].keys():
                try:
                    piece = self._squares[file][rank]
                    if piece.is_white == white:
                        square = Square(file=file, rank=rank)
                        yield piece, square
                except KeyError:
                    continue

    def get_piece_on_square(self, square: Square) -> Piece | None:
        """
        Returns the piece (if any) on the given square
        :param square: the square
        :return: the piece, or None if there is no piece on the square
        """
        try:
            return self._squares[square.file][square.rank]
        except KeyError:
            return None

    def square_is_under_attack(self, square: Square, white: bool) -> bool:
        """
        Calculates if a given square is threatened by a piece of the given color
        :param square: the square
        :param white: True for the white pieces, False for black pieces
        :return: True if the square is under attack
        """
        for piece_type in [PieceType.PAWN, PieceType.QUEEN, PieceType.KNIGHT]:
            test_piece = Piece(piece_type, not white)
            test_moves = self._get_all_moves_for_piece(test_piece, square)
            for move in test_moves:
                capture_piece = self.get_piece_on_square(move.dest_square)
                if capture_piece:
                    if capture_piece.type == piece_type:
                        return True
                    if piece_type == PieceType.QUEEN:
                        if capture_piece.type in [PieceType.BISHOP, PieceType.ROOK]:
                            return True
                        if capture_piece.type == PieceType.KING:
                            if abs(move.dest_square.file - move.origin_square.file) <= 1 and abs(move.dest_square.rank - move.origin_square.rank) <= 1:
                                return True

        return False

    def is_game_over(self) -> bool:
        """
        Calculates if the position is a game over for any reason
        :return: True if the game is over, False otherwise
        """
        return not self._has_legal_moves() or self.cant_checkmate()

    def is_in_check(self) -> bool:
        """
        Calculates if the active player is in check in the position
        :return: True if the king is in check
        """
        if self._is_check is not None:
            return self._is_check

        check = self._is_in_check(self._white_to_move)

        self._is_check = check
        return check

    def is_checkmate(self) -> bool:
        """
        Calculates if the position is checkmate
        :return: True if it's checkmate, False otherwise
        """
        return self.is_in_check() and not self._has_legal_moves()

    def is_stalemate(self) -> bool:
        """
        Calculates if the position is a stalemate
        :return: True if stalemated, False otherwise
        """
        return not self._has_legal_moves() and not self.is_in_check()

    def cant_checkmate(self) -> bool:
        """
        Calculates if the position is a draw due to the inability of either player to deliver checkmate
        :return: True if checkmate is impossible, False otherwise
        """
        w_pieces = [tuple[0] for tuple in self.get_all_pieces_by_color(white=True)]
        b_pieces = [tuple[0] for tuple in self.get_all_pieces_by_color(white=False)]

        return not self._pieces_can_checkmate(w_pieces) and not self._pieces_can_checkmate(b_pieces)

    def _get_all_legal_moves(self) -> Generator[Move]:
        """
        Calculates all the possible moves in the position ignoring game-overs
        :return: generator of possible moves
        """
        pieces = self.get_all_pieces_by_color(self._white_to_move)

        for piece, square in pieces:
            yield from self.get_legal_moves_for_piece_in_square(square)

    def _set_piece(self, piece: Piece, square: Square):
        """
        Sets a piece in the given square, overriding any piece that might already be there.
        :param piece: the piece
        :param square: the square
        """
        if self._squares.get(square.file) is None:
            self._squares[square.file] = {}

        self._squares[square.file][square.rank] = piece

    def _remove_piece(self, square: Square):
        """
        Removes the piece (if any) from the given square.
        :param square: the square
        """
        del self._squares[square.file][square.rank]
        if not self._squares[square.file]:
            del self._squares[square.file]

    def _is_in_check(self, white: bool) -> bool:
        """
        Calculates if a given king is in check in the position
        :param white: True for the white king, False for black
        :return: True if the king is in check
        """
        square = self._get_king_square(white)

        return self.square_is_under_attack(square, not white)

    def _get_king_square(self, white: bool) -> Square:
        """
        Returns the square occupied by the king of the specified color
        :param white: True for the white king, False for black
        :return: the square
        """
        pieces = self.get_all_pieces_by_color(white)
        for piece, square in pieces:
            if piece.type == PieceType.KING:
                return square

    def _has_legal_moves(self) -> bool:
        """
        Calculates if the position has possible moves
        :return: True if the player has possible moves
        """
        try:
            next(self._get_all_legal_moves())
            return True
        except StopIteration:
            return False

    def _move_is_legal(self, move: Move) -> bool:
        """
        Checks if a move is legal in the position.
        :param move: the move to check
        :return: True if the move is legal, False otherwise
        """
        # check for castling crossing attacked square
        if move.castle_long or move.castle_short:
            direction = 1 if move.dest_square.file >= move.origin_square.file else -1
            i = 1
            intermediate_square = Square(
                                    move.origin_square.file + i * direction,
                                    move.dest_square.rank)

            while intermediate_square != move.dest_square:
                if self.square_is_under_attack(intermediate_square, not self._white_to_move):
                    return False
                i += 1
                intermediate_square = Square(
                    move.origin_square.file + i * direction,
                    move.dest_square.rank)

        new_position = self.perform_move(move, update=False)
        return not new_position._is_in_check(self._white_to_move)

    def _get_all_moves_for_piece(self, piece: Piece, square: Square) -> Generator[Move]:
        """
        Returns all the moves for a piece of the given type on the given square
        :param piece: piece type
        :param square: square of the piece
        :return: generator of all moves
        """
        fn_map = {
            PieceType.PAWN: self._get_all_moves_for_pawn,
            PieceType.KNIGHT: self._get_all_moves_for_knight,
            PieceType.BISHOP: self._get_all_moves_for_bishop,
            PieceType.ROOK: self._get_all_moves_for_rook,
            PieceType.QUEEN: self._get_all_moves_for_queen,
            PieceType.KING: self._get_all_moves_for_king,
        }
        function = fn_map[piece.type]

        yield from function(square, piece.is_white)

    def _get_all_moves_for_pawn(self, origin_square: Square, is_white: bool) -> Generator[Move]:
        """
        Calculates all moves for a pawn of the given color in the given square
        :param origin_square: square that the pawn occupies
        :param is_white: True if the pawn is white, False otherwise
        :return: generator of all moves for the pawn
        """
        starting_rank = BoardState.MIN_RANK + 1 if is_white else BoardState.MAX_RANK - 1
        promotion_rank = BoardState.MAX_RANK if is_white else BoardState.MIN_RANK
        rank_advancement = 1 if is_white else -1

        next_square = origin_square.move(0, rank_advancement)
        if not BoardState.is_in_bounds(next_square):
            # edge of the board
            return

        # straight
        if not self.get_piece_on_square(next_square):
            # next square is free
            if next_square.rank == promotion_rank:
                # promotion
                for piece_type in [PieceType.KNIGHT, PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN]:
                    promotion_piece = Piece(piece_type, is_white)
                    yield self._generate_move(origin_square, next_square, promotion_piece=promotion_piece)
            else:
                # normal move
                yield self._generate_move(origin_square, next_square)

            # first move
            if origin_square.rank == starting_rank:
                # pawn in starting position
                next_next_square = origin_square.move(0, rank_advancement * 2)
                if BoardState.is_in_bounds(next_square) and not self.get_piece_on_square(next_next_square):
                    # double move
                    yield self._generate_move(origin_square, next_next_square)

        # captures
        diagonal_left_sq = origin_square.move(-1, rank_advancement)
        diagonal_right_sq = origin_square.move(1, rank_advancement)
        for diagonal_sq in [diagonal_left_sq, diagonal_right_sq]:
            if BoardState.is_in_bounds(diagonal_sq):
                capture_piece = self.get_piece_on_square(diagonal_sq)
                if capture_piece:
                    if capture_piece.is_white != is_white:
                        # capture
                        yield self._generate_move(origin_square, diagonal_sq)
                elif diagonal_sq == self._en_passant_target and self._white_to_move == is_white:
                    # en passant
                    capture_piece = self.get_piece_on_square(diagonal_sq.move(0, -rank_advancement))
                    if capture_piece.type == PieceType.PAWN and capture_piece.is_white != is_white:
                        yield self._generate_move(origin_square, diagonal_sq, en_passant=True)

    def _get_all_moves_for_knight(self, origin_square: Square, is_white: bool) -> Generator[Move]:
        """
        Calculates all moves for a knight of the given color in the given square
        :param origin_square: square that the knight occupies
        :param is_white: True if the knight is white, False otherwise
        :return: generator of all moves for the knight
        """
        jumps = [
            (1, 2),
            (2, 1),
            (2, -1),
            (1, -2),
            (-1, -2),
            (-2, -1),
            (-2, 1),
            (-1, 2),
        ]

        for jump in jumps:
            new_square = origin_square.move(jump[0], jump[1])

            if not BoardState.is_in_bounds(new_square):
                # out of the board
                continue

            capture_piece = self.get_piece_on_square(new_square)
            if not capture_piece:
                # square is free
                yield self._generate_move(origin_square, new_square)
            elif capture_piece.is_white != is_white:
                # capture
                yield self._generate_move(origin_square, new_square)

    def _get_all_moves_for_bishop(self, origin_square: Square, is_white: bool) -> Generator[Move]:
        """
        Calculates all moves for a bishop of the given color in the given square
        :param origin_square: square that the bishop occupies
        :param is_white: True if the bishop is white, False otherwise
        :return: generator of all moves for the bishop
        """
        directions = [
            (-1, 1), (1, 1),
            (-1, -1), (1, -1)
        ]
        yield from self._get_all_moves_for_line_piece(origin_square, directions, is_white)

    def _get_all_moves_for_rook(self, origin_square: Square, is_white: bool) -> Generator[Move]:
        """
        Calculates all moves for a rook of the given color in the given square
        :param origin_square: square that the rook occupies
        :param is_white: True if the rook is white, False otherwise
        :return: generator of all moves for the rook
        """
        directions = [
            (0, 1), (1, 0),
            (0, -1), (-1, 0)
        ]
        yield from self._get_all_moves_for_line_piece(origin_square, directions, is_white)

    def _get_all_moves_for_queen(self, origin_square: Square, is_white: bool) -> Generator[Move]:
        """
        Calculates all moves for a queen of the given color in the given square
        :param origin_square: square that the queen occupies
        :param is_white: True if the queen is white, False otherwise
        :return: generator of all moves for the queen
        """
        directions = [
            # rook directions
            (0, 1), (1, 0),
            (0, -1), (-1, 0),
            # bishop directions
            (-1, 1), (1, 1),
            (-1, -1), (1, -1)
        ]
        yield from self._get_all_moves_for_line_piece(origin_square, directions, is_white)

    def _get_all_moves_for_king(self, origin_square: Square, is_white: bool) -> Generator[Move]:
        """
        Calculates all moves for a king of the given color in the given square
        :param origin_square: square that the king occupies
        :param is_white: True if the king is white, False otherwise
        :return: generator of all moves for the king
        """
        directions = [
            # rook directions
            (0, 1), (1, 0),
            (0, -1), (-1, 0),
            # bishop directions
            (-1, 1), (1, 1),
            (-1, -1), (1, -1)
        ]

        moves = self._get_all_moves_for_line_piece(origin_square, directions, is_white, max_steps=1)
        for move in moves:
            yield move

        # castling
        castle_initial_square = Square(BoardState.MIN_FILE + 4, BoardState.MIN_RANK if is_white else BoardState.MAX_RANK)

        if origin_square == castle_initial_square:
            can_castle_short = self._w_castle_short if is_white else self._b_castle_short
            can_castle_long = self._w_castle_long if is_white else self._b_castle_long

            castle_short_final_square = Square(BoardState.MAX_FILE - 1, BoardState.MIN_RANK if is_white else BoardState.MAX_RANK)
            castle_long_final_square = Square(BoardState.MIN_FILE + 2, BoardState.MIN_RANK if is_white else BoardState.MAX_RANK)

            castle_short_squares = [(file, BoardState.MIN_RANK if is_white else BoardState.MAX_RANK) for file in range(castle_initial_square.file + 1, BoardState.MAX_FILE)]
            castle_long_squares = [(file, BoardState.MIN_RANK if is_white else BoardState.MAX_RANK) for file in range(BoardState.MIN_FILE + 1, castle_initial_square.file)]

            if can_castle_short:
                rook = self.get_piece_on_square(castle_short_final_square)
                if rook and rook.type == PieceType.ROOK and rook.is_white == is_white:
                    if not any([self.get_piece_on_square(Square(s[0], s[1])) for s in castle_short_squares]):
                        yield self._generate_move(origin_square, castle_short_final_square, castle_short=True)

            if can_castle_long:
                rook = self.get_piece_on_square(castle_long_final_square)
                if rook and rook.type == PieceType.ROOK and rook.is_white == is_white:
                    if not any([self.get_piece_on_square(Square(s[0], s[1])) for s in castle_long_squares]):
                        yield self._generate_move(origin_square, castle_long_final_square, castle_long=True)

    def _get_all_moves_for_line_piece(self, origin_square: Square, directions: list[tuple[int, int]], is_white: bool, max_steps: int = 8) -> Generator[Move]:
        """
        Calculates all moves for a piece that can move in a straight line
        :param origin_square: square that the piece occupies
        :param directions: list of tuples representing directions that the piece can move in (i.e.: (0, -1) for straight line to the left, (1, 1) for diagonal up and to the right, etc.)
        :param is_white: True if the piece is white, False otherwise
        :param max_steps: maximum number of steps to take in each direction. Defaults to 8
        :return: generator of all straight-line moves for the piece
        """
        for direction in directions:
            current_square = origin_square
            steps = 0
            while steps < max_steps:
                next_square = current_square.move(direction[0], direction[1])
                if not BoardState.is_in_bounds(next_square):
                    # out of the board
                    break

                capture_piece = self.get_piece_on_square(next_square)
                if not capture_piece:
                    # square is free
                    yield self._generate_move(origin_square, next_square)
                elif capture_piece.is_white != is_white:
                    # capture
                    yield self._generate_move(origin_square, next_square)
                    break
                else:
                    # blocked square
                    break

                current_square = next_square
                steps += 1

    def _reset_calculations(self):
        """
        Resets all the stored calculations previously performed on the BoardState
        """
        self._is_check = None
        self._legal_moves = None

    @staticmethod
    def is_in_bounds(square: Square) -> bool:
        """
        Calculates if a square is inside the board
        :param square: the square
        :return: True if the square is inside the board, False otherwise
        """
        return BoardState.MIN_FILE <= square.file <= BoardState.MAX_FILE and BoardState.MIN_RANK <= square.rank <= BoardState.MAX_RANK

    @staticmethod
    def _pieces_can_checkmate(pieces: list[Piece]) -> bool:
        """
        Calculates if a set of pieces of the same color are enough to theoretically deliver checkmate
        :param pieces: list of pieces
        :return: True if the pieces could deliver checkmate, False otherwise
        """
        non_king_pieces = [piece for piece in pieces if piece.type != PieceType.KING]
        if len(non_king_pieces) > 1:
            return True
        elif len(non_king_pieces) == 1:
            type = non_king_pieces[0].type
            return type != PieceType.KNIGHT and type != PieceType.BISHOP
        else:
            return False

    @staticmethod
    def _generate_move(origin_square: Square, dest_square: Square, promotion_piece: Piece = None, en_passant: bool = False, castle_short: bool = False, castle_long: bool = False) -> Move:
        return Move(origin_square, dest_square, promotion_piece=promotion_piece, en_passant=en_passant, castle_short=castle_short, castle_long=castle_long)


def get_stating_board() -> BoardState:
    squares = {
        0: {
            0: Piece(PieceType.ROOK, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.ROOK, is_white=False),
        },
        1: {
            0: Piece(PieceType.KNIGHT, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.KNIGHT, is_white=False),
        },
        2: {
            0: Piece(PieceType.BISHOP, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.BISHOP, is_white=False),
        },
        3: {
            0: Piece(PieceType.QUEEN, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.QUEEN, is_white=False),
        },
        4: {
            0: Piece(PieceType.KING, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.KING, is_white=False),
        },
        5: {
            0: Piece(PieceType.BISHOP, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.BISHOP, is_white=False),
        },
        6: {
            0: Piece(PieceType.KNIGHT, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.KNIGHT, is_white=False),
        },
        7: {
            0: Piece(PieceType.ROOK, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.ROOK, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)