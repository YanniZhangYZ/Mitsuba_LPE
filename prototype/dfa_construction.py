
from nfa import ASCII_COUNT
from parse import Verifier
from dfa import DFA
from prototype.lexical_analysis import Grammar


dfa_list = []
MAX_DFA_STATUS_NUM = 256
verifier = Verifier()


def get_jump_table(nfa_start_node):
    jump_table = convert_to_dfa(nfa_start_node)
    return jump_table


def list_dict(width):
    return [dict() for i in range(width)]


def convert_to_dfa(nfa_start_node):
    jump_table = list_dict(MAX_DFA_STATUS_NUM)
    ns = [nfa_start_node]
    n_closure = verifier.closure(ns)

    dfa = DFA.nfas_to_dfa(n_closure)

    dfa_list.append(dfa)

    dfa_index = 0
    while dfa_index < len(dfa_list):
        dfa = dfa_list[dfa_index]
        for i in range(len(Grammar.events)):
            c = Grammar.events[i]
            nfa_move = verifier.move(dfa.nfa_sets, c)
            if nfa_move is not None:
                nfa_closure = verifier.closure(nfa_move)
                if nfa_closure is None:
                    continue
                new_dfa = convert_completed(dfa_list, nfa_closure)
                if new_dfa is None:
                    new_dfa = DFA.nfas_to_dfa(nfa_closure)
                    dfa_list.append(new_dfa)
                next_state = new_dfa.status_num
            jump_table[dfa.status_num][c] = next_state
            if new_dfa.accepted:
                jump_table[new_dfa.status_num]['accepted'] = True
        dfa_index = dfa_index + 1

    return jump_table


def convert_completed(dfa_list, closure):
    for dfa in dfa_list:
        if dfa.nfa_sets == closure:
            return dfa

    return None
