from z3 import *

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class Z3Backend:

    def __init__(self):
        self._solver = Solver()
        self._children = []
        self._sorts = set()

    def reset(self):
        self._solver.reset()
        self._children.clear()

    def model(self):
        self._solver.check()
        return self._solver.model()

    def add(self, constraint):
        self._solver.add(constraint)

    def declare_sort(self, name):
        sort = DeclareSort(name)
        self._sorts.add(sort)
        return sort

    def symbolic(self, basename, sort):
        return Const(self._autogenerate_name(basename), sort)

    def symbolic_int(self, basename):
        return Int(self._autogenerate_name(basename))

    def symbolic_bool(self, basename):
        return Bool(self._autogenerate_name(basename))

    def symbolic_real(self, basename):
        return Real(self._autogenerate_name(basename))

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

    def iff(self, a, b):
        return self.conjunction(self.implies(a,b), self.implies(b,a))

    def uninterpreted_function(self, basename, *sorts):
        # Not autogenerating name for functions, cause it looks like cr*p.
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
        return Z3CustomTypeWrapper(value) if value.sort() in self._sorts else value

    def _autogenerate_name(self, basename):
        type(self)._autogenerate_name.counter += 1
        return '{}:{}'.format(basename, type(self)._autogenerate_name.counter)
    
    _autogenerate_name.counter = 0

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class Z3CustomTypeWrapper:

    def __init__(self, obj):
        self._obj = obj

    @property
    def wrapped(self):
        return self._obj

    def __eq__(self, other):
        if isinstance(other, Z3CustomTypeWrapper):
            return self._obj.eq(other._obj)
        else:
            return other.__eq__(self)

    def __ne__(self, other):
        return not self.__eq__(other)

def to_int(z3_object):
    return z3_object.as_long()

def to_bool(z3_object):
    return bool(z3_object)

def to_obj(z3_object):
    return Z3CustomTypeWrapper(z3_object)