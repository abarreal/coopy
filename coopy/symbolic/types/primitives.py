from .. import Symbol, Evaluable, do_evaluate
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

class SymbolicBool(Symbol, Predicate, SymbolicPrimitive):

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

class SymbolicArray(Symbol):

    def __init__(self, *args, datatype=SymbolicInteger, **kwargs):
        super().__init__(*args, **kwargs)
        self._DataType = datatype
        self._created = []

    def concretize(self, model):
        super().concretize(model)
        # Also concretize elements created by array accesses.
        for c in self._created:
            c.concretize(model)

    def __getitem__(self, idx):
        idx = do_evaluate(idx)
        element = self.symbol[idx]
        element_name = '{}[{}]'.format(self.name, idx)
        element_object = self._DataType(name=element_name, backend_symbol=element)
        if self.has_concrete_value:
            element_object.concretize(self._model)
            return element_object.concrete_value
        else:
            self._created.append(element_object)
            return element_object

class ConcreteWrapper(Evaluable, SymbolicPrimitive, ConcretizableArithmeticOperand):
    
    def __init__(self, value):
        self._value = value

    @property
    def name(self):
        return self.__repr__()

    @property
    def value(self):
        return self._value

    @property
    def concretized(self):
        return True

    @property
    def concrete_value(self):
        return self.value

    @property
    def has_concrete_value(self):
        return True

    @property
    def symbol(self):
        return self.value

    def __repr__(self):
        return self.value.__repr__()

    def __hash__(self):
        return hash(self.value)