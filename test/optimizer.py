import unittest
import coopy

from coopy import symbolic_int, require

class TestOptimizezr(unittest.TestCase):

    def setUp(self):
        coopy.reset()

    def test_minimization(self):
        with coopy.optimizer():
            x = symbolic_int('x')
            y = symbolic_int('y')

            require(y > 1)
            require(x > y)
            
            coopy.minimize(x + y)
            coopy.concretize()

            self.assertEqual(y, 2)
            self.assertEqual(x, 3)

    def test_minimization_shortcut_syntax(self):
        with coopy.optimizer():
            x = symbolic_int('x')
            y = symbolic_int('y')

            require(y > 1)
            require(x > y)
            
            coopy.concretize(minimize=x+y)

            self.assertEqual(y, 2)
            self.assertEqual(x, 3)

if __name__ == '__main__':
    unittest.main()