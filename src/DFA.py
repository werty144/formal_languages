from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import *


def regex_to_minimal_dfa(regex_str):
    regex = Regex(regex_str)
    return regex.to_epsilon_nfa().minimize()


def minimal_dfa_and_nfa_intersection(dfa, nfa):
    return dfa.to_regex().to_epsilon_nfa().get_intersection(nfa.to_regex().to_epsilon_nfa()).to_deterministic()
