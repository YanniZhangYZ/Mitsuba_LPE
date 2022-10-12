import unittest
from regex import Regex


class TestCase(object):
    def __init__(self, str, regex, expect_result):
        self.str = str
        self.regex = regex
        self.expect_result = expect_result


testLists = []
testLists.append(TestCase("a", "a", True))
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


# testLists.append(RegexMaterial("THISISREGEXTEST", "([A-Z]*|[0-9]+)", True))
# testLists.append(TestCase("a", "^c", True))
# testLists.append(TestCase("c", "^c", False))
# testLists.append(RegexMaterial("ccccc", "[^c]+", False))
# testLists.append(RegexMaterial("ac", "[abcd]+", True))


class TestRegex(unittest.TestCase):
    def test(self):
        for t in testLists:
            regex = Regex(t.str, t.regex)
            print("str is " + t.str + ", regex is " +
                  t.regex + ", expected " + str(t.expect_result))
            self.assertEqual(regex.match(), t.expect_result)


if __name__ == '__main__':
    unittest.main()
