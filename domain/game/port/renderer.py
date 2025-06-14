from abc import ABCMeta, abstractmethod
from domain.game.model.board import BoardState

class Renderer(ABCMeta):

    @abstractmethod
    def render(cls, board_state: BoardState):
        raise NotImplemented