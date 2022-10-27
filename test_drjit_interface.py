
from drjit_utils import DrJitInterface, NO_EVENT, KILLED_STATE, ACCEPT_STATE
import numpy as np
import drjit as dr
import mitsuba as mi


regex = "a*b.c?d+"
interface = DrJitInterface(regex)

events = np.array(
    [['a', 'a', 'b', 'd', 'd'], ['b', 'd', NO_EVENT, NO_EVENT, NO_EVENT], ['b', 'c', 'd', 'c', NO_EVENT]])

# assume when first part of string match regex, even it has more incoming chars, we regard this string as accept
# This assumpution is valid as we will stop the tracing of rays at the moment they match the LPE. It is not possible to have further incoming events.


expected_result_2, passed_node_2 = interface.verifier.verify_all(
    "aabdd", interface.nfa.start_node)
print(expected_result_2, passed_node_2)
expected_result_2, passed_node_2 = interface.verifier.verify_all(
    "bd", interface.nfa.start_node)
print(expected_result_2, passed_node_2)
expected_result_2, passed_node_2 = interface.verifier.verify_all(
    "bcdc", interface.nfa.start_node)
print(expected_result_2, passed_node_2)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# curr_state_batch = [1,1,1]
# for event_batch:
#     for idx in state_total_num:
#         mask = dr.eq(current_state_batch, idx)
#         filtered_event = dr.select(mask, event_batch, ord(NO_EVENT))
#         update_filtered_state = state_transition_given_event(idx, filtered_event)
#         next_state_batch = dr.select(mask, update_filtered_state, next_state_batch)
#     curr_state_batch = next_state_batch

curr_state_batch = mi.Int32(np.ones(3))
for i in range(events.shape[1]):
    event_batch = events[:, i]
    print("After " + str(i)+"th event")
    next_state_batch = interface.batch_tansition(curr_state_batch, event_batch)
    curr_state_batch = next_state_batch
