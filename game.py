from math import floor

from domain.game.model.board import BoardState, get_stating_board
from domain.game.model.move import Move
from domain.game.model.square import Square
from domain.game.model.pieces import Piece, PieceType
from infrastructure.console.mapper.board_mapper import ConsoleBoardStateMapper
from infrastructure.console.mapper.move_mapper import ConsoleMoveMapper
from infrastructure.console.mapper.piece_mapper import ConsolePieceMapper
from infrastructure.console.mapper.square_mapper import ConsoleSquareMapper

board_mapper = ConsoleBoardStateMapper()
move_mapper = ConsoleMoveMapper()
square_mapper = ConsoleSquareMapper()
piece_mapper = ConsolePieceMapper()
evaluator = None


def _query_origin_square(board_state: BoardState) -> Square:
    moves = board_state.get_legal_moves()
    while True:
        user_input = input('Select square of piece to move: ')
        square = square_mapper.string_to_square(user_input.lower())
        if not square or not board_state.is_in_bounds(square):
            print(f'Invalid input: {user_input}.')
            continue

        if not any([move.origin_square == square for move in moves]):
            piece = board_state.get_piece_on_square(square)
            if not piece:
                print(f'There are not pieces in square {square_mapper.square_to_string(square)}.')
            elif piece.is_white != board_state.white_to_move:
                print(f'The {piece.type.name} on {square_mapper.square_to_string(square)} is a {'white' if piece.is_white else 'black'} piece.')
            else:
                print(f'The {piece.type.name} on {square_mapper.square_to_string(square)} cannot move.')
            continue

        return square


def _query_dest_square(board_state: BoardState, origin_square: Square) -> Square | None:
    moves = board_state.get_legal_moves()
    piece = board_state.get_piece_on_square(origin_square)
    while True:
        user_input = input(f'Select square to move the {piece.type.name} on {square_mapper.square_to_string(origin_square)} (z to go back): ')

        if user_input.lower() == 'z':
            return None

        square = square_mapper.string_to_square(user_input.lower())
        if not square or not board_state.is_in_bounds(square):
            print(f'Invalid input: {user_input}.')
            continue

        if not any([move.origin_square == origin_square and move.dest_square == square for move in moves]):
            target_piece = board_state.get_piece_on_square(square)
            if not target_piece:
                print(f'The {piece.type.name} on {square_mapper.square_to_string(origin_square)} cannot move to {square_mapper.square_to_string(square)}.')
            elif target_piece.is_white == board_state.white_to_move:
                print(f'The {target_piece.type.name} on {square_mapper.square_to_string(square)} is a {'white' if target_piece.is_white else 'black'} piece.')
            else:
                print(f'Illegal move.')
            continue

        return square


def _query_promotion_piece(board_state: BoardState) -> Piece | None:
    while True:
        user_input = input('Select piece to promote to (z to go back): ')

        if user_input.lower() == 'z':
            return None

        piece_type = piece_mapper.string_to_piece_type(user_input.upper())
        if not piece_type:
            print(f'Invalid input: {user_input}.')
            continue
        elif piece_type == PieceType.PAWN:
            print(f'Cannot promote to a pawn.')
            continue
        elif piece_type == PieceType.KING:
            print(f'Cannot promote to a king.')
            continue

        return Piece(piece_type, board_state.white_to_move)


def _find_move(moves: list[Move], origin_square: Square, dest_square: Square) -> Move | list[Move]:
    matching_moves = [move for move in moves if move.origin_square == origin_square and move.dest_square == dest_square]

    if len(matching_moves) == 1:
        return matching_moves[0]
    else:
        return matching_moves


def _print_board(board_state: BoardState, turn: float):
    check = board_state.is_in_check()

    if evaluator:
        score = evaluator.evaluate(board_state)
    else:
        score = '???'

    if board_state.is_stalemate():
        status = 'stalemate'
    elif board_state.cant_checkmate():
        status = 'draw'
    elif board_state.is_checkmate():
        status = 'checkmate'
    else:
        status = 'playing'
    print(board_mapper.board_state_to_string(board_state, border=True))
    print(f'check: {check}')
    print(f'status: {status}')
    print(f'score: {score}')
    print(f'TURN {floor(turn)}. {'WHITE' if board_state.white_to_move else 'BLACK'} TO MOVE')


def _query_move(board_state: BoardState) -> Move:
    moves = board_state.get_legal_moves()

    while True:
        origin_square = _query_origin_square(board_state)
        dest_square = _query_dest_square(board_state, origin_square)
        if not dest_square:
            # cancelled by user, restarting loop
            continue

        selected_move = _find_move(moves, origin_square, dest_square)

        if isinstance(selected_move, list):
            # promotion move
            promotion_piece = _query_promotion_piece(board_state)
            if not promotion_piece:
                # cancelled by user, restarting loop
                continue
            promotion_moves = [move for move in selected_move if move.promotion_piece == promotion_piece]
            selected_move = promotion_moves[0]

        return selected_move


def run():
    board_state = get_stating_board()

    turn = 1
    while not board_state.is_game_over():
        _print_board(board_state, turn)
        selected_move = _query_move(board_state)
        board_state.perform_move(selected_move, update=True)
        turn += 0.5

    _print_board(board_state, turn)


if __name__ == '__main__':
    run()