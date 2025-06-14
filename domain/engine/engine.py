import abc
from abc import abstractmethod

from domain.evaluator.evaluator import Evaluator
from domain.game.model.board import BoardState
from domain.game.model.move import Move


class Engine(abc.ABC):

    def __init__(self, evaluator: Evaluator):
        self._evaluator = evaluator

    @abstractmethod
    def calculate_move(self, board_state: BoardState) -> tuple[Move, float, list[Move]]:
        """
        Calculates the next best move for the position and its score. Optionally, it may also calculate a list of the next best sequence of moves, starting with the next best move.
        :param board_state: the board state
        :return: a tuple with the best move, the score for the move, and, optionally, a list of the best moves for the following turns
        """
        raise NotImplemented