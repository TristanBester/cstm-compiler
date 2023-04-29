import sys

from input_token import TokenType


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set()
        self.labels_declared = set()
        self.labels_gotoed = set()

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

        while self.check_token(TokenType.NEWLINE):
            self.next_token()

        while not self.check_token(TokenType.EOF):
            self.statement()

        for label in self.labels_gotoed:
            if label not in self.labels_declared:
                self.abort("Attempting to GOTO to undeclared label: " + label)

    def statement(self):
        # "PRINT" (expression | string)
        if self.check_token(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.next_token()

            if self.check_token(TokenType.STRING):
                self.next_token()
            else:
                self.expression()
        elif self.check_token(TokenType.IF):
            print("STATEMENT-IF")
            self.next_token()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            while not self.check_token(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
        elif self.check_token(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.next_token()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.check_token(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
        elif self.check_token(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.next_token()

            if self.curr_token.text in self.labels_declared:
                self.abort("Label already exists")
            self.labels_declared.add(self.curr_token.text)

            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.next_token()
            self.labels_gotoed.add(self.curr_token.text)
            self.match(TokenType.IDENT)
        elif self.check_token(TokenType.LET):
            print("STATEMENT-LET")
            self.next_token()

            if self.curr_token.text not in self.symbols:
                self.symbols.add(self.curr_token.text)

            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        elif self.check_token(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.next_token()

            if self.curr_token.text not in self.symbols:
                self.symbols.add(self.curr_token.text)

            self.match(TokenType.IDENT)
        else:
            self.abort(
                "Invalid statement at "
                + self.curr_token.text
                + " ("
                + self.curr_token.kind.name
                + ")"
            )
        self.nl()

    def nl(self):
        print("NEWLINE")

        # match one newline at least
        self.match(TokenType.NEWLINE)
        while self.check_token(TokenType.NEWLINE):
            self.next_token()

    def is_comparison_operator(self):
        return (
            self.check_token(TokenType.GT)
            or self.check_token(TokenType.GTEQ)
            or self.check_token(TokenType.LT)
            or self.check_token(TokenType.LTEQ)
            or self.check_token(TokenType.EQEQ)
            or self.check_token(TokenType.NOTEQ)
        )

    def comparison(self):
        print("COMPARISON")

        self.expression()

        if self.is_comparison_operator():
            self.next_token()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curr_token.text)

        while self.is_comparison_operator():
            self.next_token()
            self.expression()

    def expression(self):
        print("EXPRESSION")

        self.term()
        while self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
            self.term()

    def term(self):
        print("TERM")

        self.unary()
        while self.check_token(TokenType.ASTERISK) or self.check_token(TokenType.SLASH):
            self.next_token()
            self.unary()

    def unary(self):
        print("UNARY")

        if self.check_token(TokenType.PLUS) or self.check_token(TokenType.MINUS):
            self.next_token()
        self.primary()

    def primary(self):
        print("PRIMARY (" + self.curr_token.text + ")")

        if self.check_token(TokenType.NUMBER):
            self.next_token()
        elif self.check_token(TokenType.IDENT):
            if self.curr_token.text not in self.symbols:
                self.abort(
                    "Referencing variable before assignment: " + self.curr_token.text
                )

            self.next_token()
        else:
            self.abort("Unexpected token at " + self.curr_token.text)
