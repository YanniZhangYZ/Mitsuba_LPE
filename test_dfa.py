from prototype.nfa import NFA
from prototype.dfa import DFA
from prototype.parse import Verifier
from prototype.dfa_construction import get_jump_table
from prototype.lexical_analysis import Grammar
from test import TestCase
import unittest


testLists = []
# testLists.append(TestCase("T", "R?T", True))
# testLists.append(TestCase("T", "R?TV?", True))

# s = "RTSVDDD"
# reg = "R*T.V?D+"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "RVT"
# reg = "R.T"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "RT"
# reg = "RT"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "RV"
# reg = "RT"
# expect = False
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "R"
# reg = "T+"
# expect = False
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "TTTTT"
# reg = "T+"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "T"
# reg = "R?T"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "T"
# reg = "R*T"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "RRT"
# reg = "R*T"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "TTT"
# reg = "R?T"
# expect = False
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "T"
# reg = "R|T"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "TTT"
# reg = "R|T"
# expect = False
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "T"
# reg = "[^R]"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))

# s = "TVGD"
# reg = "[^R]*"
# expect = True
# nfa = NFA(reg)
# v = Verifier()
# g = Grammar()
# enum_input = g.check_translate_event_string_simple(s)
# jump_table = get_jump_table(nfa.start_node)
# result = v.dfa_match(enum_input, jump_table)
# print("str is " + s + ", regex is " +
#       reg + ", expected = actual " + str(expect == result))
