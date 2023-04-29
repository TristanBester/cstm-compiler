import sys

from input_token import Token, TokenType


class Lexer:
    def __init__(self, source):
        self.source = source + "\n"
        self.curr_char = ""
        self.curr_pos = -1
        self.next_char()

    def next_char(self):
        self.curr_pos += 1

        if self.curr_pos >= len(self.source):
            # set current character to EOF
            self.curr_char = "\0"
        else:
            self.curr_char = self.source[self.curr_pos]

    def peek(self):
        if self.curr_pos + 1 >= len(self.source):
            return "\0"
        return self.source[self.curr_pos + 1]

    def abort(self, message):
        sys.exit("Lexing errror: " + message)

    def skip_whitespace(self):
        while self.curr_char in (" ", "\t", "\r"):
            self.next_char()

    def skip_comment(self):
        if self.curr_char == "#":
            while self.curr_char != "\n":
                self.next_char()

    def get_token(self):
        self.skip_whitespace()
        self.skip_comment()

        if self.curr_char == "+":
            token = Token(self.curr_char, TokenType.PLUS)
        elif self.curr_char == "-":
            token = Token(self.curr_char, TokenType.MINUS)
        elif self.curr_char == "*":
            token = Token(self.curr_char, TokenType.ASTERISK)
        elif self.curr_char == "/":
            token = Token(self.curr_char, TokenType.SLASH)
        elif self.curr_char == "\n":
            token = Token(self.curr_char, TokenType.NEWLINE)
        elif self.curr_char == "\0":
            token = Token(self.curr_char, TokenType.EOF)
        elif self.curr_char == "=":
            if self.peek() == "=":
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.EQEQ)
            else:
                token = Token(self.curr_char, TokenType.EQ)
        elif self.curr_char == ">":
            if self.peek() == "=":
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.GTEQ)
            else:
                token = Token(self.curr_char, TokenType.GT)
        elif self.curr_char == "<":
            if self.peek() == "=":
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.LTEQ)
            else:
                token = Token(self.curr_char, TokenType.LT)
        elif self.curr_char == "!":
            if self.peek() == "=":
                last_char = self.curr_char
                self.next_char()
                token = Token(last_char + self.curr_char, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
        elif self.curr_char == '"':
            # Get characters between quotation marks
            self.next_char()
            start_pos = self.curr_pos

            while self.curr_char != '"':
                if self.curr_char in ("\r", "\n", "\t", "\\", "%"):
                    self.abort("Illegal character in string")
                self.next_char()
            token = Token(self.source[start_pos : self.curr_pos], TokenType.STRING)
        elif self.curr_char.isdigit():
            start_pos = self.curr_pos

            while self.peek().isdigit():
                self.next_char()

            if self.peek() == ".":
                self.next_char()

                if not self.peek().isdigit():
                    self.abort("Illegal character in number")

                while self.peek().isdigit():
                    self.next_char()
            token = Token(self.source[start_pos : self.curr_pos + 1], TokenType.NUMBER)
        elif self.curr_char.isalpha():
            start_pos = self.curr_pos

            while self.peek().isalnum():
                self.next_char()

            token_text = self.source[start_pos : self.curr_pos + 1]
            keyword = Token.get_keyword(token_text)

            if keyword is None:
                token = Token(token_text, TokenType.IDENT)
            else:
                token = Token(token_text, keyword)
        else:
            self.abort("Unknown token: " + self.curr_char)

        self.next_char()
        return token
