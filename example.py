from polynomials import Mono, Poly, Ideal

print("Primer 1:")

terms1 = [Mono(1, (3,0,0)), Mono(-2, (1,1,0))]
terms2 = [Mono(1, (2,1,0)), Mono(-2, (0,2,0)), Mono(1, (1,0,0))]

poly1 = Poly(terms1)
poly2 = Poly(terms2)


ideal = Ideal([poly1, poly2])
basis = ideal.grobner_basis()
print(basis)
print(Ideal.minimal(basis))
print(Ideal.reduced(basis))

print("Primer 2:")

terms1 = [Mono(1, (2,1,0)), Mono(-1, (0,0,3))]
terms2 = [Mono(2, (1,1,0)), Mono(-4, (0,0,1)), Mono(-1, (0,0,0))]
terms3 = [Mono(1, (0,0,1)), Mono(-1, (0,2,0))]
terms4 = [Mono(1, (3,0,0)), Mono(-4, (0,1,1))]

poly1 = Poly(terms1)
poly2 = Poly(terms2)
poly3 = Poly(terms3)
poly4 = Poly(terms4)

ideal = Ideal([Poly(terms1), Poly(terms2), Poly(terms3), Poly(terms4)])
basis = ideal.grobner_basis()
print(basis)
print(Ideal.minimal(basis))
print(Ideal.reduced(basis))