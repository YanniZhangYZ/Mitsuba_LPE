from prototype.nfa import NFA
from prototype.dfa import DFA
from prototype.parse import Verifier
from prototype.lexical_analysis import Grammar
from test import TestCase
import unittest


testLists = []
testLists.append(TestCase("T", "R?T", True))
testLists.append(TestCase("T", "R?TV?", True))
testLists.append(TestCase("RTSVDDD", "R*T.V?D+", True))
testLists.append(TestCase("RVT", "R.T", True))
testLists.append(TestCase("RT", "RT", True))
testLists.append(TestCase("RV", "RT", False))
testLists.append(TestCase("R", "T+", False))
testLists.append(TestCase("T", "T+", True))
testLists.append(TestCase("T", "R?T", True))
testLists.append(TestCase("RRT", "R?T", False))
testLists.append(TestCase("T", "R*T", True))
testLists.append(TestCase("RRT", "R*T", True))
testLists.append(TestCase("TTT", "R*T", False))
testLists.append(TestCase("T", "R|T", True))
testLists.append(TestCase("R", "R|T", True))
testLists.append(TestCase("TTT", "R|T", False))
testLists.append(TestCase("T", "[^R]", True))
testLists.append(TestCase("TVGD", "[^R]*", True))


class TestDFA(unittest.TestCase):
    def test(self):
        for t in testLists:

            nfa = NFA(t.regex)
            v = Verifier()
            g = Grammar()
            dfa = DFA()
            enum_input = g.check_translate_event_string_simple(t.str)
            dfa.convert_to_dfa(nfa.start_node)

            result = v.dfa_match(enum_input, dfa.jump_table)

            print("str is " + t.str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))

            self.assertEqual(result, t.expect_result)


if __name__ == '__main__':
    unittest.main()
