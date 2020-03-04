from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import *


def regex_to_minimal_dfa(regex_str):
    regex = Regex(regex_str)
    return regex.to_epsilon_nfa().minimize()


def minimal_dfa_and_nfa_intersection(dfa, nfa):
    enfa1 = dfa.to_regex().to_epsilon_nfa()
    enfa2 = nfa.to_regex().to_epsilon_nfa()
    return enfa1.get_intersection(enfa2).to_deterministic()
