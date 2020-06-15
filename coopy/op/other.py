from ..smt import backend
from .logic import Predicate
from .arithmetic import ConcretizableArithmeticOperand

class ITE(Predicate, ConcretizableArithmeticOperand):

    def __init__(self, guard, true_case, false_case):
        self._guard = guard
        self._t = true_case
        self._f = false_case

    @property
    def value(self):
        g = do_evaluate(self._guard)
        t = do_evaluate(self._t)
        f = do_evaluate(self._f)
        return backend.ite(g,t,f)