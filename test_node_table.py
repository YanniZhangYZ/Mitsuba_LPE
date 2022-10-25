from nfa import NFA
from parse import Verifier


regex = "a?b.c?d*"
nfa = NFA(regex)
nfa.regex_to_nfa()
node_table = nfa.get_node_table()

print("====================")
for n in node_table:
    print(n.node_ID)

verifier = Verifier()
# result = verifier.verify_all("a", nfa.start_node)
# result2 = verifier.verify_all("b", nfa.node_table[2])
# result3 = verifier.verify_all("c", nfa.node_table[6])

result, passed_nodes = verifier.verify_all("bscddd", nfa.start_node)
print(result, passed_nodes)
print("====================")

result, batch_passed_node = verifier.verify_batch("bscddd", nfa.start_node)
print(result, batch_passed_node)
