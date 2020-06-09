import coopy

from coopy.symbolic.evaluable import Evaluable
from coopy import forall
from functools import reduce

# Define a new sort for a custom domain.
B = coopy.sort('B')

class Boolean(Evaluable):

    # Define the boolean negation unary function ~ : B -> B.
    NOT = coopy.function('~', B, B)

    # Define the boolean binary function 'and', * : (B,B) -> B.
    AND = coopy.function('*', B, B, B)

    # Define the boolean binary function 'or', + : (B,B) -> B.
    OR = coopy.function('+', B, B, B)

    def __init__(self, name=None, value=None):
        # Instantiate a symbolic value of the sort B if no value was given.
        self._sym = value if value else coopy.symbolic(name if name else 'b', B)

    @property
    def value(self):
        # Defining this method allows to pass Boolean objects to coopy functions
        # directly, rather than passing the symbol object, as well as using them 
        # as bound variables for quantifiers.
        return self._sym.value

    @property
    def neg(self):
        return Boolean.NOT(self, wrapper=Boolean)

    def __mul__(self, other):
        return Boolean.AND(self, other, wrapper=Boolean)

    def __add__(self, other):
        return Boolean.OR(self, other, wrapper=Boolean)

    def __eq__(self, other):
        return self._sym == other._sym

    def __ne__(self, other):
        # Important: do NOT use "not self.__eq__(other)"
        return self._sym != other._sym

class BooleanAlgebra:

    def __init__(self):
        # Instantiate the neutral elements of this boolean algebra.
        self.T = Boolean('T')
        self.F = Boolean('F')

    @property
    def axioms(self):

        axioms = True

        T = self.T
        F = self.F

        # Instantiate some constants to use as bound variables:
        p = Boolean('p')
        q = Boolean('q')
        r = Boolean('r')

        # Plain binary boolean algebra:
        axioms &= (T != F)
        axioms &= forall([p], (p == T) | (p == F))

        # Commutative property:
        axioms &= forall([p,q], p + q == q + p)
        axioms &= forall([p,q], p * q == q * p)

        # Distributive property:
        axioms &= forall([p,q,r], r + (p*q) == (r+p) * (r+q))
        axioms &= forall([p,q,r], r * (p+q) == (r*p) + (r*q))

        # Neutral elements:
        axioms &= forall([p], p + F == p)
        axioms &= forall([p], p * T == p)

        # Complements:
        axioms &= forall([p], p + p.neg == T)
        axioms &= forall([p], p * p.neg == F)

        return axioms

# Instantiate a boolean algebra.
algebra = BooleanAlgebra()

# Impose axioms.
algebra.axioms.require()

# Concretize. This resolves all boolean functions
# and gives identity to constants T and F.
coopy.concretize()

# Now the algebra can just be used concretely.
T = algebra.T
F = algebra.F

assert(T != F and T.neg == F and T * F == F and T + F == T)