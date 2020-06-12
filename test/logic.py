import unittest
import coopy

from coopy import *

class TestLogic(unittest.TestCase):

    def setUp(self):
        coopy.reset()

    def test_implication_1(self):
        p = symbolic_bool('p')
        q = symbolic_bool('q')

        require(implies(True, p))
        require(implies(p, q))

        concretize()
        self.assertTrue(p)
        self.assertTrue(q)

    def test_implication_2(self):
        p = symbolic_bool('p')
        q = symbolic_bool('q')

        require(p == True)
        require(implies(p, True))
        require(implies(p, q))

        concretize()
        self.assertTrue(p)
        self.assertTrue(q)
        
if __name__ == '__main__':
    unittest.main()