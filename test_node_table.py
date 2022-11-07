from prototype.nfa import NFA
from prototype.parse import Verifier
from prototype.lexical_analysis import Grammar


# regex = "a?b.c?d*"
# nfa = NFA(regex)
# node_table = nfa.get_node_table()

# print("====================")
# for n in node_table:
#     print(n.node_ID)

# verifier = Verifier()
# # result = verifier.verify_all("a", nfa.start_node)
# # result2 = verifier.verify_all("b", nfa.node_table[2])
# # result3 = verifier.verify_all("c", nfa.node_table[6])

# result, passed_nodes = verifier.verify_all("bscddd", nfa.start_node)
# print(result, passed_nodes)
# print("====================")

# result, batch_passed_node = verifier.verify_batch("bscddd", nfa.start_node)
# print(result, batch_passed_node)

regex = "R*T*"
nfa = NFA(regex)
node_table = nfa.get_node_table()
v = Verifier()
g = Grammar()
enum_input = g.check_translate_event_string_simple("VRRTV")
result_all, passed_node = v.verify_all(enum_input, nfa.start_node)
