from .parse import Verifier
from .lexical_analysis import StateUtils
from .lexical_analysis import Event
from .lexical_analysis import Grammar
MAX_DFA_STATUS_NUM = 50


class DFANode(object):
    def __init__(self, node_ID):
        self.node_ID = node_ID
        self.is_accept_state = StateUtils.NORMAL_STATE

    def set_accept(self):
        self.is_accept_state = StateUtils.ACCEPT_STATE


class DFAEdge(object):
    def __init__(self, origin, next, event):
        self.origin = origin
        self.next = next
        self.event = event


class DFA(object):
    STATUS_NUM = 0

    def __init__(self):
        self.nfa_sets = []
        self.accepted = False
        self.status_num = -1
        self.STATUS_NUM = 0
        self.dfa_list = []
        self.verifier = Verifier()
        self.jump_table = self.list_dict(MAX_DFA_STATUS_NUM)
        self.edges = []
        self.accept_node = []

    def get_accept_node(self):
        for dict in self.jump_table:
            if dict:
                if StateUtils.ACCEPT_STATE in dict:
                    self.accept_node.append(True)
                    continue
                self.accept_node.append(False)

    def get_edges(self):
        self.get_accept_node()
        # print(self.accept_node)
        # for dict in self.jump_table:
        #     if dict:
        #         print(dict)
        # print("===============================")

        for origin_ID in range(len(self.jump_table)):
            edges = self.jump_table[origin_ID]
            if edges:
                for edge_event, next_ID in edges.items():
                    origin = DFANode(origin_ID+1)
                    if self.accept_node[origin_ID]:
                        origin.set_accept()

                    if edge_event == StateUtils.ACCEPT_STATE:
                        edge = DFAEdge(origin, origin, Event.NO_EVENT)
                        self.edges.append(edge)
                        continue

                    next = DFANode(next_ID+1)
                    if self.accept_node[next_ID]:
                        next.set_accept()
                    edge = DFAEdge(origin, next, edge_event)
                    self.edges.append(edge)

    def nfas_to_dfa(self, nfas):
        dfa = DFA()
        for n in nfas:
            dfa.nfa_sets.append(n)
            if n.next_1 is None and n.next_2 is None:
                dfa.accepted = True

        dfa.status_num = self.STATUS_NUM
        self.STATUS_NUM = self.STATUS_NUM + 1
        return dfa

    def list_dict(self, width):
        return [dict() for i in range(width)]

    def convert_to_dfa(self, nfa_start_node):
        ns = [nfa_start_node]
        n_closure = self.verifier.closure(ns)

        dfa = self.nfas_to_dfa(n_closure)

        self.dfa_list.append(dfa)

        dfa_index = 0
        while dfa_index < len(self.dfa_list):
            dfa = self.dfa_list[dfa_index]
            for i in range(len(Grammar.events)):
                c = Grammar.events[i]
                nfa_move = self.verifier.move(dfa.nfa_sets, c)
                if nfa_move is not None:
                    nfa_closure = self.verifier.closure(nfa_move)
                    if nfa_closure is None:
                        continue
                    new_dfa = self.convert_completed(nfa_closure)
                    if new_dfa is None:
                        new_dfa = self.nfas_to_dfa(nfa_closure)
                        self.dfa_list.append(new_dfa)
                    next_state = new_dfa.status_num
                self.jump_table[dfa.status_num][c] = next_state
                if new_dfa.accepted:
                    self.jump_table[new_dfa.status_num][StateUtils.ACCEPT_STATE] = True
            dfa_index = dfa_index + 1

    def convert_completed(self, closure):
        for dfa in self.dfa_list:
            if dfa.nfa_sets == closure:
                return dfa

        return None
