from .op.logic import Predicate, EmptyPredicate
from .op.logic import ForAll as forall
from .op.logic import Implies as implies
from .op.logic import Exists as exists
from .op.logic import Iff as iff
from .frontend import Front

import functools

solver = Front()

# Allow access to front-end methods more easily.
symbolic_int = solver.symbolic_int
symbolic_real = solver.symbolic_real
symbolic_bool = solver.symbolic_bool
concretize = solver.concretize
model = solver.model
reset = solver.reset

scope = solver.scope

sort = solver.sort
symbolic = solver.symbolic
function = solver.uninterpreted_function

neg = Predicate.negate

# The following function is meant to make
# expressions like (x > y).require() more natural
# by writing them like require(x > y).
def require(constraint):
    constraint.require()

def all(constraints):
    if not constraints: 
        return EmptyPredicate()
    return functools.reduce(lambda x,y: x & y, constraints)

def any(constraints):
    if not constraints: 
        return EmptyPredicate()
    return functools.reduce(lambda x,y: x | y, constraints)