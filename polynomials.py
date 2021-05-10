from fraction import frac
from collections import deque


class Mono:

    @staticmethod
    def lex(mono):
        return mono.exp
    @staticmethod
    def grlex(mono):
        order = sum(mono.exp)
        return (order, mono.exp)

    def __init__(self, alpha, exp):
        if type(alpha) == int: alpha = frac(alpha)
        self.alpha = alpha
        self.exp = exp

    def __add__(self, other):
        assert self.exp == other.exp, "bruh"
        return Mono(self.alpha + other.alpha, self.exp)

    def __mul__(self, other):
        order = tuple([a + b for (a, b) in zip(self.exp, other.exp)])
        return Mono(self.alpha * other.alpha, order)

    def __mod__(self, other):
        assert other.alpha != 0, "zero division"
        for i in range(len(self.exp)):
            if self.exp[i] < other.exp[i]:
                return 1
        return 0

    def __truediv__(self, other):
        assert self % other == 0, "not divisible"
        order = []
        for i in range(len(self.exp)):
            order.append(self.exp[i] - other.exp[i])
        return Mono(self.alpha / other.alpha, tuple(order))

    @staticmethod
    def lcm(a, b):
        order = []
        for i in range(len(a.exp)):
            order.append(max(a.exp[i], b.exp[i]))
        return Mono(frac(1), tuple(order))

    def __eq__(self, other):
        return self.alpha == other.alpha and self.exp == other.exp

    def __repr__(self):
        var_names = "xyzwabcdef"
        out = repr(self.alpha)
        for i in range(len(self.exp)):
            if self.exp[i] > 0:
                out += "*" + var_names[i] 
                if self.exp[i] > 1:
                    out += "^" + str(self.exp[i])
        return out



class Poly:
    def __init__(self, terms):
        self.terms = terms
        self.simplify()

    def check(self, terms=None):
        if terms is None: terms = self.terms
        for term in terms:
            if type(term) != Mono:
                return False
        return True

    def simplify(self):
        self.check()
        if self.terms == []:
            return
        new_terms = deque(sorted(self.terms, key=Mono.lex, reverse=True))
        self.check(new_terms)
        self.terms = [new_terms.popleft()]
        while len(new_terms) > 0:
            term = new_terms.popleft()
            if self.terms[-1].exp == term.exp:
                self.terms[-1] += term
            else:
                self.terms.append(term)
        self.terms = [term for term in self.terms if term.alpha != 0]

    def LT(self):
        return self.terms[0]

    def __neg__(self):
        return Poly([Mono(-term.alpha, term.exp) for term in self.terms])

    def __add__(self, other):
        return Poly(self.terms + other.terms)
    
    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        new_terms = [A * B for A in self.terms for B in other.terms]
        return Poly(new_terms)

    def __mod__(self, others):
        return self.divide(others)[1]

    def divide(poly, others):
        qs = [Poly([]) for _ in range(len(others))]
        r = Poly([])
        while len(poly.terms) > 0:
            term = poly.LT()
            for i, p in enumerate(others):
                if term % p.LT() == 0:
                    factor = term / p.LT()
                    qs[i] += Poly([factor])
                    poly -= Poly([factor]) * p
                    break
            else:
                poly -= Poly([term])
                r += Poly([term])
        return (qs, r)

    def __eq__(self, other):
        if len(self.terms) != len(other.terms):
            return False
        for a, b in zip(self.terms, other.terms):
            if a != b:
                return False
        return True

    def is_zero(self):
        return self.terms == []

    def scalar_multiple(self, alpha):
        return Poly([Mono(alpha * term.alpha, term.exp) for term in self.terms])

    def __repr__(self):
        #print("terms =", self.terms)
        if self.terms == []:
            return "0"
        out = ""
        for term in self.terms:
            out += repr(term)
        return out

class Ideal:

    def __init__(self, gen, order=Mono.lex):
        self.gen = gen
        self.order = order
    
    @staticmethod
    def s_poly(p, q):
        lcm = Mono.lcm(p.LT(), q.LT())
        return Poly([lcm / p.LT()]) * p - Poly([lcm / q.LT()]) * q

    def grobner_basis(self):
        if len(self.gen) <= 1:
            return self.gen
        basis = self.gen
        first, second = 0, 1
        while second < len(basis):
            poly = Ideal.s_poly(basis[first], basis[second])
            #print(f"S(f{first + 1}, f{second + 1}) =", poly)
            rem = poly.divide(basis)[1]
            #print("r =", rem)
            if not rem.is_zero():
                basis.append(rem)
            first += 1
            if first == second:
                second += 1
                first = 0
        return basis

    @staticmethod
    def minimal(basis):
        remove = []
        for i in range(len(basis)):
            for j in range(len(basis)):
                if i != j and basis[i].LT() % basis[j].LT() == 0:
                    remove.append(i)
                    break
        minimal_basis = []
        idx = 0
        for i in range(len(basis)):
            if idx < len(remove) and i == remove[idx]:
                idx += 1
            else:
                minimal_basis.append(basis[i])
        return minimal_basis

    @staticmethod
    def reduced(basis):
        minimal = Ideal.minimal(basis)
        for i in range(len(minimal)):
            minimal[i] = minimal[i] % (minimal[:i] + minimal[i + 1:])
            minimal[i] = minimal[i].scalar_multiple(frac(1) / minimal[i].LT().alpha)
        return minimal
