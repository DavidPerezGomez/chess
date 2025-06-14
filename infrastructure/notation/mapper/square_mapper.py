class NotationSquareMapper:

    @staticmethod
    def string_to_file(file_str: str) -> int:
        return ord(file_str) - ord('a')

    @staticmethod
    def string_to_rank(rank_str: str) -> int:
        return int(rank_str) - 1