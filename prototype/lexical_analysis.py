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


class EdgeUtils(Enum):
    # edge with empty transition condition
    EPSILON = 31
    # edge with char transition condition
    CCL = 32


class Event(Enum):
    Reflection = 21  # reflection type
    Transmission = 22  # transmission type
    Volume = 23  # volume interaction type
    Diffuse = 24  # diffuse mode
    Glossy = 25  # glossy mode
    Specular = 26  # specular mode
    NO_EVENT = -1


class Grammar(object):

    # TODO: optimize to parallel
    def check_translate_event_string_simple(self, event_string):
        enum_events = []
        for ch in list(event_string):
            if ch not in self.events_grammar.keys():
                print("Invalid input strings.")
                return None
            enum_events.append(self.events_grammar.get(ch))
        return enum_events

    events = [Event.Reflection, Event.Transmission, Event.Volume,
              Event.Diffuse, Event.Glossy, Event.Specular]
    tokens = [Token.ANY, Token.EXCEPT, Token.STAR, Token.OPTIONAL, Token.PLUS, Token.OR, Token.OPEN_SQUARE,
              Token.CLOSE_SQUARE, Token.OPEN_CURLY, Token.CLOSE_CURLY, Token.OPEN_PAREN, Token.CLOSE_PAREN, Token.DASH]

    events_grammar = {
        'R': Event.Reflection,
        'T': Event.Transmission,
        'V': Event.Volume,
        'D': Event.Diffuse,
        'G': Event.Glossy,
        'S': Event.Specular,
        'N': Event.NO_EVENT,
    }

    tokens_grammar = {
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
    def __init__(self, regex):
        self.regex = regex
        self.lexeme = ''
        self.pos = 0
        self.current_token = None

    def check_regex_simple(self):
        for c in self.regex:
            if (c not in Grammar.events_grammar.keys()) and (c not in Grammar.tokens_grammar.keys()):
                print("Invalid regular expression.")
                return False
        return True

    def move_next(self):
        pos = self.pos
        regex = self.regex
        if pos > len(regex) - 1:
            self.current_token = Token.EOS
            return Token.EOS

        text = self.lexeme = regex[pos]
        self.pos += 1
        self.current_token = Grammar.tokens_grammar.get(text, Token.L)

        if self.current_token == Token.L:
            self.lexeme = Grammar.events_grammar.get(text, Event.NO_EVENT)
            # print(type(Grammar.events.get(text, Event.NO_EVENT)))

        return self.current_token

    def is_current(self, token):
        return self.current_token == token
