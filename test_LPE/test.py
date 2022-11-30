import unittest
# from regex import Regex
from LPE_Engine.prototype.nfa import NFA
from LPE_Engine.prototype.parse import Verifier
from LPE_Engine.prototype.interface import Interface


class TestCase(object):
    def __init__(self, str, regex, expect_result):
        self.input_str = str
        self.regex = regex
        self.expect_result = expect_result


testLists = []
testLists.append(TestCase("b", "a?b", True))
testLists.append(TestCase("b", "a?bc?", True))

testLists.append(TestCase("bdd", "a?bc?d*", True))
testLists.append(TestCase("acb", "a.b", True))
testLists.append(TestCase("ab", "ab", True))
testLists.append(TestCase("ac", "ab", False))
testLists.append(TestCase("a", "b+", False))
testLists.append(TestCase("b", "b+", True))
testLists.append(TestCase("b", "a?b", True))
testLists.append(TestCase("aab", "a?b", False))
testLists.append(TestCase("b", "a*b", True))
testLists.append(TestCase("aab", "a*b", True))
testLists.append(TestCase("bbb", "a*b", False))
testLists.append(TestCase("b", "a|b", True))
testLists.append(TestCase("a", "a|b", True))
testLists.append(TestCase("bbb", "a|b", False))
testLists.append(TestCase("b", "[^a]", True))
testLists.append(TestCase("bcds", "[^a]*", True))


# testLists.append(RegexMaterial("THISISREGEXTEST", "([A-Z]*|[0-9]+)", True))
# testLists.append(TestCase("a", "^c", True))
# testLists.append(TestCase("c", "^c", False))
# testLists.append(TestCase("ccccc", "[^c]+", False))
# testLists.append(RegexMaterial("ac", "[abcd]+", True))


class TestRegex(unittest.TestCase):
    def test(self):
        for t in testLists:

            nfa = NFA(t.regex)
            verifier = Verifier()
            result_all, passed_node = verifier.verify_all(
                t.input_str, nfa.start_node)
            # result_batch, batch_passed_node = verifier.verify_batch(
            #     t.str, nfa.start_node)
            print("str is " + t.input_str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))

            # self.assertEqual(result_batch, t.expect_result)
            self.assertEqual(result_all, t.expect_result)
            # self.assertEqual(all_passed_node, batch_passed_node)


if __name__ == '__main__':
    unittest.main()
