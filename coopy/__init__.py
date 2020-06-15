from .op.logic import Predicate, EmptyPredicate
from .op.logic import ForAll as forall
from .op.logic import Implies as implies
from .op.logic import Exists as exists
from .op.logic import Iff as iff
from .op.other import ITE as ite
from .frontend import Front

import functools

solver = Front()

# Allow access to front-end methods more easily.
symbolic_int = solver.symbolic_int
symbolic_real = solver.symbolic_real
symbolic_bool = solver.symbolic_bool
symbolic_int_array = solver.symbolic_int_array
concretize = solver.concretize
model = solver.model
check_sat = solver.check_sat
reset = solver.reset
maximize = solver.maximize
minimize = solver.minimize
push = solver.push
pop = solver.pop
wrap_concrete = solver.wrap_concrete

scope = solver.scope
optimizer = solver.optimizer

sort = solver.sort
symbolic = solver.symbolic
function = solver.uninterpreted_function

neg = Predicate.negate

# The following function is meant to make
# expressions like (x > y).require() more natural
# by writing them like require(x > y).
def require(constraint):
    if isinstance(constraint, Predicate):
        constraint.require()
    elif not (type(constraint) == bool and constraint == True):
        raise Exception('Cannot require {} as a constraint'.format(constraint))

def all(constraints):
    if not constraints: 
        return EmptyPredicate()
    return functools.reduce(lambda x,y: x & y, constraints)

def any(constraints):
    if not constraints: 
        return EmptyPredicate()
    return functools.reduce(lambda x,y: x | y, constraints)

from .symbolic import Evaluable

class CustomSort(Evaluable):

    def __init__(self, name=None, value=None, sort=None):
        self._sym = value if value else symbolic(name if name else '{}i'.format(sort.name), sort)

    @property
    def value(self):
        return self._sym.value

    def __eq__(self, other):
        return self._sym == other._sym

    def __ne__(self, other):
        return self._sym != other._sym

    def __repr__(self):
        return self._sym.value.__repr__()