import sys
from antlr4 import *
from RegularExprLexer import RegularExprLexer
from RegularExprParser import RegularExprParser
from RegularExprEvalVisitor import RegularExprEvalVisitor
from DFA import DFA


def write_dfa(file, dfa):
    """
    Scrie pe rand datele in fisier
    Pe prima linie numarul de stari, apoi lista de stari finale, apoi delta
    :param file: Fisierul in care se scriu datele
    :param dfa: DFA-ul cu datele pastrate
    """
    file.write(str(dfa.number_of_states))
    file.write('\n')
    string = ''
    for x in dfa.final_states:
        string += str(x) + ' '
    file.write(string)
    file.write('\n')
    for k, v in dfa.delta.items():
        string = str(k[0]) + ' ' + str(k[1]) + ' ' + str(v)
        file.write(string)
        file.write('\n')


# Mainul in care deschid fisierele de scriere si citire si apelez transformarea din NFA in DFA
def main():
    # Fisierul in care se afiseaza detaliile NFA-ului
    file_nfa = open(str(sys.argv[2]), 'w')
    # Fisierul in care se afiseaza detaliile DFA-ului
    file_dfa = open(str(sys.argv[3]), 'w')
    # Fisierul din care se citeste REGEXUL
    i = FileStream(sys.argv[1])

    # Parsarea REGEXULUI cu ajutorul ANTLR4
    lexer = RegularExprLexer(i)
    stream = CommonTokenStream(lexer)
    parser = RegularExprParser(stream)
    tree = parser.expr()

    # Evaluarea REGEXULUI cu clasa de vizitare si evaluare creata de mine
    eval_visitor = RegularExprEvalVisitor()
    nfa = eval_visitor.visit(tree)

    # Afisarea NFA-ului
    file_nfa.write(str(nfa))

    # Transformarea NFA-ului obtinut intr-un DFA
    dfa_delta, dfa_nr, dfa_final = nfa.delta_dfa()
    # Variabila in care se memoreaza DFA-ul
    dfa = DFA(dfa_nr, dfa_final, dfa_delta, nfa.alphabet)
    # Afisarea DFA-ului
    write_dfa(file_dfa, dfa)


if __name__ == '__main__':
    main()
