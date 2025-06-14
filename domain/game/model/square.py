from __future__ import annotations


class Square:

    def __init__(self, file: int, rank: int):
        self._file = file
        self._rank = rank

    def __eq__(self, other) -> bool:
        if other is None:
            return self is None
        return self.file == other.file and self.rank == other.rank

    def __str__(self):
        return f'{self.file},{self.rank}'

    def __deepcopy__(self, memo=None) -> Square:
        return Square(file=self._file, rank=self._rank)

    def __hash__(self) -> int:
        return 10 * self._file + self._rank

    @property
    def file(self) -> int:
        return self._file

    @property
    def rank(self) -> int:
        return self._rank

    def move(self, file: int, rank: int) -> Square:
        """
        Creates a new square after moving the specified number of files and ranks
        :param file: the number of files to move (positive to go right, negative to go left)
        :param rank: the number of ranks to move (positive to go up, negative to go down)
        :return: the new square
        """
        return Square(self.file + file, self.rank + rank)