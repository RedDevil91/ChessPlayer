import unittest

import numpy as np

from chess_table import ChessTable, TABLE_FIELD_NUM


class TestTableBase(unittest.TestCase):
    player = "white"

    def check_field(self, field_id, figure, vector=None):
        field = self.table.getField(field_id)
        self.assertEqual(field.figure, figure)
        if vector is not None:
            self.assertTupleEqual(tuple(field.center), tuple(vector))
        else:
            with self.assertRaises(AssertionError):
                _ = field.center
        return

    def create_fields(self):
        self.check_field(0, "empty")
        self.check_field(63, "empty")

        field_props = [("empty", np.array([row, col])) for row in range(TABLE_FIELD_NUM) for col in range(TABLE_FIELD_NUM)]
        field_props[0] = ("w_pawn", np.array([0, 0]))
        field_props[63] = ("b_pawn", np.array([7, 7]))
        self.table.setFields(field_props)

        self.check_field(0, "w_pawn", vector=np.array([0, 0]))
        self.check_field(1, "empty", vector=np.array([0, 1]))
        self.check_field(62, "empty", vector=np.array([7, 6]))
        self.check_field(63, "b_pawn", vector=np.array([7, 7]))
        return

    def check_field_pairs(self, field_pairs):
        for int_id, str_annotation in field_pairs:
            self.assertTrue(self.table.getField(int_id) is self.table.getField(str_annotation))

    def setUp(self):
        self.table = ChessTable(self.player)
        return

    def tearDown(self):
        self.table = None
        return

    def test_empty_table(self):
        self.assertEqual(str(self.table), "8/8/8/8/8/8/8/8 {color}".format(color=self.player[0]))
        self.assertEqual(self.table.fields[0][0].figure, "empty")
        return

    def test_init_table(self):
        self.table.initTable()
        self.assertEqual(str(self.table), "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR {color}".format(color=self.player[0]))
        self.assertEqual(self.table.fields[0][0].figure, "w_rook")
        self.assertEqual(self.table.fields[7][0].figure, "b_rook")
        return


class TestChessTablePlayerIsWhite(TestTableBase):
    def test_get_field(self):
        self.check_field_pairs([(0, "a8"), (23, "h6"), (63, "h1")])
        return

    def test_set_fields(self):
        self.create_fields()
        self.assertEqual(str(self.table), "P7/8/8/8/8/8/8/7p {color}".format(color=self.player[0]))
        return

    def test_set_field(self):
        self.check_field("e7", "empty")
        self.table.setField(12, "w_queen")
        self.check_field("e7", "w_queen", vector=np.array([0, 0]))
        return


class TestChessTablePlayerIsBlack(TestTableBase):
    player = "black"

    def test_get_field(self):
        self.check_field_pairs([(0, "h1"), (40, "h6"), (63, "a8")])
        return

    def test_set_fields(self):
        self.create_fields()
        self.assertEqual(str(self.table), "7p/8/8/8/8/8/8/P7 {color}".format(color=self.player[0]))
        return

    def test_set_field(self):
        self.check_field("e7", "empty")
        self.table.setField(51, "w_queen")
        self.check_field("e7", "w_queen", vector=np.array([0, 0]))
        return


if __name__ == '__main__':
    unittest.main()
