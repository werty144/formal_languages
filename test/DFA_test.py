import unittest
from pyformlang.finite_automaton import *
from pyformlang.regular_expression import Regex
from src.DFA import *


class TestDFA(unittest.TestCase):
    def test_accept(self):
        dfa = DeterministicFiniteAutomaton()

        # Creation of the states
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)

        # Creation of the symbols
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        symb_d = Symbol("d")

        # Add a start state
        dfa.add_start_state(state0)

        # Add two final states
        dfa.add_final_state(state2)
        dfa.add_final_state(state3)

        # Create transitions
        dfa.add_transition(state0, symb_a, state1)
        dfa.add_transition(state1, symb_b, state1)
        dfa.add_transition(state1, symb_c, state2)
        dfa.add_transition(state1, symb_d, state3)

        # Check if a word is accepted
        self.assertTrue(dfa.accepts([symb_a, symb_b, symb_c]))

    def test_regex_to_minimal_dfa(self):
        dfa = regex_to_minimal_dfa("(a|a a b)*")
        symb_a = Symbol("a")
        symb_b = Symbol("b")

        self.assertTrue(dfa.is_deterministic())

        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b, symb_a, symb_a, symb_b]))
        self.assertFalse(dfa.accepts([symb_a, symb_b]))
        self.assertTrue(dfa.accepts([symb_a]))

    def test_minimal_dfa_and_nfa_intersection(self):
        dfa = regex_to_minimal_dfa("(a|a a b)* (c)*")

        nfa = NondeterministicFiniteAutomaton()
        # Declare the states
        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        state4 = State(4)

        # Declare the symbols
        symb_a = Symbol("a")
        symb_b = Symbol("b")
        symb_c = Symbol("c")
        symb_d = Symbol("d")

        # Add a start state
        nfa.add_start_state(state0)
        # Add a final state
        nfa.add_final_state(state4)
        nfa.add_final_state(state3)
        # Add the transitions
        nfa.add_transition(state0, symb_a, state1)
        nfa.add_transition(state1, symb_a, state1)
        nfa.add_transition(state1, symb_b, state1)
        nfa.add_transition(state1, symb_c, state2)
        nfa.add_transition(state1, symb_d, state3)
        nfa.add_transition(state1, symb_b, state4)

        intersection_fa = minimal_dfa_and_nfa_intersection(dfa, nfa)

        self.assertTrue(intersection_fa.is_deterministic())

        self.assertTrue(dfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(nfa.accepts([symb_a, symb_a, symb_b]))
        self.assertTrue(intersection_fa.accepts([symb_a, symb_a, symb_b]))

        self.assertTrue(dfa.accepts([symb_c, symb_c]))
        self.assertFalse(intersection_fa.accepts([symb_c, symb_c]))

        self.assertTrue(nfa.accepts([symb_a, symb_b]))
        self.assertFalse(intersection_fa.accepts([symb_a, symb_d]))


if __name__ == '__main__':
    unittest.main()
