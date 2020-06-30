from .smt import backend
from .symbolic import Evaluable
from .symbolic.types import *

class Front:

    def __init__(self):
        self._default_scope = FrontScope(self, backend, backend.default_scope)
        self._transient_scopes = []
        self._enable_concretization = True

    @property
    def concretization_enabled(self):
        return self._enable_concretization

    def disable_concretization(self):
        self._enable_concretization = False

    def enable_concretization(self):
        self._enable_concretization = True

    def scope(self):
        return self._scope(backend.scope())

    def optimizer(self):
        return self._scope(backend.optimizer())

    def exit_scope(self):
        self._transient_scopes.pop()

    @property
    def assertions(self):
        return self._active_scope.assertions

    def reset(self):
        self._active_scope.reset()

    def push(self):
        self._active_scope.push()

    def pop(self):
        self._active_scope.pop()

    def check_sat(self):
        return self._active_scope.check_sat()

    def model(self):
        return self._active_scope.model()

    def minimize(self, expression):
        self._active_scope.minimize(expression)

    def maximize(self, expression):
        self._active_scope.maximize(expression)

    def concretize(self, minimize=None, maximize=None):

        if not self.concretization_enabled:
            raise Exception('Cannot concretize: concretization was disabled.')

        if not minimize is None:
            self.minimize(minimize)

        if not maximize is None:
            self.maximize(maximize)

        # We first obtain a model given the current constraints.
        model = self.model().backend_model
        # We then concretize all non concretized children for which there
        # is a solution in the model.
        for child in [c for c in self._children if not c.concretized]:
            # We only concretize with the given model if there is an actual solution
            # for this child's symbolic variable in the model.
            if model[child.symbol] != None:
                child.concretize(model)
                # Additionally impose the equality restriction.
                # NOTE: Z3 does not seem to allow concretizing functions,
                # thus concrete value constraints are only imposed for non functions.
                if not child.is_function:
                    self._active_scope.concretize(child, model)

        # Just return the model.
        return model

    def wrap_concrete(self, value):
        return ConcreteWrapper(value)

    def symbolic_int_array(self, basename='arr'):
        symbol = backend.symbolic_int_array(basename)
        object = SymbolicArray(str(symbol), symbol, datatype=SymbolicInteger)
        # Keep track of the child only if concretization is enabled.
        if self.concretization_enabled: self._children.append(object)
        return object

    def symbolic_int(self, basename='int'):
        symbol = backend.symbolic_int(basename)
        object = SymbolicInteger(str(symbol), symbol)
        # Keep track of the child only if concretization is enabled.
        if self.concretization_enabled: self._children.append(object)
        return object

    def symbolic_bool(self, basename='bool'):
        symbol = backend.symbolic_bool(basename)
        object = SymbolicBool(str(symbol), symbol)
        # Keep track of the child only if concretization is enabled.
        if self.concretization_enabled: self._children.append(object)
        return object

    def symbolic_real(self, basename='real', precision=6):
        symbol = backend.symbolic_real(basename)
        object = SymbolicReal(str(symbol), symbol, precision=precision)
        # Keep track of the child only if concretization is enabled.
        if self.concretization_enabled: self._children.append(object)
        return object

    def sort(self, name):
        symbol = backend.declare_sort(name)
        return Sort(name, symbol)

    def symbolic(self, name, sort):
        symbol = backend.symbolic(name, sort.symbol)
        object = SymbolicObject(str(symbol), symbol, sort)
        # Keep track of the child only if concretization is enabled.
        if self.concretization_enabled: self._children.append(object)
        return object

    def uninterpreted_function(self, name, *sorts):
        # We first obtain the symbols for each of the sorts given as arguments.
        sorts = [sort.symbol for sort in sorts]
        # We then request an uninterpreted function symbol to the backend.
        f = backend.uninterpreted_function(name, *sorts)
        # We instantiate then a concretizable function object.
        object = ConcretizableFunction(name, f)
        # We then register the function object for eventual concretization,
        # but only if concretization is enabled.
        if self.concretization_enabled:  self._children.append(object)
        # Then we just return the object.
        return object

    @property
    def _active_scope(self):
        return self._default_scope if not self._transient_scopes else self._transient_scopes[-1]

    @property
    def _children(self):
        return self._active_scope.children

    def _scope(self, backend_scope):
        scope = FrontScope(self, backend, backend_scope)
        self._transient_scopes.append(scope)
        return scope

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class Model:

    def __init__(self, backend_model, backend):
        self._backend_model = backend_model
        self._backend = backend

    @property
    def backend_model(self):
        return self._backend_model

    def __getitem__(self, item):
        return self.evaluate(item)

    def evaluate(self, expression, precision=6):
        if not isinstance(expression, Evaluable):
            return expression
        elif expression.has_concrete_value:
            return expression.value
        else:
            return self._backend.evaluate_in_model(
                expression.value, self._backend_model, self, precision=precision)

    def _handle_integer(self, value):
        return ConcreteWrapper(value)

    def _handle_bool(self, value):
        return ConcreteWrapper(value)

    def _handle_real(self, value):
        return ConcreteWrapper(value)

    def __repr__(self):
        return self.backend_model.__repr__()

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class FrontScope:

    def __init__(self, frontend, backend, backend_scope):
        self._frontend = frontend
        self._backend = backend
        self._backend_scope = backend_scope
        self._symbols = []

    @property
    def children(self):
        return self._symbols

    @property
    def assertions(self):
        return self._backend_scope.assertions

    def reset(self):
        self._backend.reset()
        self._symbols.clear()

    def push(self):
        self._backend.push()

    def pop(self):
        self._backend.pop()

    def concretize(self, variable, model):
        self._backend_scope.add(variable.symbol == model[variable.symbol])
        # Remove variable from children to allow for eventual garbage collection.
        # TODO: Should this be made configurable?
        self.children.remove(variable)

    def minimize(self, expression):
        self._backend.minimize(expression.value)

    def maximize(self, expression):
        self._backend.maximize(expression.value)

    def check_sat(self):
        sat, model = self._backend.check_sat()
        return sat, (Model(model, self._backend) if sat else None)

    def model(self):
        return Model(self._backend.model(), self._backend)

    def __enter__(self):
        self._backend_scope.__enter__()

    def __exit__(self, type, value, traceback):
        self._backend_scope.__exit__(type, value, traceback)
        self._frontend.exit_scope()