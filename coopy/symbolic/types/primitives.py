from .. import Symbol
from ...op.arithmetic import ConcretizableArithmeticOperand
from ...op.logic import Predicate, ConcretizableEntity

# TODO: make this less coupled to Z3 model outputs.

class SymbolicPrimitive:

    def __int__(self):
        return int(self.concrete_value)

    def __float__(self):
        return float(self.concrete_value)

    def __bool__(self):
        return bool(self.concrete_value)

class SymbolicInteger(Symbol, SymbolicPrimitive, ConcretizableArithmeticOperand):

    @property
    def concrete_value(self):
        return super().concrete_value.as_long()

class SymbolicBool(Symbol, Predicate, SymbolicPrimitive, ConcretizableEntity):

    @property
    def concrete_value(self):
        return bool(super().concrete_value)

class SymbolicReal(Symbol, SymbolicPrimitive, ConcretizableArithmeticOperand):

    def __init__(self, *args, precision=6, **kwargs):
        super().__init__(*args, **kwargs)
        self._concretization_precision = precision
        self._concretized_value = None

    @property
    def concrete_value(self):
        # Get the value as a string, and then parse it into a float. Cache the result
        # for eventual reuse.
        if not self._concretized_value:
            model_str = super().concrete_value.as_float(self._concretization_precision)
            self._concretized_value = float(model_str)

        return self._concretized_value