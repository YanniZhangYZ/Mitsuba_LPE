from enum import Enum


class Token(Enum):
    EOS = 0
    ANY = 1
    AT_BOL = 2
    # AT_EOL = 3
    CCL_END = 4
    CCL_START = 5
    CLOSE_CURLY = 6
    CLOSE_PAREN = 7
    CLOSURE = 8
    DASH = 9
    END_OF_INPUT = 10
    L = 11
    OPEN_CURLY = 12
    OPEN_PAREN = 13
    OPTIONAL = 14
    OR = 15
    PLUS_CLOSE = 16


Tokens = {
    '.': Token.ANY,
    '^': Token.AT_BOL,
    # '$': Token.AT_EOL,
    '*': Token.CLOSURE,
    '?': Token.OPTIONAL,
    '|': Token.OR,
    '+': Token.PLUS_CLOSE,
    '[': Token.CCL_START,
    ']': Token.CCL_END,
    '{': Token.OPEN_CURLY,
    '}': Token.CLOSE_CURLY,
    # '(': Token.OPEN_PAREN,
    # ')': Token.CLOSE_PAREN,
    # '-': Token.DASH,
}


class Lexer(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self.lexeme = ''
        self.pos = 0
        # self.isescape = False
        self.current_token = None

    def advance(self):
        pos = self.pos
        pattern = self.pattern
        if pos > len(pattern) - 1:
            self.current_token = Token.EOS
            return Token.EOS

        text = self.lexeme = pattern[pos]
        self.current_token = self.handle_semantic_l(text)

        return self.current_token

    def handle_semantic_l(self, text):
        self.pos = self.pos + 1
        # dict.get(key[, value])
        # value (optional) - Value to be returned if the key is not found. The default value is None
        return Tokens.get(text, Token.L)

    def match(self, token):
        return self.current_token == token