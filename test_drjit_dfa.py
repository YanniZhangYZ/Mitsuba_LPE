
from drjit_utils.drjit_dfa import DrJitDFA

from prototype.lexical_analysis import Event
import numpy as np
import drjit as dr
import mitsuba as mi

# A?	0 or 1 occurrence of A
# A*	0 or more occurrence of A
# A+	1 or more occurrence of A
# .     any event. a wildcard in any position
regex = "R*T.V?G+S*"
jitDFA = DrJitDFA(regex)

expected_result_2, passed_state = jitDFA.transition_verification("RRTGG")
print(expected_result_2, passed_state)
expected_result_2, passed_state = jitDFA.transition_verification("TG")
print(expected_result_2, passed_state)
expected_result_2, passed_state = jitDFA.transition_verification(
    "TVGV")  # earlt stop at G
print(expected_result_2, passed_state)

expected_result_2, passed_state = jitDFA.transition_verification(
    "RRRRR")  # will not stop as not match regex yet and waiting for incoming ray event
print(expected_result_2, passed_state)

expected_result_2, passed_state = jitDFA.transition_verification(
    "TGGS")
print(expected_result_2, passed_state)

expected_result_2, passed_state = jitDFA.transition_verification(
    "RTSG")
print(expected_result_2, passed_state)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


events = np.array(
    [['R', 'R', 'T', 'G', 'G'], ['T', 'G', 'N', 'N', 'N'], ['T', 'V', 'G', 'V', 'N'],
     ['R', 'R', 'R', 'R', 'R'], ['T', 'G', 'G', 'S', 'N'], ['R', 'T', 'S', 'G', 'N']])

curr_states = mi.Int32(np.ones(6))

for i in range(events.shape[1]):
    event_batch = events[:, i]
    enums_tmp = jitDFA.g.check_translate_event_batch_simple(event_batch)
    enums = mi.Int32(enums_tmp)
    # print("After " + str(i+1)+"th event")
    next_states = jitDFA.transition(curr_states, enums)
    print(next_states)
    curr_states = next_states


print("=========================")
for e in jitDFA.dfa.edges:
    print("origin: " + str(e.origin.node_ID)+" next: " +
          str(e.next.node_ID) + " event: " + str(e.event))
print("=========================")
