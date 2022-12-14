
from ..prototype.nfa import NFA
from ..prototype.dfa import DFA
from ..prototype.lexical_analysis import Grammar
from ..prototype.lexical_analysis import StateUtils
from ..prototype.lexical_analysis import Event


import drjit as dr
import mitsuba as mi

mi.set_variant('llvm_ad_rgb')


class DrJitDFA(object):
    def __init__(self, regex):
        self.regex = regex
        self.flag_group_list = {mi.BSDFFlags.Reflection: Event.Reflection.value,
                                mi.BSDFFlags.Diffuse: Event.Diffuse.value,
                                mi.BSDFFlags.Transmission: Event.Transmission.value,
                                mi.BSDFFlags.Glossy: Event.Glossy.value,
                                mi.BSDFFlags.Delta: Event.Delta.value}
        self.flag_dict = {mi.BSDFFlags.DiffuseReflection:[Event.Diffuse.value,Event.Reflection.value], 
                          mi.BSDFFlags.DiffuseTransmission: [Event.Diffuse.value,Event.Transmission.value],
                          mi.BSDFFlags.GlossyReflection:[Event.Glossy.value,Event.Reflection.value] ,
                          mi.BSDFFlags.GlossyTransmission:[Event.Glossy.value,Event.Transmission.value] ,
                          mi.BSDFFlags.DeltaReflection:[Event.Delta.value,Event.Reflection.value] ,
                          mi.BSDFFlags.DeltaTransmission:[Event.Delta.value,Event.Transmission.value]}
        self.nfa = NFA(self.regex)
        # self.verifier = Verifier()
        self.g = Grammar()
        self.dfa = DFA()
        self.dfa.convert_to_dfa(self.nfa.start_node)
        self.dfa.get_edges()

    # Param:
        # events is traslated event batch
        # states is state batch
    def transition(self, states, events):
        has_match_edge = dr.zeros(mi.Int32, dr.width(states))
        null_event_mask = dr.eq(Event.NULL.value, events)
        new_states = states

        for e in self.dfa.edges:
            # print("origin: " + str(e.origin.node_ID) + " event: " + str(e.event))
            mask_state = dr.eq(e.origin.node_ID, states)
            mask_event = dr.eq(e.event.value, events)
            mask = mask_state & mask_event
            new_states = dr.select(mask, e.next.node_ID, new_states)
            has_match_edge = dr.select(mask, 1, has_match_edge)
        # print("--------------------")
        # print("match edge " + str(has_match_edge))

        for i, is_accept in enumerate(self.dfa.accept_node):
            if is_accept:
                mask = dr.eq(i+1, new_states)
                new_states = dr.select(
                    mask, StateUtils.ACCEPT_STATE.value, new_states)

        killed_mask = dr.eq(0, has_match_edge)
        new_states = dr.select(
            killed_mask, StateUtils.KILLED_STATE.value, new_states)
        
        new_states = dr.select(
            null_event_mask, states, new_states)

        # make sure only emitter event get transisted here
        # if emitter_mask != False:
        #     not_emitter_mask = dr.neq(True, emitter_mask)
        #     new_states = dr.select(not_emitter_mask, states, new_states)
        return new_states
        

    def get_accept_mask(self,states):
        return dr.eq(states, StateUtils.ACCEPT_STATE.value)
    
    def get_kill_mask(self,states):
        return dr.eq(states, StateUtils.KILLED_STATE.value)

    def create_emitter_events(self, emitter_mask):
        events = dr.zeros(mi.Int32, dr.width(emitter_mask)) + \
            Event.NULL.value
        events = dr.select(emitter_mask, Event.Emitter.value, events)
        return events

    def flag_groups_to_events(self, flags):
        events = dr.zeros(mi.Int32, dr.width(flags)) + Event.NO_EVENT.value
        for f, event_value in self.flag_group_list.items():
            mask = mi.has_flag(flags, f)
            events = dr.select(mask, event_value, events)
        return events

    def single_flag_group_to_events(self, flag, batch_size):
        value = mi.Int32(self.flag_group_list.get(flag))
        events = dr.zeros(mi.Int32, batch_size) + value
        return events

    def NEE_flag_to_events(self, flag, batch_size):
        values = mi.Int32(self.flag_dict.get(flag))
        events0 = dr.zeros(mi.Int32, batch_size) + values[0]
        events1 = dr.zeros(mi.Int32, batch_size) + values[1]
        return events0,events1


    def flags_to_events(self, flags):
        events0= dr.zeros(mi.Int32, dr.width(flags)) + Event.NO_EVENT.value
        events1= dr.zeros(mi.Int32, dr.width(flags)) + Event.NO_EVENT.value
        for f, event_values in self.flag_dict.items():
            mask = mi.has_flag(flags, f)
            events0 = dr.select(mask, event_values[0], events0)
            events1 = dr.select(mask, event_values[1], events1)
        return events0,events1


    def get_NEE_flags(self):
        return list(self.flag_dict.keys())[:-2]



# ===============================================================

    def transition_verification(self, input_str):
        passed_state = []
        enum_input = self.g.check_translate_event_string_simple(input_str)

        state_ID = 1
        passed_state.append(state_ID)
        result = False
        for ch in enum_input:
            # if ch == Event.Emitter:
            #     continue
            has_match_edge = False
            for e in self.dfa.edges:
                if state_ID == e.origin.node_ID and ch == e.event:
                    state_ID = e.next.node_ID
                    passed_state.append(state_ID)
                    has_match_edge = True
                    if e.next.is_accept_state == StateUtils.ACCEPT_STATE:
                        result = True
                        # break
                        return result, passed_state

                    # print("origin: " + str(e.origin.node_ID)+" next: " +
                    #       str(state_ID) + " event: " + str(ch))
                    break
            if has_match_edge == False:
                break
            if result == True:
                break
        return result, passed_state
