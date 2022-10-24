import unittest
from regex import Regex


class TestCase(object):
    def __init__(self, str, regex, expect_result):
        self.str = str
        self.regex = regex
        self.expect_result = expect_result


testLists = []
# concatenation
testLists.append(TestCase("a", "a", True))
testLists.append(TestCase("ab", "ab", True))
testLists.append(TestCase("ac", "ab", False))
# plus
testLists.append(TestCase("a", "b+", False))
testLists.append(TestCase("b", "b+", True))
# option
testLists.append(TestCase("b", "a?b", True))
testLists.append(TestCase("aab", "a?b", False))
# star
testLists.append(TestCase("b", "a*b", True))
testLists.append(TestCase("aab", "a*b", True))
testLists.append(TestCase("bbb", "a*b", False))
# or
testLists.append(TestCase("b", "a|b", True))
testLists.append(TestCase("aaa", "a|b", False))
testLists.append(TestCase("ab", "(ab|cd)", True))
# [], [^ ]
testLists.append(TestCase("b", "[^a]", True))
testLists.append(TestCase("bcds", "[^a]*", True))
testLists.append(TestCase("ac", "[abcd]+", True))


class TestRegex(unittest.TestCase):
    def test(self):
        for t in testLists:
            regex = Regex(t.str, t.regex)
            print("str is " + t.str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))
            self.assertEqual(regex.build_and_verify(), t.expect_result)


if __name__ == '__main__':
    unittest.main()
