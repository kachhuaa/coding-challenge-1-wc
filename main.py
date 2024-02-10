import argparse

from enum import Flag, auto
from functools import partial


class CountType(Flag):
    BYTES = auto()
    CHARACTERS = auto()
    WORDS = auto()
    LINES = auto()

class WordCounter:
    @staticmethod
    def _count_bytes(file_path):
        with open(file_path, mode="rb") as f:
            return len(f.read())
    
    @staticmethod
    def count(file_path, count_types):
        type_to_func_map = {
            CountType.BYTES: WordCounter._count_bytes,
        }

        result = []
        for typ in count_types:
            result.append(str(type_to_func_map[typ](file_path)))

        result.append(file_path)
        return " ".join(result)
                 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ccwc", description="ccwc - print newline, word, and byte counts for each file")
    parser.add_argument("-c", "--bytes", dest="count_types", action="append_const", const=CountType.BYTES, help="print the  byte counts")
    parser.add_argument("file_path", metavar="FILE", nargs=1, help="path to file")
    args = parser.parse_args()
    
    try:
        print(WordCounter.count(args.file_path[0], args.count_types))
    except FileNotFoundError:
        print(f"ccwc: {args.file_path[0]}: No such file or directory")