from LPE_Engine.prototype.nfa import NFA
from LPE_Engine.prototype.parse import Verifier
from LPE_Engine.prototype.lexical_analysis import Grammar
import unittest


class TestCase(object):
    def __init__(self, str, regex, expect_result):
        self.input_str = str
        self.regex = regex
        self.expect_result = expect_result


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
testLists.append(TestCase("RD", "R*|D*", False))


class TestRegex(unittest.TestCase):
    def test(self):
        for t in testLists:

            nfa = NFA(t.regex)
            verifier = Verifier()
            g = Grammar()
            enum_input = g.check_translate_event_string_simple(t.input_str)
            result_all, passed_node = verifier.verify_all(
                enum_input, nfa.start_node)

            print("str is " + t.input_str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))

            self.assertEqual(result_all, t.expect_result)


if __name__ == '__main__':
    unittest.main()
