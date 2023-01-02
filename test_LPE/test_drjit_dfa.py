
from LPE_Engine.drjit_utils.drjit_dfa import DrJitDFA

from LPE_Engine.prototype.lexical_analysis import Event
import numpy as np
import mitsuba as mi

# A?	0 or 1 occurrence of A
# A*	0 or more occurrence of A
# A+	1 or more occurrence of A
# .     any event. a wildcard in any position
regex = "R*E.V?G+S*"
jitDFA = DrJitDFA(regex)

result, states = jitDFA.transition_verification("RETGG")
print(result, states)


result, states = jitDFA.transition_verification("RG")
print(result, states)


result, states = jitDFA.transition_verification("REEVGV")  # earlt stop at G
print(result, states)

result, states = jitDFA.transition_verification("RREGV")  # earlt stop at G
print(result, states)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# events = np.array(
#     [['R', 'R', 'T', 'G', 'G'], ['T', 'G', 'N', 'N', 'N'], ['T', 'V', 'G', 'V', 'N'],
#      ['R', 'R', 'R', 'R', 'R'], ['T', 'G', 'G', 'S', 'N'], ['R', 'T', 'S', 'G', 'N']])
events = np.array(
    [['R', 'T', 'G', 'G', 'N'], ['R', 'G', 'N', 'N', 'N'], ['R', 'V', 'G', 'V', 'N'],['R', 'R', 'G', 'V', 'N']])
# events = np.array([
#     ['R', 'T', 'G', 'G', 'N'], ['L', 'R', 'T', 'G', 'G'],
#     ['T', 'G', 'N', 'N', 'N'], ['T', 'G', 'L', 'N', 'N'],
#     ['T', 'V', 'G', 'V', 'N'], ['T', 'V', 'G', 'V', 'L'],
#     ['T', 'G', 'G', 'N', 'N'], ['T', 'L', 'G', 'L', 'G']])


curr_states = mi.Int32(np.ones(4))

for i in range(events.shape[1]):

    # insert light event randomly
    if i == 1:
        event_batch = ['E', 'U', 'E', 'U']
        enums_tmp = jitDFA.g.check_translate_event_batch_simple(event_batch)
        enums = mi.Int32(enums_tmp)
        # print("After " + str(i+1)+"th event")
        # emitter_mask = dr.eq(Event.Emitter.value, enums)
        next_states = jitDFA.transition(curr_states, enums)

        print(next_states)
        curr_states = next_states

        event_batch = ['U', 'U', 'E', 'E']
        enums_tmp = jitDFA.g.check_translate_event_batch_simple(event_batch)
        enums = mi.Int32(enums_tmp)
        # print("After " + str(i+1)+"th event")
        # emitter_mask = dr.eq(Event.Emitter.value, enums)
        # print("---------------------")
        # print("i==2")
        next_states = jitDFA.transition(curr_states, enums)

        print(next_states)
        curr_states = next_states

    event_batch = events[:, i]
    enums_tmp = jitDFA.g.check_translate_event_batch_simple(event_batch)
    enums = mi.Int32(enums_tmp)
    # print("After " + str(i+1)+"th event")
    # emitter_mask = dr.eq(Event.Emitter.value, enums)
    # next_states = jitDFA.transition(curr_states, enums, emitter_mask)
    next_states = jitDFA.transition(curr_states, enums)

    print(next_states)
    curr_states = next_states


