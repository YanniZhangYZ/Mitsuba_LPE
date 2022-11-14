
from .lexical_analysis import Token
from .lexical_analysis import Event
from .lexical_analysis import Grammar
from .lexical_analysis import EdgeUtils
from .lexical_analysis import Lexer


# Realized function
# AB	Accepts first A, then B
# A|B	Accepts A or B
# A?	0 or 1 occurrence of A
# A*	0 or more occurrence of A
# A+	1 or more occurrence of A
# .     any event. a wildcard in any position
# [for] matches tokens in the alphabet {f,o,r} in any quantity or sequence

# The precedence from high to low is quantifiers (?, *, +, {}), concatenation, alternatives(|,[])


# TODO: change to LPE related char count, not all ascii character
ASCII_COUNT = 127
EVENTS = Grammar.events


class Node(object):
    STATUS_NUM = 0

    def __init__(self, node_ID):
        self.edge = EdgeUtils.EPSILON
        self.next_1 = None
        self.next_2 = None
        self.visited = False
        self.valid_input_set = set()
        self.node_ID = node_ID

    def set_full_valid_input_set(self):
        self.valid_input_set = set()
        for v in EVENTS:
            self.valid_input_set.add(v)


class NodePair(object):

    def __init__(self):
        self.start_node = None
        self.end_node = None


class NFA(object):

    def __init__(self, regex):
        self.regex = regex
        self.lexer = Lexer(self.regex)
        if self.lexer.check_regex_simple():
            self.start_node = None
            self.node_idx_helper = 0
            self.node_table = None
            self.regex_to_nfa()

    def get_node(self, idx):
        return self.node_table[idx-1]

    # def get_node_idx(self, node):
    #     return self.idx_node_list.index(node)

    # def add_idx_node_item(self, node):
    #     self.idx_node_dict.append(node)

    def regex_to_nfa(self):
        self.lexer.move_next()
        nfa_pair = NodePair()
        # build_group_nfa() construct the entire nfa
        self.build_nfa(nfa_pair)
        self.start_node = nfa_pair.start_node

        # deal with node labeling
        self.traverse_nfa(self.start_node)
        self.relabel_node()

    def get_node_table(self):
        return self.node_table

    def traverse_nfa(self, start_node, visited=None):
        # DFS algorithm to traverse the NFA
        if self.node_table is None:
            self.node_table = []
        self.node_table.append(start_node)

        next_nodes = []
        next1 = start_node.next_1
        next2 = start_node.next_2

        if next1 is not None:
            # print(str(start_node.node_ID) + "-->" + str(next1.node_ID))
            if next1 not in self.node_table:
                next_nodes.append(next1)
        if next2 is not None:
            # print(str(start_node.node_ID) + "-->" + str(next2.node_ID))
            if next2 not in self.node_table:
                next_nodes.append(next2)
        for next in next_nodes:
            self.traverse_nfa(next, self.node_table)

    def relabel_node(self):
        for i, node in enumerate(self.node_table):
            node.node_ID = i+1

    """
    group = (expression)*
    expression = factors (| factors)*
    factors := single_factor | single_factor single_factor*
    single_factor = (term | term (* | + | ?))*
    term  = char | [ char ] | .
    """

    def build_nfa(self, pair_out):
        if self.lexer.is_current(Token.EOS):
            return False
        else:
            self.build_expression_nfa(pair_out)

        while True:
            pair = NodePair()
            if self.lexer.is_current(Token.OPEN_PAREN):
                self.lexer.move_next()
                self.build_expression_nfa(pair)
                pair_out.end_node.next_1 = pair.start_node
                pair_out.end_node = pair.end_node

                if self.lexer.is_current(Token.CLOSE_PAREN):
                    self.lexer.move_next()
            elif self.lexer.is_current(Token.EOS):
                return False
            else:
                self.build_expression_nfa(pair)
                pair_out.end_node.next_1 = pair.start_node
                pair_out.end_node = pair.end_node

    def build_expression_nfa(self, pair_out):
        self.build_factors_nfa(pair_out)
        pair = NodePair()

        while self.lexer.is_current(Token.OR):
            self.lexer.move_next()
            self.build_factors_nfa(pair)
            self.node_idx_helper += 1
            start = Node(self.node_idx_helper)

            start.next_1 = pair.start_node
            start.next_2 = pair_out.start_node
            pair_out.start_node = start

            self.node_idx_helper += 1
            end = Node(self.node_idx_helper)

            pair.end_node.next_1 = end
            pair_out.end_node.next_2 = end
            pair_out.end_node = end

        return True

    def build_factors_nfa(self, pair_out):
        if self.is_conn(self.lexer.current_token):
            self.build_single_factor_nfa(pair_out)

        while self.is_conn(self.lexer.current_token):
            pair = NodePair()
            self.build_single_factor_nfa(pair)
            pair_out.end_node.next_1 = pair.start_node
            pair_out.end_node = pair.end_node

        return True

    # deal with . [] singlechar * + ?

    def build_single_factor_nfa(self, pair_out):
        # deal with char and .
        if self.lexer.is_current(Token.L):
            self.nfa_single_char(pair_out)
        elif self.lexer.is_current(Token.ANY):
            self.nfa_dot_char(pair_out)
        elif self.lexer.is_current(Token.OPEN_SQUARE):
            self.nfa_set_nega_char(pair_out)

        # deal with *+?
        if self.lexer.is_current(Token.STAR):
            self.nfa_star(pair_out)
        elif self.lexer.is_current(Token.PLUS):
            self.nfa_plus(pair_out)
        elif self.lexer.is_current(Token.OPTIONAL):
            self.nfa_optional(pair_out)

    def nfa_set_nega_char(self, pair_out):
        if not self.lexer.is_current(Token.OPEN_SQUARE):
            return False

        complement = False
        self.lexer.move_next()
        if self.lexer.is_current(Token.EXCEPT):
            complement = True

        self.node_idx_helper += 1
        pair_out.start_node = Node(self.node_idx_helper)
        self.node_idx_helper += 1
        pair_out.start_node.next_1 = pair_out.end_node = Node(
            self.node_idx_helper)
        pair_out.start_node.edge = EdgeUtils.CCL

        first = ''
        while not self.lexer.is_current(Token.CLOSE_SQUARE):
            first = self.lexer.lexeme
            pair_out.start_node.valid_input_set.add(first)
            self.lexer.move_next()

        if complement:
            self.char_set_complement(pair_out.start_node.valid_input_set)

        self.lexer.move_next()
        return True

    def char_set_complement(self, valid_input_set):
        origin = set(valid_input_set)
        for v in EVENTS:
            if v not in valid_input_set:
                valid_input_set.add(v)
        for v in origin:
            valid_input_set.remove(v)

    # *

    def nfa_star(self, pair_out):
        if not self.lexer.is_current(Token.STAR):
            return False
        self.node_idx_helper += 1
        start = Node(self.node_idx_helper)
        self.node_idx_helper += 1
        end = Node(self.node_idx_helper)
        start.next_1 = pair_out.start_node
        start.next_2 = end

        pair_out.end_node.next_1 = pair_out.start_node
        pair_out.end_node.next_2 = end

        pair_out.start_node = start
        pair_out.end_node = end

        self.lexer.move_next()
        return True

    # +

    def nfa_plus(self, pair_out):
        if not self.lexer.is_current(Token.PLUS):
            return False
        self.node_idx_helper += 1
        start = Node(self.node_idx_helper)
        self.node_idx_helper += 1
        end = Node(self.node_idx_helper)
        start.next_1 = pair_out.start_node

        pair_out.end_node.next_1 = pair_out.start_node
        pair_out.end_node.next_2 = end

        pair_out.start_node = start
        pair_out.end_node = end

        self.lexer.move_next()
        return True

    # ?

    def nfa_optional(self, pair_out):
        if not self.lexer.is_current(Token.OPTIONAL):
            return False
        self.node_idx_helper += 1
        start = Node(self.node_idx_helper)
        self.node_idx_helper += 1
        end = Node(self.node_idx_helper)

        start.next_1 = pair_out.start_node
        start.next_2 = end
        pair_out.end_node.next_1 = end

        pair_out.start_node = start
        pair_out.end_node = end

        self.lexer.move_next()
        return True

    def is_conn(self, token):
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

    def nfa_single_char(self, nfa_pair):
        if not self.lexer.is_current(Token.L):
            return False

        # if not self.lexer.is_current_event():
        #     return False

        self.node_idx_helper += 1
        nfa_pair.start_node = Node(self.node_idx_helper)
        self.node_idx_helper += 1
        nfa_pair.end_node = nfa_pair.start_node.next_1 = Node(
            self.node_idx_helper)
        nfa_pair.start_node.edge = self.lexer.lexeme

        self.lexer.move_next()
        return True

    # match dot

    def nfa_dot_char(self, pair_out):
        if not self.lexer.is_current(Token.ANY):
            return False
        self.node_idx_helper += 1
        pair_out.start_node = Node(self.node_idx_helper)
        self.node_idx_helper += 1
        pair_out.end_node = pair_out.start_node.next_1 = Node(
            self.node_idx_helper)
        pair_out.start_node.edge = EdgeUtils.CCL
        pair_out.start_node.set_full_valid_input_set()
        # print(pair_out.start_node.valid_input_set)

        self.lexer.move_next()
        return False
