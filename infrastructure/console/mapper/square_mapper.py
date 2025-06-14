from domain.game.model.square import Square

class ConsoleSquareMapper:

    @staticmethod
    def string_to_square(string: str) -> Square | None:
        if not string:
            return None

        if len(string) != 2:
            return None

        file_str = string[0]
        rank_str = string[1]

        file = ord(file_str)-ord('a')
        rank = int(rank_str) - 1

        return Square(file, rank)

    @staticmethod
    def square_to_string(square: Square) -> str:
        return chr(97+square.file) + str(square.rank+1)