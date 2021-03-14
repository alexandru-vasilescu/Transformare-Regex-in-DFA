from RegularExprVisitor import RegularExprVisitor
from RegularExprParser import RegularExprParser
from NFA import NFA


class RegularExprEvalVisitor(RegularExprVisitor):
    """
    Clasa are rolul de a vizita arborele de parsare.
    Evalueaza fiecare nod.
    Variabilele sunt transformate in NFA-uri cu o singura stare pe acel caracter.
    Restul operatiilor prelucreaza NFA-ul existent.
    """

    def visitVariabila(self, ctx: RegularExprParser.VariabilaContext):
        """
        Trateaza o frunza din arborele de parsare reprezentata de o variabila si creaza un
        NFA cu o singura tranzitie pe caracterul din frunza
        :return: Un NFA cu o tranzitie pe caracterul din frunza
        """
        c = str(ctx.VAR())
        number_of_states = 2
        final_state = [1]
        delta = {(0, c): [1]}
        alphabet = [c]
        n = NFA(number_of_states, final_state, delta, alphabet)
        return n

    def visitAtom(self, ctx: RegularExprParser.AtomContext):
        """
        Trateaza un nod de tip atom.
        Daca acest atom este format dintr-o pereche de paranteze viziteaza expresia din interior
        Daca nu, inseamna ca este format dintr-o variabila si viziteaza variabila
        :return: Un NFA cu o expresie regulata dintre paranteze sau
        cu o expresie creata dintr-o singura variabila
        """
        inner = ctx.inner_expr()
        if inner:
            return self.visit(ctx.inner_expr())
        else:
            return self.visit(ctx.variabila())

    def visitS_expr(self, ctx: RegularExprParser.S_exprContext):
        """
        Trateaza un nod cu o expresie cu Kleen Star.
        Poate fi formata dintr-un atom sau o alta expresie cu star.
        Daca este formata dintr-o expresie cu star vizitam expresia de sub star.
        In acest caz se modifica NFA-ul de sub star pentru a simula starul.
        Altfel, este un atom si vizitam atomul.
        :return: Un NFA care reprezinta o expresie regulata cu star sau
        un NFA format de un atom
        """
        atom = ctx.atom()
        star = ctx.s_expr()
        if star:
            v = self.visit(star)
            return v.star()
        else:
            return self.visit(atom)

    def visitC_expr(self, ctx: RegularExprParser.C_exprContext):
        """
        Trateaza un nod cu o expresie de concatenare.
        Poate fi formata dintr-un star sau o concatenare dintre un star si alta concatenare.
        Daca este formata dintr-o concatenare vizitam ambii fii ai concatenarii.
        In acest caz se creaza un nou NFA care concateneaza cele 2 NFA-uri existente.
        Altfel, este un star si vizitam expresia de tip star.
        :return: Un NFA concatenat din cele 2 expresii sau
        un NFA format de un star
        """
        star = ctx.s_expr()
        concat = ctx.c_expr()
        if concat:
            v1 = self.visit(star)
            v2 = self.visit(concat)
            return v1.concatenation(v2)
        else:
            return self.visit(star)

    def visitExpr(self, ctx: RegularExprParser.ExprContext):
        """
        Trateaza un nod cu o expresie cu reuniune.
        Poate fi formata dintr-o concatenare sau o reuniune dintre o concatenare si alta reuniune.
        Daca este formata dintr-o reuniune vizitam ambii fii ai reuniunii.
        In acest caz se creaza un nou NFA care reuneste cele 2 NFA-uri existente.
        Altfel, este o concatenare si vizitam expresia de concatenare.
        :return: Un NFA reuniunea dintre cele 2 expresii sau
        un NFA format dintr-o concatenare
        """
        concat = ctx.c_expr()
        reunion = ctx.expr()
        if reunion:
            v1 = self.visit(concat)
            v2 = self.visit(reunion)
            return v1.reunion(v2)
        else:
            return self.visit(concat)

    def visitInner_expr(self, ctx: RegularExprParser.Inner_exprContext):
        """
        Trateaza o expresie regulata cu paranteze
        Vizitam expresia din interiorul parantezei
        :return: Un NFA cu expresia din paranteza
        """
        return self.visit(ctx.expr())
