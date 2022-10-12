
from lexical_analysis import Token
from lexical_analysis import Lexer


# 对应的节点有两个出去的ε边
EPSILON = -1
# 边对应的是字符集
CCL = -2
# 一条ε边
EMPTY = -3
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



# construction part

lexer = None

def pattern(pattern_string):
    global lexer
    lexer = Lexer(pattern_string)
    lexer.advance()
    nfa_pair = NFAPair()
    # group construct the entire nfa
    group(nfa_pair)
    return nfa_pair.start_node


def group(pair_out):
    # if lexer.match(Token.OPEN_PAREN):
    #     lexer.advance()
    #     expr(pair_out)
    #     if lexer.match(Token.CLOSE_PAREN):
    #         lexer.advance()
    # elif lexer.match(Token.EOS):
    #     return False
    # else:
    #     expr(pair_out)

    # while True:
    #     pair = NFAPair()
    #     if lexer.match(Token.OPEN_PAREN):
    #         lexer.advance()
    #         expr(pair)
    #         pair_out.end_node.next_1 = pair.start_node
    #         pair_out.end_node = pair.end_node
    #         if lexer.match(Token.CLOSE_PAREN):
    #             lexer.advance()
    #     elif lexer.match(Token.EOS):
    #         return False
    #     else:
    #         expr(pair)
    #         pair_out.end_node.next_1 = pair.start_node
    #         pair_out.end_node = pair.end_node
    if lexer.match(Token.EOS):
        return False
    else:
        expr(pair_out)

    while True:
        pair = NFAPair()
        if lexer.match(Token.EOS):
            return False
        else:
            expr(pair)
            pair_out.end_node.next_1 = pair.start_node
            pair_out.end_node = pair.end_node




def expr(pair_out):
    factor_conn(pair_out)
    pair = NFAPair()

    while lexer.match(Token.OR):
        lexer.advance()
        factor_conn(pair)
        start = NFA()
        start.next_1 = pair.start_node
        start.next_2 = pair_out.start_node
        pair_out.start_node = start

        end = NFA()
        pair.end_node.next_1 = end
        pair_out.end_node.next_2 = end
        pair_out.end_node = end

    return True


# factor connect
def factor_conn(pair_out):
    if is_conn(lexer.current_token):
        factor(pair_out)

    while is_conn(lexer.current_token):
        pair = NFAPair()
        factor(pair)
        pair_out.end_node.next_1 = pair.start_node
        pair_out.end_node = pair.end_node

    return True


# factor * + ? closure
def factor(pair_out):
    # deal with char and .
    if lexer.match(Token.L):
        nfa_single_char(pair_out)
    elif lexer.match(Token.ANY):
        nfa_dot_char(pair_out)
    #deal with *+?
    if lexer.match(Token.CLOSURE):
        nfa_star_closure(pair_out)
    elif lexer.match(Token.PLUS_CLOSE):
        nfa_plus_closure(pair_out)
    elif lexer.match(Token.OPTIONAL):
        nfa_option_closure(pair_out)


# *
def nfa_star_closure(pair_out):
    if not lexer.match(Token.CLOSURE):
        return False
    start = NFA()
    end = NFA()
    start.next_1 = pair_out.start_node
    start.next_2 = end

    pair_out.end_node.next_1 = pair_out.start_node
    pair_out.end_node.next_2 = end

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.advance()
    return True


# +
def nfa_plus_closure(pair_out):
    if not lexer.match(Token.PLUS_CLOSE):
        return False
    start = NFA()
    end = NFA()
    start.next_1 = pair_out.start_node

    pair_out.end_node.next_1 = pair_out.start_node
    pair_out.end_node.next_2 = end

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.advance()
    return True


# ?
def nfa_option_closure(pair_out):
    if not lexer.match(Token.OPTIONAL):
        return False
    start = NFA()
    end = NFA()

    start.next_1 = pair_out.start_node
    start.next_2 = end
    pair_out.end_node.next_1 = end

    pair_out.start_node = start
    pair_out.end_node = end

    lexer.advance()
    return True



def is_conn(token):
    nc = [
        Token.OPEN_PAREN,
        Token.CLOSE_PAREN,
        # Token.AT_EOL,
        Token.EOS,
        Token.CLOSURE,
        Token.PLUS_CLOSE,
        Token.CCL_END,
        Token.AT_BOL,
        Token.OR,
    ]
    return token not in nc


# def term(pair_out):
#     if lexer.match(Token.L):
#         nfa_single_char(pair_out)
#     elif lexer.match(Token.ANY):
#         nfa_dot_char(pair_out)
    # elif lexer.match(Token.CCL_START):
    #     nfa_set_nega_char(pair_out)


# match single char
def nfa_single_char(pair_out):
    if not lexer.match(Token.L):
        return False

    start = pair_out.start_node = NFA()
    pair_out.end_node = pair_out.start_node.next_1 = NFA()
    start.edge = lexer.lexeme
    lexer.advance()
    return True


# match dot
def nfa_dot_char(pair_out):
    if not lexer.match(Token.ANY):
        return False

    start = pair_out.start_node = NFA()
    pair_out.end_node = pair_out.start_node.next_1 = NFA()
    start.edge = CCL
    start.set_input_set()

    lexer.advance()
    return False
