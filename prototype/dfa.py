from prototype.parse import Verifier
from prototype.lexical_analysis import StateUtils
from prototype.lexical_analysis import Grammar
MAX_DFA_STATUS_NUM = 50


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
