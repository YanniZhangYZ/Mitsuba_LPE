from enum import Enum


class Token(Enum):
    EOS = 0
    ANY = 1
    EXCEPT = 2
    # AT_EOL = 3
    CLOSE_SQUARE = 4
    OPEN_SQUARE = 5
    CLOSE_CURLY = 6
    CLOSE_PAREN = 7
    STAR = 8
    DASH = 9
    END_OF_INPUT = 10
    L = 11
    OPEN_CURLY = 12
    OPEN_PAREN = 13
    OPTIONAL = 14
    OR = 15
    PLUS = 16


Tokens = {
    '.': Token.ANY,
    '^': Token.EXCEPT,
    '*': Token.STAR,
    '?': Token.OPTIONAL,
    '+': Token.PLUS,
    '|': Token.OR,
    '[': Token.OPEN_SQUARE,
    ']': Token.CLOSE_SQUARE,
    '{': Token.OPEN_CURLY,
    '}': Token.CLOSE_CURLY,
    '(': Token.OPEN_PAREN,
    ')': Token.CLOSE_PAREN,
    '-': Token.DASH,
}


class Lexer(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self.lexeme = ''
        self.pos = 0
        self.current_token = None

    def move_next(self):
        pos = self.pos
        pattern = self.pattern
        if pos > len(pattern) - 1:
            self.current_token = Token.EOS
            return Token.EOS

        text = self.lexeme = pattern[pos]
        self.pos += 1
        self.current_token = Tokens.get(text, Token.L)
        return self.current_token

    def is_current(self, token):
        return self.current_token == token
