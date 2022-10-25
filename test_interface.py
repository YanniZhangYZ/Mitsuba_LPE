
from interface import Interface, NO_EVENT, KILLED_STATE, ACCEPT_STATE
import numpy as np
from parse import Verifier
from nfa import NFA


# regex = "1*2.3?4+"
regex = "a*b.c?d+"
interface = Interface(regex)

# events = np.array([[2, 5, 4, NO_EVENT, NO_EVENT], [1, 1, 2, NO_EVENT, NO_EVENT],
#                    [1, 2, 5, 4, NO_EVENT], [2, 2, 4, 4, 3]])

# events = np.array([[2], [1],
#                    [2], [NO_EVENT]])

events = np.array(
    [['a', 'a', 'b', 'd', 'd'], ['b', 'c', 'd', 'c', NO_EVENT], ['b', 'd', NO_EVENT, NO_EVENT, NO_EVENT]])

# assume when first part of string match regex, even it has more incoming chars, we regard this string as accept
# This assumpution is valid as we will stop the tracing of rays at the moment they match the LPE. It is not possible to have further incoming events.


expected_result_2, passed_node_2 = interface.verifier.verify_all(
    "aabdd", interface.nfa.start_node)
print(expected_result_2, passed_node_2)
expected_result_2, passed_node_2 = interface.verifier.verify_all(
    "bcdc", interface.nfa.start_node)
print(expected_result_2, passed_node_2)
expected_result_2, passed_node_2 = interface.verifier.verify_all(
    "bd", interface.nfa.start_node)
print(expected_result_2, passed_node_2)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

curr_state_batch = np.ones(3)
for i in range(events.shape[1]):
    event_batch = events[:, i]
    print("After " + str(i)+"th event")
    next_state_batch = interface.batch_tansition(curr_state_batch, event_batch)
    curr_state_batch = next_state_batch
