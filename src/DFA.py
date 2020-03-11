from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import *


def regex_to_minimal_dfa(regex_str):
    regex = Regex(regex_str)
    return regex.to_epsilon_nfa().minimize()
