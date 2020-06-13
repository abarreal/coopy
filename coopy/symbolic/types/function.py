from ..evaluable import Evaluable
from ...op.logic import Entity
from ...smt import backend

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class RValue(Evaluable, Entity):

    def __init__(self, symbol):
        self._symbol = symbol

    @property
    def value(self):
        return self._symbol

    @property
    def symbol(self):
        return self._symbol

    @property
    def has_concrete_value(self):
        return False

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class ConcretizableFunction(Evaluable):

    def __init__(self, name, backend_uninterpreted):
        self._name = name
        self._symbol = backend_uninterpreted
        self._model = None

    def concretize(self, model):
        self._model = model

    @property
    def concretized(self):
        return self._model != None

    @property
    def symbol(self):
        return self._symbol

    @property
    def is_function(self):
        return True

    def __call__(self, *args, wrapper=None):

        # Unwrap arguments.
        args = [arg.value for arg in args]

        if self.concretized:
            output = backend.evaluate_function_call(self._model, self.symbol, *args)
        else:
            output = RValue(backend.evaluate_uninterpreted(self.symbol, *args))

        return output if wrapper is None else wrapper(value=output) 