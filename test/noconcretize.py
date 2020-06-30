import unittest
import coopy

from coopy.symbolic.types.primitives import SymbolicReal

class TestNoConcretization(unittest.TestCase):

    def setUp(self):
        coopy.reset()
        coopy.solver.disable_concretization()

    def tearDown(self):
        coopy.solver.enable_concretization()

    def test_reals(self):
        x = coopy.symbolic_real('x')
        y = coopy.symbolic_real('y')
        # Impose some constraints.
        coopy.require((x == 3) & (x > y))
        # Check satisfiability and get model.
        sat, model = coopy.check_sat()
        # Evaluate both x and y in the model.
        x_val = model.evaluate(x)
        y_val = model.evaluate(y)
        # Assert.
        self.assertTrue(x_val == 3)
        self.assertTrue(x_val > y_val)
        self.assertEqual(len(coopy.solver._children), 0)

    def test_bools(self):
        x = coopy.symbolic_bool('x')
        y = coopy.symbolic_bool('y')
        # Impose some constraints.
        coopy.require((x == y) & x)
        # Check satisfiability and get model.
        sat, model = coopy.check_sat()
        # Evaluate both x and y in the model.
        x_val = model.evaluate(x)
        y_val = model.evaluate(y)
        # Assert.
        self.assertTrue(x_val)
        self.assertTrue(y_val)
        self.assertEqual(len(coopy.solver._children), 0)

if __name__ == '__main__':
    unittest.main()