from .operator import UnaryOperator, BinaryOperator

from ..symbolic import concretizable, is_concrete_like, do_evaluate
from ..smt.constraint import Constraint
from ..smt import backend

#==================================================================================================
#
# NON-CONCRETIZABLE TYPES
#
#--------------------------------------------------------------------------------------------------
class Entity:

    def __eq__(self, other):
        return Equal(self, other)

    def __ne__(self, other):
        return NotEqual(self, other)

#==================================================================================================
#
# CONCRETIZABLE TYPES
#
#--------------------------------------------------------------------------------------------------

class ConcretizableEntity:

    #----------------------------------------------------------------------------------------------
    def __eq__concretized(self, other):
        return self.concrete_value == other

    @concretizable(__eq__concretized)
    def __eq__(self, other):
        return Equal(self, other)

    #----------------------------------------------------------------------------------------------
    def __ne__concretized(self, other):
        return self.concrete_value != other

    @concretizable(__ne__concretized)
    def __ne__(self, other):
        return NotEqual(self, other)

class ConcretizableOrdered(ConcretizableEntity):

    #----------------------------------------------------------------------------------------------
    def __gt__concrete(self, other):
        return self.concrete_value > other

    @concretizable(__gt__concrete)
    def __gt__(self, other):
        return GreaterThan(self, other)

    #----------------------------------------------------------------------------------------------
    def __ge__concrete(self, other):
        return self.concrete_value > other

    @concretizable(__ge__concrete)
    def __ge__(self, other):
        return GreaterOrEqual(self, other)

    #----------------------------------------------------------------------------------------------
    def __lt__concrete(self, other):
        return self.concrete_value < other

    @concretizable(__lt__concrete)
    def __lt__(self, other):
        return LessThan(self, other)

    #----------------------------------------------------------------------------------------------
    def __le__concrete(self, other):
        return self.concrete_value <= other

    @concretizable(__le__concrete)
    def __le__(self, other):
        return LessThanOrEqual(self, other)

#==================================================================================================
#
# LOGIC AST NODES
#
#--------------------------------------------------------------------------------------------------
class Predicate(Constraint, ConcretizableEntity):

    @staticmethod
    def negate(predicate):
        return not bool(predicate) if is_concrete_like(predicate) else Not(predicate) 

    #----------------------------------------------------------------------------------------------
    def __and__concretized(self, other):
        return self and other if is_concrete_like(other) else other & self

    @concretizable(__and__concretized)
    def __and__(self, other):
        return And(self, other)
    
    #----------------------------------------------------------------------------------------------
    def __rand__concretized(self, other):
        return other and self if is_concrete_like(other) else other & self
    
    @concretizable(__rand__concretized)
    def __rand__(self, other):
        return And(other, self)

    #----------------------------------------------------------------------------------------------
    def __or__concretized(self, other):
        return self or other if is_concrete_like(other) else other | self

    @concretizable(__or__concretized)
    def __or__(self, other):
        return Or(self, other)

    #----------------------------------------------------------------------------------------------
    def __ror__concretized(self, other):
        return other or self if is_concrete_like(other) else other | self

    @concretizable(__ror__concretized)
    def __ror__(self, other):
        return Or(other, self)

class EmptyPredicate(Predicate):

    @property
    def value(self):
        return True

class ForAll(Predicate):

    def __init__(self, bound_variables, predicate):
        self._bound = [do_evaluate(v) for v in bound_variables]
        self._predicate = predicate

    @property
    def value(self):
        return backend.forall(self._bound, do_evaluate(self._predicate))

class Exists(Predicate):

    def __init__(self, bound_variables, predicate):
        self._bound = [do_evaluate(v) for v in bound_variables]
        self._predicate = predicate

    @property
    def value(self):
        return backend.exists(self._bound, do_evaluate(self._predicate))

class Implies(Predicate):

    def __init__(self, antecedent, consequent):
        self._a = antecedent
        self._c = consequent

    @property
    def value(self):
        antecedent = do_evaluate(self._a)
        consequent = do_evaluate(self._c)
        return backend.implies(antecedent, consequent)

class Iff(Predicate):

    def __init__(self, a, b):
        self._a = a
        self._b = b

    @property
    def value(self):
        a = do_evaluate(self._a)
        b = do_evaluate(self._c)
        return backend.iff(a, b)

class Not(UnaryOperator, Predicate):

    def __init__(self, arg):
        super().__init__(arg, op=lambda x: backend.negation(x))

    def __bool__(self):
        return not self.arg_value

class BinaryLogicalOperator(BinaryOperator, Predicate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class And(BinaryLogicalOperator):

    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: backend.conjunction(a,b))

    def __bool__(self):
        return self.left_value and self.right_value

class Or(BinaryLogicalOperator):

    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: backend.disjunction(a,b))

    def __bool__(self):
        return self.left_value or self.right_value

class Equal(BinaryLogicalOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: a == b)

class NotEqual(BinaryLogicalOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: a != b)

class GreaterThan(BinaryLogicalOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: a > b)

class GreaterOrEqual(BinaryLogicalOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: a >= b)

class LessThan(BinaryLogicalOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: a < b)

class LessThanOrEqual(BinaryLogicalOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a,b: a <= b)