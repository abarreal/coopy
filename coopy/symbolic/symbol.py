from .evaluable import Evaluable

import functools

class Symbol(Evaluable):

    def __init__(self, name, backend_symbol):
        self._name = name
        self._symbol = backend_symbol
        # Symbolic integers keep a reference to a modle object
        # which allows to evaluate the symbolic value once it is set.
        self._model = None

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol
        
    @property
    def concretized(self):
        return self._model != None

    @property
    def concrete_value(self):
        if self.concretized:
            return self._model.evaluate(self._symbol)
        else:
            raise Exception('concrete_value called without previous concretization')

    @property
    def value(self):
        return self.concrete_value if self.concretized else self.symbol

    @property
    def has_concrete_value(self):
        return self.concretized

    def concretize(self, model):
        self._model = model

    def __repr__(self):
        if self.concretized:
            return self.concrete_value.__repr__()
        else:
            return self.value.__repr__()

# Concretizable decorator for functions that change behavior once the symbols
# have been concretized.
def concretizable(concrete_alternative):

    # Actual decorator method.
    def inner(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if self.has_concrete_value:
                return concrete_alternative(self, *args, **kwargs)
            else:
                return method(self, *args, **kwargs)
        return wrapper

    return inner