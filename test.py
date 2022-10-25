import unittest
# from regex import Regex
from nfa import NFA
from parse import Verifier


class TestCase(object):
    def __init__(self, str, regex, expect_result):
        self.str = str
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
            nfa.regex_to_nfa()
            verifier = Verifier()
            result_all = verifier.verify_all(t.str, nfa.start_node)
            # result_batch, batch_passed_node = verifier.verify_batch(
            #     t.str, nfa.start_node)
            print("str is " + t.str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))

            # self.assertEqual(result_batch, t.expect_result)
            self.assertEqual(result_all, t.expect_result)
            # self.assertEqual(all_passed_node, batch_passed_node)


if __name__ == '__main__':
    unittest.main()
