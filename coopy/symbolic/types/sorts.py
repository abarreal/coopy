from ...smt import backend_obj_to_obj
from ..symbol import Symbol
from ...op.logic import ConcretizableEntity

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class Sort:

    def __init__(self, name, backend_sort):
        self._name = name
        self._backend_sort = backend_sort

    @property
    def symbol(self):
        return self._backend_sort

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class SymbolicObject(Symbol, ConcretizableEntity):
    
    def __init__(self, name, backend_symbol, sort):
        super().__init__(name, backend_symbol)
        self._sort = sort

    @property
    def sort(self):
        return self._sort

    @property
    def concrete_value(self):
        value = super().concrete_value
        return backend_obj_to_obj(value)