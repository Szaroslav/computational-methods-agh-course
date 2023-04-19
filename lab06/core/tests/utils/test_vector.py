import unittest as ut
import utils.vector as uv


class TestVector(ut.TestCase):
    def test_norm2(self):
        self.assertAlmostEqual(uv.norm2([3, 4]), 5)