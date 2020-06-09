from ..symbolic import Evaluable
from . import backend

import functools

class Constraint(Evaluable):

    def impose(self):
        backend.add(self.value)

    def require(self):
        self.impose()

    @property
    def has_concrete_value(self):
        return False # this should be overriden by child classes.

def constraint(f):

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        output = f(*args, **kwargs)
        concretizable = isinstance(output, Evaluable) and output.has_concrete_value
        return bool(output) if concretizable else output

    return wrapper