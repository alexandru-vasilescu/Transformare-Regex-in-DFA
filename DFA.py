class DFA:
    """
    Clasa folosita pentru a stoca datele despre un DFA
    """
    def __init__(self, number_of_states, final_states, delta, alphabet):
        self.number_of_states = number_of_states
        self.final_states = final_states
        self.delta = delta
        self.alphabet = alphabet
        self.states = range(self.number_of_states)
