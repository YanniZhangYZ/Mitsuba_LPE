from prototype.parse import Verifier
from prototype.lexical_analysis import Grammar
MAX_DFA_STATUS_NUM = 256


class DFA(object):
    STATUS_NUM = 0

    def __init__(self):
        self.nfa_sets = []
        self.accepted = False
        self.status_num = -1
        self.dfa_list = []
        self.verifier = Verifier()

    @classmethod
    def nfas_to_dfa(cls, nfas):
        dfa = cls()
        for n in nfas:
            dfa.nfa_sets.append(n)
            if n.next_1 is None and n.next_2 is None:
                dfa.accepted = True

        dfa.status_num = DFA.STATUS_NUM
        DFA.STATUS_NUM = DFA.STATUS_NUM + 1
        return dfa
