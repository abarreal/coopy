class Evaluable:

    @property
    def value(self):
        raise Exception('Not implemented (abstract)')

    @property
    def has_concrete_value(self):
        raise Exception('Not implemented (abstract)')

    @property
    def is_function(self):
        return False # should be overriden by child classes if needed.

def is_evaluable(object):
    return isinstance(object, Evaluable)

def do_evaluate(object):
    return object.value if is_evaluable(object) else object

def is_concrete_like(object):
    return not is_evaluable(object) or object.has_concrete_value