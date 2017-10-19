import numpy as np

SQUARE_SIZE = 80
TABLE_FIELD_NUM = 8


class Field(object):
    def __init__(self, number):
        self.number = number
        self.figure = 'empty'
        self.center = None
        self.translate_vector = self.getTranslation()
        return

    def getPosition(self):
        row = self.number // TABLE_FIELD_NUM
        col = self.number % TABLE_FIELD_NUM
        return row, col

    def setCenter(self, center):
        self.center = center.astype(np.int16)
        return

    def getCenter(self):
        assert self.center is not None, "Center point is None!"
        return self.center

    def getTranslation(self):
        row, col = self.getPosition()
        return np.array([row * SQUARE_SIZE + SQUARE_SIZE / 2, col * SQUARE_SIZE + SQUARE_SIZE / 2])


class ChessTable(object):
    col_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    base_line = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    color_sep = '_'

    def __init__(self, top_left):
        self.top_left = top_left
        self.fields = [Field(field_id) for field_id in range(TABLE_FIELD_NUM**2)]
        self._fields = {label: [] for label in self.col_labels}
        for _id in range(TABLE_FIELD_NUM**2):
            self._fields[self.col_labels[_id % 8]].append(Field(_id))
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
        field.setCenter(self.top_left + field.translate_vector)
        field.figure = figure
        return

    def getField(self, field_id):
        if type(field_id) is int:
            label = self.col_labels[field_id % 8]
            idx = field_id // 8
        else:
            # string type
            label = field_id[0]
            idx = int(field_id[1]) - 1 # indexing starts from zero
        return self._fields[label][idx]

    def moveFigure(self, from_id, to_id):
        # TODO fix this method!
        # set the from field figure to empty...
        # use the set and the getfield methods
        figure = self.fields[from_id].figure
        self.fields[to_id].figure = figure
        return

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
    table = ChessTable([0, 0])
    table.getField(55)
    table.getField('h6')

    table.setField('h5', 'b_pawn')
    table.initTable()
    print(table)
