from domain.game.model.board import BoardState
from domain.game.model.square import Square
from infrastructure.console.mapper.piece_mapper import ConsolePieceMapper


class ConsoleBoardStateMapper:

    CORNER = '+'
    H_LINE = '---'
    V_LINE = '|'
    EMPTY = ' '
    LINE_BREAK = '\n'
    UNICODE_A = 65

    def __init__(self):
        self._piece_mapper = ConsolePieceMapper()

    def board_state_to_string(self, board_state: BoardState, border=False) -> str:
        rank_separator = (ConsoleBoardStateMapper.CORNER + ConsoleBoardStateMapper.H_LINE) * ((BoardState.MAX_FILE + 1) + (1 if border else 0)) + ConsoleBoardStateMapper.CORNER + ConsoleBoardStateMapper.LINE_BREAK
        file_separator = ConsoleBoardStateMapper.V_LINE

        str_ranks = []
        for rank in reversed(range(BoardState.MAX_RANK + 1)):
            str_squares = []

            if border:
                str_squares.append(self._square_to_string(str(rank + 1)))

            for file in range(BoardState.MAX_FILE + 1):
                piece = board_state.get_piece_on_square(Square(file, rank))
                piece_str = self._piece_mapper.piece_to_unicode(piece)
                str_squares.append(self._square_to_string(piece_str))

            str_rank = file_separator + file_separator.join(str_squares) + file_separator + ConsoleBoardStateMapper.LINE_BREAK
            str_ranks.append(str_rank)

        if border:
            str_squares = []
            str_squares.append(self._square_to_string(ConsoleBoardStateMapper.EMPTY))
            for file in range(BoardState.MAX_FILE + 1):
                str_squares.append(self._square_to_string(chr(ConsoleBoardStateMapper.UNICODE_A + file)))
            str_rank = file_separator + file_separator.join(str_squares) + file_separator + ConsoleBoardStateMapper.LINE_BREAK
            str_ranks.append(str_rank)

        str_board = rank_separator + rank_separator.join(str_ranks) + rank_separator
        return str_board

    @staticmethod
    def _square_to_string(piece_str):
        return ' {} '.format(piece_str)

