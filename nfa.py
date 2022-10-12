
from lexical_analysis import Token
from lexical_analysis import Lexer


# Realized function
# AB	Accepts first A, then B
# A|B	Accepts A or B
# A?	0 or 1 occurrence of A
# A*	0 or more occurrence of A
# A+	1 or more occurrence of A
# .     any event. a wildcard in any position
# [for] matches tokens in the alphabet {f,o,r} in any quantity or sequence

# A{n}	Accepts exactly n consecutive occurrences of A
# A{n,m}	Accepts from n to m, inclusively, occurrences of A
# A{n,}	    Accept more than n times consecutive occurrences of A
# The precedence from high to low is quantifiers (?, *, +, {}), concatenation, alternatives(|,[])


# edge with empty transition condition
EPSILON = -1
# edge with char transition condition
CCL = -2

# TODO: change to LPE related char count, not all ascii character
ASCII_COUNT = 127


class NFA(object):
    STATUS_NUM = 0

    def __init__(self):
        self.edge = EPSILON
        self.next_1 = None
        self.next_2 = None
        self.visited = False
        self.input_set = set()
        self.set_status_num()

    def set_status_num(self):
        self.status_num = NFA.STATUS_NUM
        NFA.STATUS_NUM = NFA.STATUS_NUM + 1

    def set_input_set(self):
        self.input_set = set()
        for i in range(ASCII_COUNT):
            self.input_set.add(chr(i))


class NFAPair(object):

    def __init__(self):
        self.start_node = None
        self.end_node = None


# ============================================
# Construction Part
# ============================================
lexer = None


def regex_to_nfa(regular_expression):
    global lexer
    lexer = Lexer(regular_expression)
    lexer.next_token()
    nfa_pair = NFAPair()
    # build_group_nfa() construct the entire nfa
    build_group_nfa(nfa_pair)
    return nfa_pair.start_node


"""
group = (expression)*
expression = factors (| factors)*
factors := single_factor | single_factor single_factor*
single_factor = (term | term (* | + | ?))*
term  = char | [ char ] | .
"""


def build_group_nfa(pair_out):
    if lexer.is_current_token(Token.OPEN_PAREN):
        lexer.next_token()
        build_expression_nfa(pair_out)
        if lexer.is_current_token(Token.CLOSE_PAREN):
            lexer.next_token()
    elif lexer.is_current_token(Token.EOS):
        return False
    else:
        build_expression_nfa(pair_out)

    while True:
        pair = NFAPair()
        if lexer.is_current_token(Token.OPEN_PAREN):
            lexer.next_token()
            build_expression_nfa(pair)
            pair_out.end_node.next_1 = pair.start_node
            pair_out.end_node = pair.end_node
            if lexer.is_current_token(Token.CLOSE_PAREN):
                lexer.next_token()
        elif lexer.is_current_token(Token.EOS):
            return False
        else:
            build_expression_nfa(pair)
            pair_out.end_node.next_1 = pair.start_node
            pair_out.end_node = pair.end_node


def build_expression_nfa(pair_out):
    build_factors_nfa(pair_out)
    pair = NFAPair()

    while lexer.is_current_token(Token.OR):
        lexer.next_token()
        build_factors_nfa(pair)
        start = NFA()
        start.next_1 = pair.start_node
        start.next_2 = pair_out.start_node
        pair_out.start_node = start

        end = NFA()
        pair.end_node.next_1 = end
        pair_out.end_node.next_2 = end
        pair_out.end_node = end

    return True


def build_factors_nfa(pair_out):
    if is_conn(lexer.current_token):
        build_single_factor_nfa(pair_out)

    while is_conn(lexer.current_token):
        pair = NFAPair()
        build_single_factor_nfa(pair)
        pair_out.end_node.next_1 = pair.start_node
        pair_out.end_node = pair.end_node

    return True


# deal with . [] singlechar * + ?
def build_single_factor_nfa(pair_out):
    # deal with char and .
    if lexer.is_current_token(Token.L):
        nfa_single_char(pair_out)
    elif lexer.is_current_token(Token.ANY):
        nfa_dot_char(pair_out)
    elif lexer.is_current_token(Token.OPEN_SQUARE):
        nfa_set_nega_char(pair_out)

    # deal with *+?
    if lexer.is_current_token(Token.STAR):
        nfa_star_closure(pair_out)
    elif lexer.is_current_token(Token.PLUS):
        nfa_plus_closure(pair_out)
    elif lexer.is_current_token(Token.OPTIONAL):
        nfa_option_closure(pair_out)


def nfa_set_nega_char(pair_out):
    if not lexer.is_current_token(Token.OPEN_SQUARE):
        return False

    complement = False
    lexer.next_token()
    if lexer.is_current_token(Token.EXCEPT):
        complement = True

    pair_out.start_node = NFA()
    pair_out.start_node.next_1 = pair_out.end_node = NFA()
    pair_out.start_node.edge = CCL

    first = ''
    while not lexer.is_current_token(Token.CLOSE_SQUARE):
        first = lexer.lexeme
        pair_out.start_node.input_set.add(first)
        lexer.next_token()

    if complement:
        char_set_complement(pair_out.start_node.input_set)

    lexer.next_token()
    return True


def char_set_complement(input_set):
    origin = set(input_set)
    for i in range(ASCII_COUNT):
        c = chr(i)
        if c not in input_set:
            input_set.add(c)
    for c in origin:
        input_set.remove(c)


# *
def nfa_star_closure(pair_out):
    if not lexer.is_current_token(Token.STAR):
        return False
    start = NFA()
    end = NFA()
    start.next_1 = pair_out.start_node
    start.next_2 = end

    pair_out.end_node.next_1 = pair_out.start_node
    pair_out.end_node.next_2 = end

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.next_token()
    return True


# +
def nfa_plus_closure(pair_out):
    if not lexer.is_current_token(Token.PLUS):
        return False
    start = NFA()
    end = NFA()
    start.next_1 = pair_out.start_node

    pair_out.end_node.next_1 = pair_out.start_node
    pair_out.end_node.next_2 = end

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.next_token()
    return True


# ?
def nfa_option_closure(pair_out):
    if not lexer.is_current_token(Token.OPTIONAL):
        return False
    start = NFA()
    end = NFA()

    start.next_1 = pair_out.start_node
    start.next_2 = end
    pair_out.end_node.next_1 = end

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.next_token()
    return True


def is_conn(token):
    nc = [
        Token.OPEN_PAREN,
        Token.CLOSE_PAREN,
        Token.EOS,
        Token.STAR,
        Token.PLUS,
        Token.CLOSE_SQUARE,
        Token.CLOSE_CURLY,
        Token.EXCEPT,
        Token.OR,
    ]
    return token not in nc


# match single char
def nfa_single_char(nfa_pair):
    if not lexer.is_current_token(Token.L):
        return False

    nfa_pair.start_node = NFA()
    nfa_pair.end_node = nfa_pair.start_node.next_1 = NFA()
    nfa_pair.start_node.edge = lexer.lexeme
    lexer.next_token()
    return True


# match dot
def nfa_dot_char(pair_out):
    if not lexer.is_current_token(Token.ANY):
        return False

    pair_out.start_node = NFA()
    pair_out.end_node = pair_out.start_node.next_1 = NFA()
    pair_out.start_node.edge = CCL
    pair_out.start_node.set_input_set()

    lexer.next_token()
    return False
