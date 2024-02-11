import argparse
import sys

from enum import Enum, auto


class CountType(Enum):
    BYTES = auto()
    CHARACTERS = auto()
    WORDS = auto()
    LINES = auto()


class WordCounter:
    @staticmethod
    def _count_bytes(file_path):
        with open(file_path, mode="rb") as f:
            return len(f.read())
    
    
    def _count_lines(file_path):
        with open(file_path, mode="r") as f:
            text = f.read()
            if len(text) == 0:
                return 0
            return text.count("\n")
    

    def _count_words(file_path):
        count = 0
        with open(file_path, mode="r") as f:
            text = f.read()
            ix = 0
            while ix < len(text):
                if text[ix].isspace():
                    ix += 1
                    continue
                count += 1
                while ix < len(text) and not text[ix].isspace():
                    ix += 1
            return count
    

    def _count_characters(file_path):
        with open(file_path, mode="r", newline="") as f:
            return len(f.read())

    
    @staticmethod
    def count(file_path, count_types):
        type_to_func_map = {
            CountType.BYTES: WordCounter._count_bytes,
            CountType.LINES: WordCounter._count_lines,
            CountType.WORDS: WordCounter._count_words,
            CountType.CHARACTERS: WordCounter._count_characters,
        }

        if not count_types:
            count_types = [CountType.LINES, CountType.WORDS, CountType.BYTES]

        result = [str(type_to_func_map[typ](file_path)) for typ in count_types]
        result.append(file_path)

        field_width = max([len(v) for v in result]) + 1
        return "".join([f"{v:>{field_width}}" for v in result])
                 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ccwc", description="ccwc - print newline, word, and byte counts for each file")
    parser.add_argument("-c", "--bytes", dest="count_types", action="append_const", const=CountType.BYTES, help="print the  byte counts")
    parser.add_argument("-l", "--lines", dest="count_types", action="append_const", const=CountType.LINES, help="print the newline counts")
    parser.add_argument("-w", "--words", dest="count_types", action="append_const", const=CountType.WORDS, help="print the word counts")
    parser.add_argument("-m", "--chars", dest="count_types", action="append_const", const=CountType.CHARACTERS, help="print the character counts")
    parser.add_argument("file_path", metavar="FILE", nargs="?", help="path to file")
    args = parser.parse_args()

    file_path = args.file_path

    if file_path == "":
        print("ccwc: invalid zero-length file name")
    else:
        try:
            print(WordCounter.count(file_path, args.count_types))
        except FileNotFoundError:
            print(f"ccwc: '{file_path}': No such file or directory")
        except Exception as e:
            print(e)