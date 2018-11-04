import unittest

import numpy as np

from chess_table import Field


class TestField(unittest.TestCase):
    def setUp(self):
        self.test_field = Field()
        return

    def tearDown(self):
        self.test_field = None
        return

    def test_empty_field_without_center(self):
        with self.assertRaises(AssertionError):
            _ = self.test_field.center
        self.assertEqual(self.test_field.figure, "empty")
        self.assertEqual(str(self.test_field), "Field(empty)")
        self.assertEqual(self.test_field.fen_char, 1)
        return

    def test_field_with_center_black_figure(self):
        center = np.array([100, 100], dtype=np.float32)
        self.test_field.center = center
        self.test_field.figure = "b_bishop"
        self.assertEqual(self.test_field.figure, "b_bishop")
        self.assertTupleEqual(tuple(self.test_field.center), tuple(center.astype(np.int16)))
        self.assertEqual(self.test_field.center.dtype, np.int16)
        self.assertEqual(self.test_field.fen_char, "b")
        return

    def test_field_with_white_figure(self):
        self.test_field.figure = "w_knight"
        self.assertEqual(self.test_field.fen_char, "N")
        self.assertEqual(str(self.test_field), "Field(w_knight)")
        return


if __name__ == '__main__':
    unittest.main()
