import argparse
import io
import sys

from enum import Enum, auto


class CountType(Enum):
    BYTES = auto()
    CHARACTERS = auto()
    WORDS = auto()
    LINES = auto()


class Counter:
    @staticmethod
    def _count_bytes(data):
        return len(data)
    

    @staticmethod
    def _count_lines(text):
        if len(text) == 0:
            return 0
        return text.count("\n")
    

    @staticmethod
    def _count_words(text):
        count = 0
        ix = 0
        while ix < len(text):
            if text[ix].isspace():
                ix += 1
                continue
            count += 1
            while ix < len(text) and not text[ix].isspace():
                ix += 1
        return count
    
    
    @staticmethod
    def _count_characters(text):
        return len(text)
        
    
    @staticmethod
    def _extract_text(file_path, stdin_text, count_type):
        if file_path is None:
            if count_type == CountType.BYTES:
                with io.BytesIO(stdin_text) as f:
                    return f.read()
            else:
                with io.StringIO(stdin_text.decode("utf-8")) as f:
                    return f.read()
        else:
            if count_type == CountType.BYTES:
                with open(file_path, mode="rb") as f:
                    return f.read()
            else:
                with open(file_path, mode="r", newline="") as f:
                    return f.read()
                

    @staticmethod
    def _count(text, count_type):
        type_to_func_map = {
            CountType.BYTES: Counter._count_bytes,
            CountType.LINES: Counter._count_lines,
            CountType.WORDS: Counter._count_words,
            CountType.CHARACTERS: Counter._count_characters,
        }

        return type_to_func_map[count_type](text)

    
    @staticmethod
    def count(file_path, count_types):
        # open()
        # count()
        # display()

        if file_path is None:
            stdin_text = sys.stdin.buffer.read()
        else:
            stdin_text = None

        if not count_types:
            count_types = [CountType.LINES, CountType.WORDS, CountType.BYTES]

        results = []
        for typ in count_types:
            text = Counter._extract_text(file_path, stdin_text, typ)
            results.append(str(Counter._count(text, typ)))

        if file_path is not None:
            results.append(file_path)

        field_width = max([len(v) for v in results]) + 1
        return "".join([f"{v:>{field_width}}" for v in results])
                 

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
            print(Counter.count(file_path, args.count_types))
        except FileNotFoundError:
            print(f"ccwc: '{file_path}': No such file or directory")
        except Exception as e:
            print(e)