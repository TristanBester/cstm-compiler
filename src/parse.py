import sys

from input_token import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

    def check_token(self, kind):
        return kind == self.curr_token.kind

    def check_peek(self, kind):
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            self.abort("Expected " + kind.name + ", got ", self.cur_token.kind.name)
        self.next_token()

    def next_token(self):
        self.curr_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message):
        sys.exit("Error: " + message)

    def program(self):
        """program ::= {statement}"""
        print("PROGRAM")

        while not self.check_token(TokenType.EOF):
            self.statement()

    def statement(self):
        # "PRINT" (expression | string)
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        self.nl()

    def nl(self):
        print("NEWLINE")

        # match one newline at least
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()
