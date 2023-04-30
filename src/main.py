import sys

from emitter import Emitter
from lexer import Lexer
from parse import Parser

if __name__ == "__main__":
    print("Compiler started")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs a source file as argument")

    with open(sys.argv[1], "r") as f:
        source = f.read()

    lexer = Lexer(source)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.write_file()
    print("Compilation completed")
