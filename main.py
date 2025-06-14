import time
from cProfile import Profile
from pstats import Stats, SortKey

from domain.engine.engine import Engine
from domain.evaluator.evaluator import Evaluator
from domain.game.model.board import get_stating_board
from infrastructure.console.mapper.board_mapper import ConsoleBoardStateMapper
from infrastructure.console.mapper.move_mapper import ConsoleMoveMapper

board_mapper = ConsoleBoardStateMapper()
move_mapper = ConsoleMoveMapper()

evaluator = Evaluator()
engine = Engine(evaluator=evaluator)


def main():
    board_state = get_stating_board()

    move = None
    t_0 = time.time()
    with Profile() as profile:
        while True:
            if move:
                board_state.perform_move(move, update=True)

            print(board_mapper.board_state_to_string(board_state, border=True))
            if board_state.is_stalemate():
                status = 'stalemate'
            elif board_state.cant_checkmate():
                status = 'draw'
            elif board_state.is_checkmate():
                status = 'checkmate'
            else:
                status = 'playing'
            print(f'status: {status}')
            print(f'{'WHITE' if board_state.white_to_move else 'BLACK'} TO MOVE')

            if board_state.is_game_over():
                evaluator.evaluate(board_state)
                break

            t_0_0 = time.time()
            move, score, sequence = engine.calculate_move(board_state)
            print(f'Score {score if board_state.white_to_move else -score}')
            print(f'Move: {move_mapper.move_to_string(move)}')
            print(f'Sequence: {', '.join([move_mapper.move_to_string(move) for move in sequence])}')
            print(f'Time: {time.time() - t_0_0}s')
            # input()

        (Stats(profile)
            .strip_dirs()
            .sort_stats(SortKey.CUMULATIVE)
            .print_stats()
            .dump_stats('./out/stats_main')
         )

    t_1 = time.time()
    print(f'{t_1 - t_0}s')



if __name__ == '__main__':
    main()
