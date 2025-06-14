import math
import abc
from abc import abstractmethod

from domain.game.model.board import BoardState


class Evaluator(abc.ABC):

    SCORE_DRAW = 0
    SCORE_WIN = math.inf

    def evaluate(self, board_state: BoardState) -> float:
        """
        Evaluates a position on the board and generates a score for the white pieces
        :param board_state: the board state to evaluate
        :return: the score for white
        """
        if board_state.is_checkmate():
            if not board_state.white_to_move:
                return Evaluator.SCORE_WIN
            else:
                return -Evaluator.SCORE_WIN

        if board_state.is_stalemate() or board_state.cant_checkmate():
            return Evaluator.SCORE_DRAW

        return self._evaluate(board_state)

    @abstractmethod
    def _evaluate(self, board_state: BoardState) -> float:
        raise NotImplemented