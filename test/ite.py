import unittest
import coopy

from coopy import *

class TestITE(unittest.TestCase):

    def setUp(self):
        coopy.reset()

    def test_basic(self):
        x = coopy.symbolic_int('x')
        y = coopy.symbolic_int('y')
        
        require(y == ite(x == 5, 5, 10))
        require(y == 5)
        
        concretize()
        self.assertEqual(x, 5)
        self.assertEqual(y, 5)

    def test_nesting(self):
        x = symbolic_int('x')
        y = symbolic_int('y')
        z = symbolic_int('z')

        require(x == 5)
        require(y == ite(x == 2, 3, 4))
        require(z == ite(
            y == 3, 
                2, 
                ite(
                    y == 4, 
                        1, 
                        0
                    )
                ))
        
        concretize()
        self.assertEqual(y, 4)
        self.assertEqual(z, 1)

if __name__ == '__main__':
    unittest.main()