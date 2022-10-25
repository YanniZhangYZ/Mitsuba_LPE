
import numpy as np
from nfa import NFA
from parse import Verifier

NO_EVENT = "!"
KILLED_STATE = -1
ACCEPT_STATE = 0


class Interface(object):
    def __init__(self, regex):
        self.regex = regex
        self.nfa = NFA(self.regex)
        self.verifier = Verifier()

    def batch_tansition(self, state_batch, event_batch):
        next_state_batch = state_batch

        # handle state_batch by state index masking
        for idx in range(1, self.nfa.node_idx_helper):
            # print("======================================")
            # print(" at state " + str(idx))
            mask = state_batch == idx
            filtered_event = np.where(mask, event_batch, NO_EVENT)
            # print("filtered event batch " + str(filtered_event))

            # call nfa on
            update_filtered_state = self.state_transition_given_event(
                idx, filtered_event)
            # print(" update_filtered_state " + str(update_filtered_state))

            next_state_batch = np.where(
                mask, update_filtered_state, next_state_batch)
            # print("next state batch " + str(next_state_batch))
        print("next state batch " + str(next_state_batch))
        print("======================================")
        return next_state_batch

    # Param:
        # start_node_idx: int.
        # filtered_event: array of mi.Int32. The events for rays whose current state index is start_node_idx
    # Return:
        # update_filtered_state: array of mi.Int32
    def state_transition_given_event(self, start_node_idx, filtered_event):
        update_filtered_state = []
        curr_start_node = self.nfa.get_node(start_node_idx)

        for e in filtered_event:
            if e == NO_EVENT:
                update_filtered_state.append(KILLED_STATE)
                continue

            next_node_set = self.verifier.verify_one(str(e), curr_start_node)

            if next_node_set is not None:
                if self.verifier.has_accepted_state(next_node_set):
                    update_filtered_state.append(ACCEPT_STATE)
                    continue
                next_start_node = next_node_set[0].node_ID
                update_filtered_state.append(int(next_start_node))
            else:
                update_filtered_state.append(KILLED_STATE)

        return update_filtered_state
