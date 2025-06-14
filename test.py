from cProfile import Profile
from pstats import SortKey, Stats

from domain.engine.engine import Engine
from domain.evaluator.evaluator import Evaluator
from domain.game.model.board import BoardState, get_stating_board
from domain.game.model.pieces import Piece, PieceType
from infrastructure.console.mapper.board_mapper import ConsoleBoardStateMapper
from infrastructure.console.mapper.move_mapper import ConsoleMoveMapper


board_mapper = ConsoleBoardStateMapper()
move_mapper = ConsoleMoveMapper()

evaluator = Evaluator()
engine = Engine(evaluator=evaluator)


def get_test_board_endgame() -> BoardState:
    squares = {
        2: {
            5: Piece(PieceType.KING, is_white=True),
        },
        4: {
            4: Piece(PieceType.PAWN, is_white=True),
        },
        5: {
            4: Piece(PieceType.KING, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_endgame_2() -> BoardState:
    squares = {
        2: {
            5: Piece(PieceType.KING, is_white=True),
        },
        4: {
            4: Piece(PieceType.QUEEN, is_white=True),
        },
        5: {
            4: Piece(PieceType.KING, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_checkmate() -> BoardState:
    squares = {
        5: {
            5: Piece(PieceType.KING, is_white=True),
        },
        6: {
            4: Piece(PieceType.QUEEN, is_white=True),
        },
        7: {
            4: Piece(PieceType.KING, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=False)


def get_test_board_checkmate_2() -> BoardState:
    squares = {
        5: {
            5: Piece(PieceType.KING, is_white=True),
        },
        6: {
            4: Piece(PieceType.QUEEN, is_white=True),
        },
        7: {
            6: Piece(PieceType.KING, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_checkmate_3() -> BoardState:
    squares = {
        5: {
            1: Piece(PieceType.QUEEN, is_white=True),
        },
        7: {
            0: Piece(PieceType.KING, is_white=True),
            3: Piece(PieceType.KING, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_checkmate_4() -> BoardState:
    squares = {
        3: {
            2: Piece(PieceType.QUEEN, is_white=True),
        },
        4: {
            5: Piece(PieceType.KING, is_white=True),
        },
        6: {
            3: Piece(PieceType.KING, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_checkmate_5() -> BoardState:
    squares = {
        0: {
            1: Piece(PieceType.PAWN, is_white=True),
        },
        6: {
            3: Piece(PieceType.KING, is_white=True),
        },
        7: {
            0: Piece(PieceType.KING, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_checkmate_6() -> BoardState:
    squares = {
        6: {
            3: Piece(PieceType.KING, is_white=True),
        },
        7: {
            1: Piece(PieceType.KING, is_white=False),
            7: Piece(PieceType.ROOK, is_white=True),
        },
    }
    return BoardState(squares=squares, white_to_move=False)


def get_test_board_checkmate_7() -> BoardState:
    squares = {
        0: {
            0: Piece(PieceType.KING, is_white=False),
            2: Piece(PieceType.KING, is_white=True),
            3: Piece(PieceType.PAWN, is_white=True),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_check() -> BoardState:
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
            # 6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.QUEEN, is_white=False),
        },
        4: {
            0: Piece(PieceType.KING, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            # 6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.KING, is_white=False),
        },
        5: {
            0: Piece(PieceType.BISHOP, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            5: Piece(PieceType.KNIGHT, is_white=True),
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
    return BoardState(squares=squares, white_to_move=False)


def get_test_board_check_2() -> BoardState:
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
            4: Piece(PieceType.ROOK, is_white=True),
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
    return BoardState(squares=squares, white_to_move=False)


def get_test_board_castle() -> BoardState:
    squares = {
        0: {
            0: Piece(PieceType.ROOK, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.ROOK, is_white=False),
        },
        1: {
            # 0: Piece(PieceType.KNIGHT, is_white=True),
            # 5: Piece(PieceType.ROOK, is_white=False),
        },
        2: {
            # 0: Piece(PieceType.BISHOP, is_white=True),
            # 7: Piece(PieceType.BISHOP, is_white=False),
            # 5: Piece(PieceType.ROOK, is_white=False),
        },
        3: {
            # 0: Piece(PieceType.QUEEN, is_white=True),
            # 7: Piece(PieceType.QUEEN, is_white=False),
        },
        4: {
            0: Piece(PieceType.KING, is_white=True),
            7: Piece(PieceType.KING, is_white=False),
        },
        5: {
            # 0: Piece(PieceType.BISHOP, is_white=True),
            # 5: Piece(PieceType.KNIGHT, is_white=True),
            # 7: Piece(PieceType.BISHOP, is_white=False),
        },
        6: {
            # 0: Piece(PieceType.KNIGHT, is_white=True),
            # 5: Piece(PieceType.ROOK, is_white=False),
        },
        7: {
            0: Piece(PieceType.ROOK, is_white=True),
            1: Piece(PieceType.PAWN, is_white=True),
            6: Piece(PieceType.PAWN, is_white=False),
            7: Piece(PieceType.ROOK, is_white=False),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def get_test_board_promotion() -> BoardState:
    squares = {
        0: {
            1: Piece(PieceType.PAWN, is_white=False),
            6: Piece(PieceType.PAWN, is_white=True),
        },
        1: {
            1: Piece(PieceType.PAWN, is_white=False),
            6: Piece(PieceType.PAWN, is_white=True),
        },
        2: {
            1: Piece(PieceType.PAWN, is_white=False),
            6: Piece(PieceType.PAWN, is_white=True),
        },
        3: {
            1: Piece(PieceType.PAWN, is_white=False),
            6: Piece(PieceType.PAWN, is_white=True),
        },
        4: {
            1: Piece(PieceType.KING, is_white=True),
            6: Piece(PieceType.KING, is_white=False),
        },
        5: {
            1: Piece(PieceType.PAWN, is_white=False),
            6: Piece(PieceType.PAWN, is_white=True),
        },
        6: {
            1: Piece(PieceType.PAWN, is_white=False),
            6: Piece(PieceType.PAWN, is_white=True),
        },
        7: {
            1: Piece(PieceType.PAWN, is_white=False),
            6: Piece(PieceType.PAWN, is_white=True),
        },
    }
    return BoardState(squares=squares, white_to_move=True)


def test():
    board_state = get_test_board_promotion()
    print(board_mapper.board_state_to_string(board_state, border=True))

    with Profile() as profile:
        move, score, sequence = engine.calculate_move(board_state)
        stats = Stats(profile)
        stats.strip_dirs()
        stats.sort_stats(SortKey.CUMULATIVE)
        stats.print_stats()
        stats.dump_stats('./out/stats_test')


if __name__ == '__main__':
    test()