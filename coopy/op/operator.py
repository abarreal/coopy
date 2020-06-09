from ..symbolic import Evaluable, is_evaluable, do_evaluate

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class UnaryOperator(Evaluable):

    def __init__(self, arg, op):
        self._arg = arg
        self._op = op

    @property
    def arg(self):
        return self._arg

    @property
    def arg_value(self):
        return do_evaluate(self.arg)

    @property
    def value(self):
        return self._op(self.arg_value)

    @property
    def has_concrete_value(self):
        return self.arg.has_concrete_value if is_evaluable(self.arg) else True

#==================================================================================================
#--------------------------------------------------------------------------------------------------
class BinaryOperator(Evaluable):

    def __init__(self, arg1, arg2, op):
        self._a1 = arg1
        self._a2 = arg2
        self._op = op

    @property
    def left(self):
        return self._a1

    @property
    def right(self):
        return self._a2

    @property
    def left_value(self):
        return do_evaluate(self.left)

    @property
    def right_value(self):
        return do_evaluate(self.right)

    @property
    def value(self):
        return self._op(self.left_value, self.right_value)

    @property
    def has_concrete_value(self):
        concrete_l = self.left.has_concrete_value if is_evaluable(self.left) else True
        concrete_r = self.right.has_concrete_value if is_evaluable(self.right) else True
        return concrete_l and concrete_r