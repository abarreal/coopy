import unittest
import coopy

from coopy.symbolic.types.primitives import SymbolicBool

class TestBooleans(unittest.TestCase):

    def setUp(self):
        coopy.reset()

    def test_instantiation(self):
        b = coopy.symbolic_bool('b')
        self.assertTrue(not b is None)
        self.assertTrue(isinstance(b, SymbolicBool))

    def test_equality(self):
        p = coopy.symbolic_bool()
        q = coopy.symbolic_bool()
        self.assertTrue(isinstance(p == q, coopy.op.logic.Equal))

    def test_equality_with_concrete_values(self):
        p = coopy.symbolic_bool()
        # Test equality both left and right (there should be no difference for this case).
        self.assertTrue(isinstance(p == True, coopy.op.logic.Equal))
        self.assertTrue(isinstance(True == p, coopy.op.logic.Equal))
        # Test also with false. There should be no difference, but we never know.
        self.assertTrue(isinstance(p == False, coopy.op.logic.Equal))
        self.assertTrue(isinstance(False == p, coopy.op.logic.Equal))
        # Impose constraint.
        (p == False).require()
        # Concretize; we expect p to behave like a plain false boolean from now on.
        coopy.concretize()
        # Assert that p is indeed false.
        self.assertFalse(p)

    def test_conjunction(self):
        p = coopy.symbolic_bool()
        q = coopy.symbolic_bool()
        self.assertTrue(isinstance(p & True, coopy.op.logic.And))
        self.assertTrue(isinstance(p & q, coopy.op.logic.And))
        # Impose constraint and concretize.
        (p & q).require()
        coopy.concretize()
        # Assert that p and q can be used as booleans.
        self.assertTrue(p and q)
        # Assert that expressions that previously used & now evaluate to
        # boolean values.
        self.assertFalse(not (p & q))
        self.assertTrue((p & q) == True)
        self.assertFalse(p & coopy.neg(q))

    def test_disjunction(self):
        p = coopy.symbolic_bool()
        q = coopy.symbolic_bool()
        self.assertTrue(isinstance(p | True, coopy.op.logic.Or))
        self.assertTrue(isinstance(p | q, coopy.op.logic.Or))
        # Impose constraint and concretize.
        (p | q).require()
        coopy.concretize()
        # Assert that p and q can be used as booleans.
        self.assertTrue(p or q)
        # Assert that expressions that previously used | now evaluate to
        # boolean values.
        self.assertFalse(not (p | q))
        self.assertTrue((p | q) == True)

    def test_negation(self):
        neg = coopy.neg
        p = coopy.symbolic_bool()
        q = coopy.symbolic_bool()
        self.assertTrue(isinstance(neg(p), coopy.op.logic.Not))
        # Impose constraint and concretize.
        neg(p).require()
        neg(neg(q)).require()
        coopy.concretize()
        # Ensure that p is now false and q is now true.
        self.assertFalse(p)
        self.assertFalse(p and q)
        self.assertTrue(not p)
        self.assertTrue(neg(p))
        self.assertTrue(q)
        self.assertTrue(p or q)

if __name__ == '__main__':
    unittest.main()