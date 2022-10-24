from parse import verify
from nfa import regex_to_nfa


class Regex(object):
    def __init__(self, input_string, pattern_string):
        self.input_string = input_string
        self.pattern_string = pattern_string

    def build_nfa(self):
        pattern_string = self.pattern_string
        input_string = self.input_string
        nfa = regex_to_nfa(pattern_string)
        return verify(input_string, nfa)
