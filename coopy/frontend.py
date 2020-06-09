from .smt import backend
from .symbolic.types import *

class Front:

    def __init__(self):
        self._children = []

    def reset(self):
        backend.reset()
        self._children.clear()

    def model(self):
        return backend.model()

    def concretize(self):
        # We first obtain a model given the current constraints.
        model = self.model()
        # We then concretize all non concretized children for which there
        # is a solution in the model.
        for child in [c for c in self._children if not c.concretized]:
            # We only concretize with the given model if there is an actual solution
            # for this child's symbolic variable in the model.
            if model[child.symbol] != None:
                child.concretize(model)
        # Just return the model.
        return model
    
    def symbolic_int(self, basename='int'):
        symbol = backend.symbolic_int(basename)
        object = SymbolicInteger(basename, symbol)
        self._children.append(object)
        return object

    def symbolic_bool(self, basename='bool'):
        symbol = backend.symbolic_bool(basename)
        object = SymbolicBool(basename, symbol)
        self._children.append(object)
        return object

    def symbolic_real(self, basename='real', precision=6):
        symbol = backend.symbolic_real(basename)
        object = SymbolicReal(basename, symbol, precision=precision)
        self._children.append(object)
        return object

    def sort(self, name):
        symbol = backend.declare_sort(name)
        return Sort(name, symbol)

    def symbolic(self, name, sort):
        symbol = backend.symbolic(name, sort.symbol)
        object = SymbolicObject(name, symbol, sort)
        self._children.append(object)
        return object

    def uninterpreted_function(self, name, *sorts):
        # We first obtain the symbols for each of the sorts given as arguments.
        sorts = [sort.symbol for sort in sorts]
        # We then request an uninterpreted function symbol to the backend.
        f = backend.uninterpreted_function(name, *sorts)
        # We instantiate then a concretizable function object.
        object = ConcretizableFunction(name, f)
        # We then register the function object for eventual concretization.
        self._children.append(object)
        # Then we just return the object.
        return object