import unittest

from coopy import *

class TestSorts(unittest.TestCase):

    def vars(self):
        return self.x, self.y, self.z

    def setUp(self):
        reset()

        # Declare a custom sort.
        self.S = sort('S')
        # Create some objects of sort S.
        self.x = symbolic('x', self.S)
        self.y = symbolic('y', self.S)
        self.z = symbolic('z', self.S)

        # Create a function.
        self.f = function('f', self.S, self.S)

    def test_disjunction_of_equality(self):
        x, y, z = self.vars()
        # Require x being equal either to y, or to z.
        forall([x], (x == y) | (x == z)).require()
        # Concretize.
        concretize()

    def test_functions(self):
        x, y, z = self.vars()
        # Require x being equal either to y, or to z.
        forall([x], (x == y) | (x == z)).require()

        # Give some meaning to the function f.
        f = self.f

        forall([x], f(x) != x).require()

        # Concretize.
        concretize()

        # Assert that the function was concretized.
        self.assertTrue(f(y) == z)
        self.assertTrue(f(z) == y)
        self.assertFalse(f(y) == y)
        self.assertFalse(f(z) == z)

    def test_disjunction_of_function_calls(self):
        x, y, z = self.vars()
        # Require x being equal either to y, or to z.
        forall([x], (x == y) | (x == z)).require()

        # Give some meaning to the function f.
        f = self.f

        forall([x], (f(x) == x) | (f(x) == z)).require()

        # Concretize.
        concretize()

if __name__ == '__main__':
    unittest.main()