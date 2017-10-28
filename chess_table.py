import numpy as np

SQUARE_SIZE = 80
TABLE_FIELD_NUM = 8


class Field(object):

    def __init__(self):
        self.figure = 'empty'
        self._center = None
        return

    def setCenter(self, top_left, x, y):
        translate = np.array([x, y])
        center = (top_left + translate)
        self._center = center.astype(np.int16)
        return

    def getCenter(self):
        assert self._center is not None, "Center point is None!"
        return self._center

    @staticmethod
    def getTranslation(row, col):
        return np.array([col * SQUARE_SIZE + SQUARE_SIZE / 2, row * SQUARE_SIZE + SQUARE_SIZE / 2])


class ChessTable(object):
    col_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    base_line = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    color_sep = '_'

    def __init__(self, top_left, player):
        self.player = player
        self.labels = list(self.col_labels)
        if self.player == 'black':
            self.labels.reverse()
        self.top_left = top_left
        self._fields = {label: [None] * 8 for label in self.col_labels}
        return

    def initTable(self):
        colors = ['w', 'b']
        start_pos = [1, 7]
        reverse = [False, True]
        for col, st, rev in zip(colors, start_pos, reverse):
            pawn = col + self.color_sep + 'pawn'
            for label, figure in zip(self.col_labels, self.base_line):
                fig = col + self.color_sep + figure
                first_figure = fig if not rev else pawn
                second_figure = pawn if not rev else fig
                self.setField(label + str(st), first_figure)
                self.setField(label + str(st+1), second_figure)
        return

    def setField(self, field_id, figure):
        field = self.getField(field_id)
        field.figure = figure
        return field

    def getField(self, field_id):
        if type(field_id) is int:
            label = self.labels[field_id % 8]
            idx = field_id // 8
        else:
            # string type
            label = field_id[0]
            idx = int(field_id[1]) - 1 # indexing starts from zero
        if self._fields[label][idx] is None:
            self._fields[label][idx] = Field()
        return self._fields[label][idx]

    def __str__(self):
        row_sep_str = "-" * 11 * TABLE_FIELD_NUM + "\n"
        table_str = row_sep_str
        for idx in range(TABLE_FIELD_NUM, 0, -1):
            for label in self.col_labels:
                field = self.getField(label + str(idx))
                table_str += "|%10s" % field.figure
            table_str += "|\n" + row_sep_str
        return table_str


if __name__ == '__main__':
    table = ChessTable([0, 0], 'white')
    table.getField(55)
    table.getField('h6')

    table.setField('h5', 'b_pawn')
    print(table)
    table.initTable()
    print(table)
