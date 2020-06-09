from .operator import BinaryOperator
from .logic import ConcretizableEntity, ConcretizableOrdered

from ..symbolic import concretizable

from functools import partial

#==================================================================================================
#
# CONCRETIZABLE TYPES
#
#--------------------------------------------------------------------------------------------------
class ConcretizableArithmeticOperand(ConcretizableOrdered):

    #----------------------------------------------------------------------------------------------
    def __add__concretized(self, other):
        return self.concrete_value + other

    @concretizable(__add__concretized)
    def __add__(self, other):
        return Add(self, other)

    #----------------------------------------------------------------------------------------------
    def __radd__concretized(self, other):
        return other + self.concrete_value

    @concretizable(__radd__concretized)
    def __radd__(self, other):
        return Add(other, self)

    #----------------------------------------------------------------------------------------------
    def __sub__concretized(self, other):
        return self.concrete_value - other

    @concretizable(__sub__concretized)
    def __sub__(self, other):
        return Sub(self, other)

    #----------------------------------------------------------------------------------------------
    def __rsub__concretized(self, other):
        return other - self.concrete_value

    @concretizable(__rsub__concretized)
    def __rsub__(self, other):
        return Sub(other, self)

    #----------------------------------------------------------------------------------------------
    def __rmul__concretized(self, other):
        return other * self.concrete_value

    @concretizable(__rmul__concretized)
    def __rmul__(self, other):
        return Mul(other, self)

    #----------------------------------------------------------------------------------------------
    def __mul__concretized(self, other):
        return self.concrete_value * other

    @concretizable(__mul__concretized)
    def __mul__(self, other):
        return Mul(self, other)

    #----------------------------------------------------------------------------------------------
    def __rdiv__concretized(self, other):
        return other / self.concrete_value

    @concretizable(__rdiv__concretized)
    def __rdiv__(self, other):
        return Div(other, self)

    #----------------------------------------------------------------------------------------------
    def __div__concretized(self, other):
        return self.concrete_value / other

    @concretizable(__div__concretized)
    def __div__(self, other):
        return Div(self, other)

    #----------------------------------------------------------------------------------------------
    def __rmod__concretized(self, other):
        return other % self.concrete_value

    @concretizable(__rmod__concretized)
    def __rmod__(self, other):
        return Mod(other, self)

    #----------------------------------------------------------------------------------------------
    def __mod__concretized(self, other):
        return self.concrete_value % other

    @concretizable(__mod__concretized)
    def __mod__(self, other):
        return Mod(self, other)

#==================================================================================================
#
# ARITHMETIC AST NODES
#
#--------------------------------------------------------------------------------------------------
class BinaryArithmeticOperator(ConcretizableArithmeticOperand, BinaryOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Add(BinaryArithmeticOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a, b: a + b)

class Sub(BinaryArithmeticOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a, b: a - b)

class Mul(BinaryArithmeticOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a, b: a * b)

class Div(BinaryArithmeticOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a, b: a / b)

class Div(BinaryArithmeticOperator):
    def __init__(self, a, b):
        super().__init__(a, b, lambda a, b: a % b)