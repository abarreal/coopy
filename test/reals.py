import unittest
import coopy

from coopy.symbolic.types.primitives import SymbolicReal

class TestBooleans(unittest.TestCase):

    def setUp(self):
        coopy.reset()

    def test_instantiation(self):
        x = coopy.symbolic_real('x')
        self.assertTrue(not x is None)
        self.assertTrue(isinstance(x, SymbolicReal))

if __name__ == '__main__':
    unittest.main()