grammar RegularExpr;

//ETAPA LEXICALA
//Am declarat operatorii de reuniune, paranteze, star
REUNION : '|' ;
STAR : '*' ;
OPEN : '(' ;
CLOSED : ')' ;

//Am adaugat si whitespace desi nu este folosit in input
WHITESPACE : [ \t\r\n]+ -> skip ;

//Variabila reprezinta un singur caracter
VAR : [a-z] ;

//ETAPA SINTACTICA
//Am definit gramatica dezambiguizata
//Reuniunea are cea mai mica prioritate in ordinea operatiilor
expr :  c_expr | c_expr REUNION expr ;
//Concatenarea are prioritate mai mare decat reuninunea
c_expr : s_expr | s_expr c_expr ;
//Star-ul are cea mai mare prioritate
s_expr : atom | s_expr STAR ;

//Atom este reprezentat dintr-un caracter sau o alta expresie in paranteze
atom : variabila | inner_expr ;
variabila : VAR ;
inner_expr : OPEN expr CLOSED ;