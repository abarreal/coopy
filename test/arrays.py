import unittest
import coopy

from coopy import *

class TestArrays(unittest.TestCase):

    def setUp(self):
        coopy.reset()

    def test_basic(self):
        x = symbolic_int_array('arr')
        require(x[0] == 5)
        require(x[1] == 4)
        concretize()
        self.assertEqual(x[0], 5)
        self.assertEqual(x[1], 4)

if __name__ == '__main__':
    unittest.main()