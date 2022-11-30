from LPE_Engine.prototype.nfa import NFA
from LPE_Engine.prototype.dfa import DFA
from LPE_Engine.prototype.parse import Verifier
from LPE_Engine.prototype.lexical_analysis import Grammar
from test import TestCase
import unittest


testLists = []
testLists.append(TestCase("SDDDDE", "G|S.*DE", True))
testLists.append(TestCase("GDE", "G.*DE|S.*DE", True))
testLists.append(TestCase("GDE", "[GS].*DE", True))
testLists.append(TestCase("GSDE", "[GS].*DE", True))
testLists.append(TestCase("GGGGSSSSSDE", "[GS].*DE", True))



# testLists.append(TestCase("CT", "C?T", True))
# testLists.append(TestCase("TE", "R?TE?", True))
# testLists.append(TestCase("RTSVDDD", "R*T.V?D+", True))
# testLists.append(TestCase("RVT", "R.T", True))
# testLists.append(TestCase("RT", "RT", True))
# testLists.append(TestCase("RV", "RT", False))
# testLists.append(TestCase("R", "T+", False))
# testLists.append(TestCase("T", "T+", True))
# testLists.append(TestCase("R", "R?", True))
# testLists.append(TestCase("RRT", "R?T", False))
# testLists.append(TestCase("R", "R*T*", True))
# testLists.append(TestCase("RRT", "R*T", True))
# testLists.append(TestCase("TTT", "R*T", False))
# testLists.append(TestCase("R", "R|T", True))
# testLists.append(TestCase("TTT", "R|T", False))
# testLists.append(TestCase("T", "[^R]", True))
# testLists.append(TestCase("TVGD", "[^R]*", True))
# testLists.append(TestCase("RRR", "R*|D*", True))
# testLists.append(TestCase("DDD", "R*|D*", True))
# testLists.append(TestCase("RRD", "R*|D*", False))


class TestDFA(unittest.TestCase):
    def test(self):
        for t in testLists:

            nfa = NFA(t.regex)
            v = Verifier()
            g = Grammar()
            dfa = DFA()
            enum_input = g.check_translate_event_string_simple(t.input_str)
            dfa.convert_to_dfa(nfa.start_node)
            dfa.get_edges()
            # for i in range(len(dfa.jump_table)):
            #     e = dfa.jump_table[i]
            #     if e:
            #         print(e)
            # for e in dfa.edges:
            #     print(e.origin.node_ID, e.next.node_ID, e.event)

            result = v.dfa_match(enum_input, dfa.jump_table)

            print("str is " + t.input_str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))

            self.assertEqual(result, t.expect_result)


if __name__ == '__main__':
    unittest.main()
