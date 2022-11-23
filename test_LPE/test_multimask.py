from prototype.nfa import NFA
from prototype.dfa import DFA
from prototype.parse import Verifier
from prototype.lexical_analysis import Grammar
from prototype.lexical_analysis import StateUtils
from prototype.lexical_analysis import Event
from test import TestCase
import unittest


# regex = "R|T"
# input = "TTT"

# nfa = NFA(regex)
# v = Verifier()
# g = Grammar()
# dfa = DFA()
# enum_input = g.check_translate_event_string_simple(input)
# dfa.convert_to_dfa(nfa.start_node)
# dfa.get_edges()
# for e in dfa.edges:
#     print("origin: " + str(e.origin.node_ID)+" next: " +
#           str(e.next.node_ID) + " event: " + str(e.event))
#     print(e.next.is_accept_state)

# print("=======================")


# state_ID = 1
# result = False
# for ch in enum_input:
#     flag = False
#     for e in dfa.edges:
#         if state_ID == e.origin.node_ID and ch == e.event:
#             if e.next.is_accept_state == StateUtils.ACCEPT_STATE:
#                 print("origin: " + str(state_ID)+" next: " +
#                       str(e.next.node_ID) + " event: " + str(ch))
#                 print("hello")
#                 result = True
#                 break
#             state_ID = e.next.node_ID
#             flag = True
#             print("origin: " + str(e.origin.node_ID)+" next: " +
#                   str(state_ID) + " event: " + str(ch))
#             break
#     if flag == False:
#         print("hi")
#         break
#     if result == True:
#         break

# print(result)

testLists = []
testLists.append(TestCase("T", "R?T", True))
testLists.append(TestCase("T", "R?TV?", True))
testLists.append(TestCase("RTSVDDD", "R*T.V?D+", True))
testLists.append(TestCase("RVT", "R.T", True))
testLists.append(TestCase("RT", "RT", True))
testLists.append(TestCase("RV", "RT", False))
testLists.append(TestCase("R", "T+", False))
testLists.append(TestCase("T", "T+", True))
testLists.append(TestCase("R", "R?", True))
testLists.append(TestCase("RRT", "R?T", False))
testLists.append(TestCase("R", "R*T*", True))
testLists.append(TestCase("RRT", "R*T", True))
testLists.append(TestCase("TTT", "R*T", True))  # early stop
testLists.append(TestCase("T", "R|T", True))
testLists.append(TestCase("R", "R|T", True))
testLists.append(TestCase("TTT", "R|T", True))  # early stop
testLists.append(TestCase("T", "[^R]", True))
testLists.append(TestCase("TVGD", "[^R]*", True))


class TestDFA(unittest.TestCase):
    def test(self):
        for t in testLists:
            # g = Grammar()
            # enum_input = g.check_translate_event_string_simple(t.input_str)

            result = self.transition(t.regex, t.input_str)

            print("str is " + t.input_str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))
            print(result, t.expect_result)

            self.assertEqual(result, t.expect_result)

    def transition(self, regex, input_str):
        nfa = NFA(regex)
        g = Grammar()
        dfa = DFA()
        enum_input = g.check_translate_event_string_simple(input_str)
        dfa.convert_to_dfa(nfa.start_node)
        dfa.get_edges()

        state_ID = 1
        result = False
        for ch in enum_input:
            has_match_edge = False
            for e in dfa.edges:
                if state_ID == e.origin.node_ID and ch == e.event:
                    if e.next.is_accept_state == StateUtils.ACCEPT_STATE:
                        result = True
                        # break
                        return result
                    state_ID = e.next.node_ID
                    has_match_edge = True
                    # print("origin: " + str(e.origin.node_ID)+" next: " +
                    #       str(state_ID) + " event: " + str(ch))
                    break
            if has_match_edge == False:
                break
            if result == True:
                break
        return result


if __name__ == '__main__':
    unittest.main()
