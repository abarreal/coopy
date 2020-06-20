from z3 import *

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class Z3Backend:

    def __init__(self):
        self._default_scope = Z3Scope(self, Solver())
        self._transient_scopes = []

    @property
    def default_scope(self):
        return self._default_scope

    @property
    def _active_scope(self):
        return self._default_scope if not self._transient_scopes else self._transient_scopes[-1]

    def reset(self):
        self._active_scope.reset()

    def minimize(self, expression):
        self._active_scope.minimize(expression)

    def maximize(self, expression):
        self._active_scope.maximize(expression)

    def check_sat(self):
        scope = self._active_scope
        output = scope.check()
        return (output.r == 1), (self._active_scope.model() if output.r == 1 else None)

    def model(self):
        scope = self._active_scope
        scope.check()
        return scope.model()

    def push(self):
        self._active_scope.push()

    def pop(self):
        self._active_scope.pop()

    def add(self, constraint):
        # Simplify non boolean constraints.
        if not type(constraint) == bool:
            constraint = simplify(constraint)
        # Add the constraint.
        self._active_scope.add(constraint)

    def soft(self, constraint, weight=1):
        self._active_scope.soft(constraint, weight)

    def declare_sort(self, name):
        sort = DeclareSort(name)
        self._active_scope.add_sort(sort)
        return sort

    def scope(self):
        scope = Z3Scope(self, Solver())
        self._transient_scopes.append(scope)
        return scope

    def optimizer(self):
        scope = Z3Scope(self, Optimize())
        self._transient_scopes.append(scope)
        return scope

    def exit_scope(self):
        self._transient_scopes.pop()

    def symbolic(self, basename, sort):
        return Const(self._autogenerate_name(basename), sort)

    def symbolic_int(self, basename):
        return Int(self._autogenerate_name(basename))

    def symbolic_bool(self, basename):
        return Bool(self._autogenerate_name(basename))

    def symbolic_real(self, basename):
        return Real(self._autogenerate_name(basename))

    def symbolic_int_array(self, basename):
        return Array(self._autogenerate_name(basename), IntSort(), IntSort())

    def conjunction(self, *args):
        return And(*args)

    def disjunction(self, *args):
        return Or(*args)

    def negation(self, *args):
        return Not(*args)

    def forall(self, *args):
        return ForAll(*args)

    def exists(self, *args):
        return Exists(*args)

    def implies(self, antecedent, consequent):
        return Implies(antecedent, consequent)

    def ite(self, guard, true_case, false_case):
        return If(guard, true_case, false_case)

    def iff(self, a, b):
        return a == b

    def uninterpreted_function(self, basename, *sorts):
        # Not autogenerating name for functions, it does not look that well.
        return Function(basename, *sorts)

    def evaluate_uninterpreted(self, f, *args):
        return f(*args)

    def evaluate_function_call(self, model, f, *args):
        # Unwrap wrapped objects.
        copy = args
        args = list(copy)
        for i,arg in enumerate(copy):
            if isinstance(arg, Z3CustomTypeWrapper):
                args[i] = arg.wrapped
        # Evaluate the function and obtain a result.
        value = model.evaluate(f(*args))
        # If of a custom sort, wrap the resulting value in a wrapper.
        sorts = self._active_scope.sorts
        return Z3CustomTypeWrapper(value) if value.sort() in sorts else value

    def _autogenerate_name(self, basename):
        type(self)._autogenerate_name.counter += 1
        return '{}:{}'.format(basename, type(self)._autogenerate_name.counter)
    
    _autogenerate_name.counter = 0

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class Z3Scope:

    def __init__(self, backend, solver):
        self._backend = backend
        self._solver = solver
        self._sorts = set()

    def reset(self):
        self._solver.reset()

    def check(self):
        return self._solver.check()

    def push(self):
        self._solver.push()

    def pop(self):
        self._solver.pop()

    def model(self):
        return self._solver.model()

    @property
    def assertions(self):
        return self._solver.assertions()

    def add(self, constraint):
        self._solver.add(constraint)

    def soft(self, constraint, weight=1):
        self._solver.add_soft(constraint, weight=1)

    def minimize(self, expression):
        self._solver.minimize(expression)

    def maximize(self, expression):
        self._solver.maximize(expression)

    def add_sort(self, sort):
        self._sorts.add(sort)

    @property
    def sorts(self):
        return self._sorts

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        self._backend.exit_scope()

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class Z3CustomTypeWrapper:

    def __init__(self, obj):
        self._obj = obj

    @property
    def wrapped(self):
        return self._obj

    @property
    def value(self):
        return self.wrapped

    def __eq__(self, other):
        if isinstance(other, Z3CustomTypeWrapper):
            return self._obj.eq(other._obj)
        else:
            return other.__eq__(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.value.__repr__()

def to_int(z3_object):
    return z3_object.as_long()

def to_bool(z3_object):
    return bool(z3_object)

def to_obj(z3_object):
    return Z3CustomTypeWrapper(z3_object)