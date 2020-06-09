from .z3 import Z3Backend

backend = Z3Backend()

from .z3 import to_int as backend_int_to_int
from .z3 import to_bool as backend_bool_to_bool
from .z3 import to_obj as backend_obj_to_obj