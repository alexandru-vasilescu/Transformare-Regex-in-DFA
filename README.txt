Vasilescu Alexandru Madalin - 331CB
----------------------------------------------TEMA 3-----------------------------------------------

Am rezolvat tema 3 cu ajutorul utilitarului predat la curs "ANTLR4". Pe forum s-a spus ca putem folosi acest tool.
In rezolvarea temei am lucrat in fisierele "RegularExpr.g4", "RegularExprEvalVisitor.py", "NFA.py" si "main.py".
Fisierele "NFA.py", "DFA.py" si "main.py" le-am preluat din TEMA 2(Am decis sa pastrez si README-ul de la tema 2 pentru claritate).
Restul fisierelor au fost generate de antlr4 si nu am lucrat direct in ele, doar am folosit elemente din ele in rezolvarea mea.

Am inceput prin a scrie gramatica in fisierul "RegularExpr.g4".
Mi-am definit tokenii de reuniune, star, paranteze si whitespace(chit ca in fisierele de input am vazut ca nu apare).
Am definit variabila ca fiind orice litera mica de la 'a' la 'z'.
Apoi am definit tranzitiile.
Expr reprezinta starea initiala a gramaticii. De aici se poate face o reuniune sau trece in c_expr.
C_expr reprezinta un nonterminal unde se poate face o concatenare sau trece intr-un s_expr.
S_expr reprezinta un nonterminal unde se poate face operatia de star peste o expresie sau trece intr-un atom.
Un atom este reprezentat de o variabila sau de un inner_expr.
Inner_expr reprezinta o expresie aflata in parenteze.
Astfel am definit gramatica dezambiguizata pentru a face operatiile in ordinea corecta.
Astfel prima data se realizeaza parantezele, apoi star-ul, concatenarea si la final reuniunea.

Folosind utilitarul antlr4 mi s-au generat fisierele de lexer si parser, precum si un visitor.
Apoi eu am cret o noua clasa RegularExprEvalVisitor care extinde clasa visitor deja creata de antlr4.
In cadrul clasei create de mine am facut implementarea pentru fiecare tip de nod din arborele de parsare.

Variabilele se salveaza ca un caracter (c) si apoi creez un NFA.
Acest NFA are 2 stari, o stare finala [1], o tranzitie din starea initiala pe caracterul c si alfabet format doar din caracterul c.

Inner_expr viziteaza expresia din interiorul parantezelor.

Atomii verifica daca exista un inner_expr si il viziteaza.
Daca nu exista intoarce un NFA creat dintr-o variabila.

S_expr verifica daca exista o expresie cu star. Daca exista viziteaza expresia si modifica NFA-ul format din expresia de sub star.
Sub star folosesc alta S_expr. Astfel pot avea oricate star-uri la rand(a****), chiar daca repetari de star nu modifica comportamentul.
Daca nu exista o expresie cu star viziteaza atomul si intoarce NFA-ul format de Atom.

C_expr verifica daca exista o concatenare. Daca exista viziteaza expresiile si creaza un nou NFA format din cele 2 NFA-uri obtinute din expresii.
Daca nu exista o concatenare vizireaza s_expr si intoarce NFA-ul format de acea expresie.

Expr verifica daca exista o reuniune. Daxa exista viziteaza expresiile si creaza un nou NFA format din cele 2 NFA-uri obtinute din expresii.
Daca nu exista o reuniune viziteaza c_expr si intoarce NFA-ul fomrat de acea expresie.

In NFA am modificat __str__ pentru a-mi intoarce exact stringul in formatul cerut de enunt
(Pe prima linie numarul de stari. Pe a doua lista de stari finale. Pe urmatoarele tranzitiile).
Am adauga functiile de reunion, concatenation, star. In rest este identic ca la TEMA 2. Descrierea se poate citi mai jos.

In metoda concatenation primesc un NFA si creez un nou NFA din cel primit ca parametru si cel pe care se apeleaza metoda(self).
Concatenarea a doua NFA-uri am facut-o cum a fost predata la curs.
Din starile finale a primului NFA creez cate o tranzitie pe EPSILON catre starea initiala a celui de-al doilea NFA.
Toate starile din cel de-al doilea NFA le-am translatat cu numarul de stari din primul NFA.
Adica daca am 2 NFA cu starile [0,1] si [0,1], dupa translatare o sa folosesc starile [0,1] si [2,3]. Din 1 spre 2 am tranzitie pe EPS.

Creez un nou numar de stari ca suma dintre cele 2.
Creez o noua lista de stari finale formata din starile finale ale celui de-al doilea NFA translatate.
Creez un nou dictionar de tranzitii in care copiez tranzitiile din primul NFA.
Copiez tranzitiile din cel de-al doilea NFA translatate.
Creez o noua tranzitie din starea finala a primului NFA in starea initiala a celui de-al doilea pe sirul vid.
Reunesc alfabetele intr-o multime pentru a nu avea duplicate.
Creez noul nfa cu atributele noi calculate.

In metoda reunion primesc un NFA si creez un nou NFA din cel primit ca parametru si cel pe care se apeleaza metoda(self).
Reuniune a doua NFA-uri am facut-o cum a fost predata la curs.
Creez o noua stare initiala si tranzitii din aceasta catre cele 2 stari initiale alea automatelor initiale pe EPS.
Creez o noua stare finala si tranzitii din cele 2 automate initiale catre starea noua finala pe EPS.
Translatez starile.
Daca am initial 2 NFA-uri cu starile [0,1] si [0,1], dupa translatare si adaugarea de stari o sa am:
- 0 stare initiala
- [1, 2] starile din primul automat (adaug 1)
- [3, 4] starile din cel de-al doilea automat (adaug numarul de stari din primul + 1)
- 5 stare finala

Creez un nou numar de stari ca suma dintre cele 2 la care adaug 2(starea finala si starea initiala).
Creez o noua lista de stari finale formata din ultima stare din automat.
Creez un nou dictionar de tranzitii. Adaug tranzitiile din starea initiala si catre starea finala.
Copiez tranzitiile din cele 2 NFA-uri translatate.
Reunesc alfabetele intr-o multime pentru a nu avea duplicate.
Creez un nou nfa din atributele noi calculate.

In metoda star creez un nou NFA din cel pe care se apeleaza metoda(self).
NFA-ul star se creeaza cum a fost predat la curs.
Creez o noua stare initiala si o noua stare finala.
Din starea initiala noua am o tranzitie catre starea initiala din NFA-ul initial si catre stare finala noua.
Din starea finala veche creez o tranzitie catre starea initiala veche si catre starea finala noua.
Translatez starile din NFA-ul initial cu 1.
Daca am initial un NFA cu starile [0,1], dupa trasnalate o sa am:
-0 stare initiala
-[1,2] stari intermediare din NFA-ul initial (adaug 1)
-3 stare finala

Creez un nou numar de stari ca numarul de stari initial la care adaug 2(starea finala si initiala).
Creez o noua lista de stari finale formata din ultima stare din automat.
Creez un nou dictionar de tranzitii. Adaug tranzitiile din starea initiala si catre starea finala.
Copiez tranzitiile din NFA-ul initial si le translatez.
Copiez alfabetul.
Creez un nou nfa din atributele noi calculate.

In main.py. Deschid fisierele pentru scrierea NFA-ului si DFA-ului.
Deschid fisierul din care se citeste REGEXUL.
Parsez REGEXUL (ca la curs) cu ajutorul claselor create de antlr4.
Folosesc clasa mea de EvalVisitor pentru a vizita arborele de parsare si a crea un NFA.
Afisez NFA-ul. Il transform apoi intr-un DFA folosind tema 2.
Afisez DFA-ul.


----------------------------------------------TEMA 2-----------------------------------------------

Am folosit putin din scheletul de la laboratorul 5. 
De asemenea functiile step si epsilon_closure implementate in cadrul aceluiasi laborator.

In main.py am creat o functie de parsare a inputului din fisier si una de scriere a outputului in fisier in formatul dorit. 
Se mai pastreaza un obiect NFA si un obiect DFA in care se tin datele si se apeleaza functiile necesare pentru transformare. 

In DFA.py am creat o clasa pentru a pasta toate datele DFA-ului, nou creat, organizate.

In NFA.py am creat clasa NFA. 
Aici am functia care realizeaza tranzitia intr-un pas pe un caracter sau pe epsilon daca nu avem caractere in cuvantul din configuratie. 
Urmatoare functie, epsilon_closure imi calculeaza toate inchiderile epsilon ale unei stari. 
Se adauga intr-o multime starile pe rand apelandu-se step de mai multe ori. 
Cand nu se mai adauga de la o iteratie la alta stari in multime se termina functia.
Functia transition primeste o lista de stari si imi intoarce o lista cu toate starile in urma unei tranzitii pe un caracter intr-un pas. 
Se adauga la final toate inchiderile epsilon ale starilor actuale.
Functia dfa_final primeste un dictionar si intoarce o lista cu stari finale ale dfa-ului

Dictionarul are key = tuplu cu starile din NFA din care e formata starea in DFA 
		value = numarul starii in DFA

Eu imi creez stari in DFA din mai multe stari in NFA. 
Starea initiala din DFA este inchiderea epsilon a starii intiale din NFA. 
Apoi verific pe fiecare stare din multimea starii intiale, ce tranzitii se face pe fiecare caracter din alfabet. 
Cu rezultatul pentru feicare litera creez o stare noua si ii asignez un index. 
Si continui cu starile pana sunt realizate toate tranzitiile de pe toate starile.

Functia delta_dfa face in principiu ce am scris mai sus. 
Folosesc 2 dictionare in care retin delta_DFA-ului nou si indicele echivalent stari formate din NFA. 
Incep cu starea inchiderea epsilon a starii initiale a NFA-ului. 
Pentru fiecare stare din multimea de stari care se updateaza la fiecare pas si pentru fiecare litera din alfabet caut tranzitiile. 
Daca am gasit o stare care nu se afla in lista o adaug. 
Daca gasesc o stare care nu se gaseste in dictionar ii asignez un index. 
La final intorc functia delta, numarul de stari din dfa si lista starilor finale din DFA.