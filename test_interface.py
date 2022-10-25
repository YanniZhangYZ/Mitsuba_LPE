
from interface import Interface, NO_EVENT, KILLED_STATE, ACCEPT_STATE


regex = "1*2.3?4+"
interface = Interface(regex)
interface.set_up()
table = interface.nfa.get_node_table()
for n in table:
    print(n.node_ID)
