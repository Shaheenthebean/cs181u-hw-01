from propositional_logic import *

T = BoolConst(True)
F = BoolConst(False)

A = BoolVar("A")
B = BoolVar("B")
C = BoolVar("C")


# helper function to test for
# duplicates in a list
def allDistinct(var_list):
    return len(var_list) == len(set(var_list))

def test_isAtom():
	assert T.isAtom()
	assert F.isAtom()
	assert A.isAtom()
	assert B.isAtom()
	assert not Not(A).isAtom()
	assert not Not(Not(A)).isAtom()
	assert not And(A,B).isAtom()
	assert not Iff(T, And(A,B)).isAtom()


def test_isLiteral():
	assert T.isLiteral()
	assert F.isLiteral()
	assert A.isLiteral()
	assert Not(A).isLiteral()
	assert Not(T).isLiteral()
	assert not Not(Not(T)).isLiteral()
	assert not And(T, F).isLiteral()

def test_getVars():
	assert T.getVars() == []  and allDistinct(T.getVars())
	assert Not(T).getVars() == [] and allDistinct(Not(T).getVars())
	assert And(T,F).getVars() == [] and allDistinct(And(T,F).getVars())
	assert A.getVars() == [A] and allDistinct(A.getVars())
	assert And(A,F).getVars() == [A] and allDistinct(And(A,F).getVars())

	# for more than one variable convert
	# list to set in case order is different
	assert set(And(A,B).getVars()) == set([A,B]) and allDistinct(And(A,B).getVars())
	assert set(Iff(And(A,Or(B,T)), C).getVars()) == set([A,B,C]) and allDistinct(Iff(And(A,Or(B,T)), C).getVars())

def test_isNNF():
	assert T.isNNF()
	assert F.isNNF()
	assert A.isNNF()
	assert Not(T).isNNF()
	assert Not(A).isNNF()
	assert And(A,B).isNNF()
	assert Or(Not(C),A).isNNF()
	assert not Not(Not(A)).isNNF()
	assert not And(Not(Not(T)),Not(A)).isNNF()
	assert not Not(And(A,B)).isNNF()
	assert not Iff(A,T).isNNF()

def test_NNF():
	assert T.NNF().isNNF()
	assert A.NNF().isNNF()
	assert Not(A).NNF().isNNF()
	assert Not(T).NNF().isNNF()
	assert And(A,B).NNF().isNNF()
	assert Or(Not(C),A).NNF().isNNF()
	assert Not(Not(A)).NNF().isNNF()
	assert And(Not(Not(T)),Not(A)).NNF().isNNF()
	assert Not(And(A,B)).NNF().isNNF()

	assert Not(T.NNF()).isNNF()
	assert Not(A.NNF()).isNNF()
	assert Not(Not(Not(A)).NNF()).isNNF()

	# assert not Iff(A,T).NNF().isNNF() // this should be an NNF
	assert Iff(A,T).NNF().isNNF()
	assert not Not(Not(A).NNF()).isNNF()
	assert not Not(Not(T).NNF()).isNNF()
	assert not Not(And(A,B).NNF()).isNNF()
	assert not Not(Iff(A,T).NNF()).isNNF()
	assert not Not(Or(Not(C),A).NNF()).isNNF()
	assert not Not(And(Not(Not(T)),Not(A)).NNF()).isNNF()
	assert not Not(Not(And(A,B)).NNF()).isNNF()

	# More test
	assert  Not(Or(Not(Not(T)),Not(A))).NNF().isNNF()
	assert  Not(And(Not(C),A)).NNF().isNNF()
	assert  Implies(A,T).NNF().isNNF()

def test_removeImplications():

	assert T.removeImplications() == T
	assert A.removeImplications() == A
	assert Not(A).removeImplications() == Not(A)
	assert And(A,F).removeImplications() == And(A,F)
	assert Implies(A,B).removeImplications() == Or(Not(A),B)

	f = Not(Implies(A,Or(C,B)))
	f_ = f.removeImplications()
	assert f_ == Not(Or(Not(A), Or(C, B)))

	d = Iff(A,B)
	d_ = d.removeImplications()

	assert d_ == And(Or(Not(A), B), Or(Not(B), A))

def test_eval():
	interp_1 = {A : T, B : F}

	assert T.eval(interp_1) == T
	assert F.eval(interp_1) == F
	assert A.eval(interp_1) == T
	assert B.eval(interp_1) == F
	assert And(A,T).eval(interp_1) == T
	assert And(B,T).eval(interp_1) == F
	assert Or(A,B).eval(interp_1) == T
	assert And(A,B).eval(interp_1) == F

	interp_2 = {A : F, B : F, C : T}
	assert F == Iff(C, And(Not(A),B)).eval(interp_2)
	assert T == Iff(Not(C), And(Not(A),B)).eval(interp_2)
	assert F == Implies(Iff(Not(C), And(Not(A),B)), And(T, Not(C))).eval(interp_2)
	
	D = BoolVar("D")
	E = BoolVar("E")
	interp_3 = {A : F, B : F, C : T, D : T, E : F}
	assert T == Or(And(Not(Implies(Iff(Not(C), And(Not(A),B)), And(T, Not(C)))), D), F).eval(interp_3)



def test_simplify():
	# This is a placeholder test.
	# You should write your own tests
	# to make sure your simplify is working.
	assert T == Or(T,T).simplify()
	assert F == Or(F,F).simplify()
	assert T == Or(T,F).simplify()
	assert T == Or(F,T).simplify()
	assert T == Or(And(T,T), Or(T,F)).simplify()
	assert B == Or(B,B).simplify()

	x = And(Or(A,B), Not(C))
	assert x == Or(F, x).simplify()
	assert A == And(A,A).simplify()
	assert x == And(x,x).simplify()
	assert F == And(F, x).simplify()
	assert F == And(x, F).simplify()
	assert T == And(Or(T,F), Or(T,T)).simplify()

	assert Iff(T, x).simplify() == x
	assert Iff(x, T).simplify() == x 
	assert Iff(F, x).simplify() == Not(x)
	assert Iff(x, F).simplify() == Not(x)
	assert Iff(x, x).simplify() == T
	assert Implies(T, x).simplify() == x
	assert Implies(F, x).simplify() == T
	assert Implies(x, x).simplify() == T
	assert Implies(x, T).simplify() == T
	assert Implies(x, F).simplify() == Not(x)
