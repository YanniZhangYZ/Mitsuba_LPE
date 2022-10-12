from parse import match
from nfa import pattern


class Regex(object):
    def __init__(self, input_string, pattern_string):
        self.input_string = input_string
        self.pattern_string = pattern_string


    def match(self):
        pattern_string = self.pattern_string
        input_string = self.input_string
        nfa = pattern(pattern_string)
        return match(input_string, nfa)            

    def replace():
        pass

    def search():
        pass