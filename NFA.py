class NFA:
    """
    Clasa folosita pentru a stoca datele despre un NFA
    """

    def __init__(self, number_of_states, final_states, delta, alphabet):
        self.number_of_states = number_of_states
        self.final_states = final_states
        self.delta = delta
        self.initial_state = 0
        self.states = list(range(self.number_of_states))
        self.alphabet = [x for x in alphabet if x]

    def step(self, configuration):
        """
        Primeste o configuratie si intoarce lista tuturor configuratiilor in care se poate ajunge
        intr-un singur pas
        :param configuration: Configuratia actuala
        :return: Lista configuratii dupa un pas
        """
        # Lista in care retin configuratiile cand am un caracter in cuvantul din configuratie
        list_with_charactes = []
        # Lista in care retin configuratiile cand am epsilon in configuratie
        list_with_epsilon = []
        if configuration[1]:
            list_with_charactes = self.delta.get((configuration[0], configuration[1][0]))
        else:
            list_with_epsilon = self.delta.get((configuration[0], ''))
        # Lista finala in concatenez cele 2 liste
        ls = []
        if list_with_charactes:
            ls.extend([(x, configuration[1][1:]) for x in list_with_charactes])
        if list_with_epsilon:
            ls.extend([(x, configuration[1]) for x in list_with_epsilon])
        return ls

    def epsilon_closure(self, state):
        """
        Gaseste inchiderea epsilon pentru o stare data
        :param state: Starea pentru care se cauta inchiderea epsilon
        :return: Multimea de inchidere epsilon
        """
        # Daca starea nu este in multimea de stari se afiseaza un mesaj
        if state not in self.states:
            print(f'{state} is not in States List')
            return None
        # Multimea in care se retin starile in care se poate ajunge pe epsilon
        states = {state}
        # Lista cu starile in care se poate ajunge intr-un pas pe epsilon
        ls = [x[0] for x in self.step((state, ''))]
        # Se executa inca un pas pana am gasit toate starile
        while not set(ls).issubset(states):
            # Adaug in multime starile gasite dupa inca un pas
            states = states.union(set(ls))
            laux = []
            # Pentru fiecare stare din lista mai execut un pas pe epsilon si le pastrez pe toate intr-o lista
            for x in ls:
                laux += [x[0] for x in self.step((x, ''))]
            ls = laux
        return states

    def transition(self, states, character):
        """
        Intoarce o lista cu toate starile in care se poate ajunge dintr-o multime de stari pe un caracter
        :param states: Multime de stari initiale
        :param character: Caracterul pe care se face tranzitia
        :return: Multime de stari dupa tranzitie
        """
        states_after_transition = set()
        # Pentru fiecare stare din multimea de stari fac o tranzitie de un pas cu caracterul dat
        for x in states:
            # Lista de stari dupa un pas
            ls = [x[0] for x in self.step((x, character))]
            states_after_transition = states_after_transition.union(set(ls))
        # Pentru fiecare stare din multime adaugam si inchiderea epsilon corespunzatoare
        for x in states_after_transition:
            states_after_transition = states_after_transition.union(self.epsilon_closure(x))
        return states_after_transition

    def dfa_final(self, dfa_state):
        """
        Intoarce o lista de stari finale ale unui DFA folosind starile finale ale unui NFA.
        :param dfa_state: Dictionar(key = tuplu de stari din NFA din care e formata starea : value = numarul
        starii in DFA)
        :return: Lista de stari finale ale DFA-ului
        """
        final = []
        for k, v in dfa_state.items():
            for i in k:
                if i in self.final_states:
                    final.append(v)
        return final

    def delta_dfa(self):
        """
        Calculeaza parametrii unui DFA dintr-un NFA
        :return: Intoarce delta pentru un DFA, numarul de stari ale DFA-ului, Lista stari finale ale DFA-ului
        """
        # Numarul starii curente
        index = 0
        # Noul dictionar al functiei de tranzitii pentru DFA
        delta = dict()
        # Pentru fiecare stare alcatuita din mai multe stari din NFA ii atribui un index corespunzator starii din DFA
        dfa_state = dict()
        # Incep de la inchiderea epsilon a starii initiale care are index 0 in DFA
        dfa_state[tuple(self.epsilon_closure(self.initial_state))] = index
        # Lista in care tin toate starile care urmeaza sa le verific
        states = [tuple(self.epsilon_closure(self.initial_state))]
        index += 1
        # Iterez prin lista de stari si prin alfabet
        for state in states:
            for letter in self.alphabet:
                # Pentru fiecare stare din tuplul de stari si fiecare litera din dictionar formez lista dupa un pas
                state1 = tuple(self.transition(state, letter))
                # Verific daca starea mea exista in dictionarul de stari ale DFA-ului
                if dfa_state.get(state1) is None:
                    # Daca nu o gasesc ii atribui un nou index
                    dfa_state[state1] = index
                    index += 1
                # Adaug in dictionar pe starea actuala si litera, starea urmatoare
                delta[(dfa_state[state], letter)] = dfa_state[state1]
                # Daca starea urmatoare nu exista in lista de stari o adaug
                if state1 not in states:
                    states.append(state1)
        return delta, len(dfa_state), self.dfa_final(dfa_state)

    def __str__(self):
        """
        :return: Detaliile despre NFA in formatul cerut
        """
        s = ""
        s += str(self.number_of_states) + "\n"
        for i in self.final_states:
            s += str(i) + " "
        s += "\n"
        for k, v in self.delta.items():
            s += str(k[0]) + " "
            if k[1]:
                s += k[1]
            else:
                s += "eps"
            for x in v:
                s += " " + str(x)
            s += "\n"
        return s

    def concatenation(self, nfa2):
        """
        :param nfa2: un NFA
        :return: Concatenarea obiectului pe care se apeleaza cu NFA-ul primit parametru
        """
        # Se calculeaza numarul de stari ca suma dintre numarul de stari ale celor 2 NFA-uri
        new_number_of_states = self.number_of_states + nfa2.number_of_states

        # Se calculeaza lista de stari finale ca fiind lista de stari ale celui de-al doilea NFA
        # Se aduna la starile curente numarul de stari din primul NFA pentru a face o tranzitie
        new_final_states = [x + self.number_of_states for x in nfa2.final_states]

        # Se copiaza in noul delta tranzitiile primului NFA
        new_delta = self.delta
        # Se copiaza in noul delta tranzitiile celui de-al doilea NFA translatate
        for k, v in nfa2.delta.items():
            new_delta[(k[0] + self.number_of_states, k[1])] = [x + self.number_of_states for x in v]
        # Se creaza tranzitii pe epsilon din starile finale ale primului NFA
        # in starea initiala a celui de-al doilea NFA
        for x in self.final_states:
            new_delta[x, ''] = [self.number_of_states]

        # Se reunesc alfabetele pastrandu-se doar o data toate variabilele
        new_alphabet = set(self.alphabet).union(nfa2.alphabet)
        # Se creaza un nou NFA din concatenarea celor 2
        new_nfa = NFA(new_number_of_states, new_final_states, new_delta, list(new_alphabet))
        return new_nfa

    def reunion(self, nfa2):
        """
        :param nfa2: NFA
        :return: Reuniunea obiectului pe care se apeleaza cu NFA-ul primit parametru
        """
        # Numarul de stari din primul automat
        nr1 = self.number_of_states
        # Numarul de stari adunat din cele 2 automate + o noua stare initiala + o noua stare finala
        new_number_of_states = nr1 + nfa2.number_of_states + 2

        # Starea finala este ultima stare (numarul de stari - 1)
        new_final_states = [new_number_of_states - 1]
        # Declar dictionarul de tranzitii

        new_delta = dict()
        # Declar tranzitie din starea initiala 0 in starile initiale ale celor 2 NFA-uri
        new_delta[(0, '')] = [self.initial_state + 1, nfa2.initial_state + nr1 + 1]
        # Copiez tranzitiile primului NFA cu starile translatate cu 1.
        for k, v in self.delta.items():
            new_delta[(k[0] + 1, k[1])] = [x + 1 for x in v]
        # Copiez tranzitiile celui de-al doilea NFA cu starile translatate cu numarul de stari din primul automat
        for k, v in nfa2.delta.items():
            new_delta[(k[0] + nr1 + 1, k[1])] = [x + nr1 + 1 for x in v]
        # Creez tranzitii din toate starile finale ale primului automat in starea finala noua
        for x in self.final_states:
            new_delta[(x + 1, '')] = [new_number_of_states - 1]
        # Creez tranzitii din toate starile celui de-al doilea NFA in starea finala noua
        for x in nfa2.final_states:
            new_delta[(x + nr1 + 1, '')] = [new_number_of_states - 1]
        # Se reunesc alfabetele pastrandu-se doar o data toate variabilele

        new_alphabet = set(self.alphabet).union(nfa2.alphabet)
        # Se creeaza un nou NFA din reuniunea celor 2
        new_nfa = NFA(new_number_of_states, new_final_states, new_delta, list(new_alphabet))
        return new_nfa

    def star(self):
        """
        :return: NFA-ul original peste care s-a aplicat regula Kleen Star
        """
        # Numarul de stari din NFA + o noua stare initiala + o noua stare finala
        new_number_of_states = 2 + self.number_of_states
        # Lista de stari finale reprezentata de ultima stare

        new_final_states = [new_number_of_states - 1]
        # Dictionarul de tranzitii

        new_delta = dict()
        # Creez o tranzitie din starea initiala in prima stare a automatului existent si in starea finala noua
        new_delta[(0, '')] = [1, new_number_of_states - 1]
        # Copiez starile din NFA-ul existent si le translatez
        for k, v in self.delta.items():
            new_delta[(k[0] + 1, k[1])] = [x + 1 for x in v]
        # Creez tranzitii din starile finale ale automatului initial spre starea finala
        # si spre starea initiala a automatului initial pentru a se putea repeta
        for x in self.final_states:
            new_delta[(x + 1, '')] = [1, new_number_of_states - 1]
        # Copiez alfabetul

        new_alphabet = set(self.alphabet)
        # Creez un nou NFA cu modificarile facute
        new_nfa = NFA(new_number_of_states, new_final_states, new_delta, list(new_alphabet))
        return new_nfa
