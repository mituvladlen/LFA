import itertools

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def is_deterministic(self):
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                if len(next_states) > 1:
                    return False
        return True

    def to_dfa(self):
        dfa_states = set()
        dfa_transitions = {}
        state_map = {}

        queue = [frozenset([self.start_state])]
        while queue:
            current = queue.pop(0)
            dfa_states.add(current)
            state_map[current] = "{" + ",".join(current) + "}"

            transitions = {}
            for symbol in self.alphabet:
                next_state = frozenset(itertools.chain.from_iterable(self.transitions.get(state, {}).get(symbol, []) for state in current))
                if next_state:
                    transitions[symbol] = next_state
                    if next_state not in dfa_states and next_state not in queue:
                        queue.append(next_state)
            dfa_transitions[current] = transitions

        dfa_final_states = {state for state in dfa_states if any(s in self.final_states for s in state)}
        return FiniteAutomaton(dfa_states, self.alphabet, dfa_transitions, frozenset([self.start_state]), dfa_final_states), state_map

    def print_as_regular_grammar(self):
        print("Regular Grammar:")
        print("Non-terminals:", list(self.states))
        print("Terminals:", list(self.alphabet))
        print("Productions:")
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    print(f"{state} : {symbol}{next_state}")
            if state in self.final_states:
                print(f"{state} : ε")  # Epsilon transition for final states

    def print_as_fa(self, state_map):
        print("Converted NFA to DFA:")
        print("States:", [state_map[state] for state in self.states])
        print("Alphabet:", list(self.alphabet))
        print("Transitions:")
        for state, transitions in self.transitions.items():
            for symbol, next_state in transitions.items():
                print(f"{state_map[state]}--{symbol}-->{state_map[next_state]}")

# Define NFA
states = {"q0", "q1", "q2", "q3"}
alphabet = {"a", "b", "c"}
transitions = {
    "q0": {"a": {"q0", "q1"}},
    "q1": {"b": {"q2"}},
    "q2": {"a": {"q2"}, "c": {"q3"}},
    "q3": {"c": {"q3"}}
}
start_state = "q0"
final_states = {"q3"}

nfa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
nfa.print_as_regular_grammar()

if nfa.is_deterministic():
    print("Finite Automaton is deterministic")
else:
    print("Finite Automaton is non-deterministic")

dfa, state_map = nfa.to_dfa()
dfa.print_as_fa(state_map)
