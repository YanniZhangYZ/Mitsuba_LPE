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


class StateUtils(Enum):
    KILLED_STATE = 0
    ACCEPT_STATE = -1
    NORMAL_STATE = 1
    LIGHT_STATE = -2


class Event(Enum):
    Camera = 20
    Reflection = 21  # reflection type
    Transmission = 22  # transmission type
    Volume = 23  # volume interaction type
    Diffuse = 24  # diffuse mode
    Glossy = 25  # glossy mode
    Delta = 26  # specular mode
    Emitter = 27  # can only be the first event or last event
    NO_EVENT = -1
    NULL = -2 # only used with Emitter event to create emitter event batch


class Grammar(object):

    # # check event batch from multi ray
    def check_translate_event_batch_simple(self, event_batch):
        enum_events = []
        for ch in list(event_batch):
            if ch not in self.events_grammar.keys():
                print("Invalid input strings.")
                return None
            enum_events.append(self.events_grammar.get(ch).value)
        return enum_events

    # for event series of one ray
    def check_translate_event_string_simple(self, event_batch):
        enum_events = []
        for ch in list(event_batch):
            if ch not in self.events_grammar.keys():
                print("Invalid input batch.")
                return None
            enum_events.append(self.events_grammar.get(ch))
        return enum_events

    events = [Event.Camera, Event.Reflection, Event.Transmission, Event.Volume,
              Event.Diffuse, Event.Glossy, Event.Emitter, Event.Delta]
    tokens = [Token.ANY, Token.EXCEPT, Token.STAR, Token.OPTIONAL, Token.PLUS, Token.OR, Token.OPEN_SQUARE,
              Token.CLOSE_SQUARE, Token.OPEN_CURLY, Token.CLOSE_CURLY, Token.OPEN_PAREN, Token.CLOSE_PAREN, Token.DASH]

    events_grammar = {
        'C': Event.Camera,
        'R': Event.Reflection,
        'T': Event.Transmission,
        'V': Event.Volume,
        'D': Event.Diffuse,
        'G': Event.Glossy,
        'E': Event.Emitter,
        'S': Event.Delta,
        'N': Event.NO_EVENT,
        'U': Event.NULL,
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
                print("[error]: Invalid regular expression.")
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

        # if haven't got any test
        if self.current_token == Token.L:
            self.lexeme = Grammar.events_grammar.get(text, Event.NO_EVENT)
            # print(type(Grammar.events.get(text, Event.NO_EVENT)))

        return self.current_token

    def is_current(self, token):
        return self.current_token == token
