import sys

from lexer import Lexer
from parse import Parser

if __name__ == "__main__":
    print("Compiler started")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs a source file as argument")

    with open(sys.argv[1], "r") as f:
        source = f.read()

    lexer = Lexer(source)
    parser = Parser(lexer)

    parser.program()
    print("Parsing completed")
