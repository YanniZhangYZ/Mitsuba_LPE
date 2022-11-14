
import numpy as np
from ..prototype.nfa import NFA
from ..prototype.parse import Verifier
import drjit as dr
import mitsuba as mi

NO_EVENT = "!"
KILLED_STATE = -1
ACCEPT_STATE = 0
mi.set_variant('llvm_ad_rgb')


class DrJitInterface(object):
    def __init__(self, regex):
        self.regex = regex
        self.nfa = NFA(self.regex)
        self.verifier = Verifier()

    def char_array_to_ascii(self, char_array):
        ascii = []
        for c in char_array:
            ascii.append(ord(c))
        return mi.Int32(ascii)

    def ascii_array_to_char(self, ascii_array):
        chars = []
        for a in ascii_array:
            chars.append(chr(a))
        return np.array(chars)

    # Param:
        # state_batch: array of mi.Int32
        # event_batch: numpy array of char. Need to translate to ascii code of corresponding char event.
    # Return:
        # next_state_batch: array of mi.Int32
    def batch_tansition(self, state_batch, event_batch):
        next_state_batch = state_batch
        ascii_event_batch = self.char_array_to_ascii(event_batch)

        # handle state_batch by state index masking
        for idx in range(1, self.nfa.node_idx_helper):

            mask = dr.eq(state_batch, idx)
            if not (True in mask):
                continue

            # seems Dr.Jit  doesn't support char array
            # filtered_event = np.where(mask, event_batch, NO_EVENT)
            filtered_event = dr.select(mask, ascii_event_batch, ord(NO_EVENT))

            update_filtered_state = self.state_transition_given_event(
                idx, filtered_event)

            next_state_batch = dr.select(
                mask, update_filtered_state, next_state_batch)

        print("next state batch " + str(next_state_batch))
        print("-------------------------------------------")
        return next_state_batch

    # Param:
        # start_node_idx: int.
        # filtered_event: array of mi.Int32. ascii code of corresponding char event. The events for rays whose current state index is start_node_idx
    # Return:
        # update_filtered_state: array of mi.Int32
    def state_transition_given_event(self, start_node_idx, asscii_filtered_event):
        update_filtered_state = []
        curr_start_node = self.nfa.get_node(start_node_idx)
        filtered_event = self.ascii_array_to_char(asscii_filtered_event)
        # print("filtered event " + str(filtered_event))

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
