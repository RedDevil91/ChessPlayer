class Field(object):
    def __init__(self, number):
        self.number = number
        self.figure = 'empty'
        return

    def getPosition(self):
        row = self.number / 8
        col = self.number % 8
        return row, col


class ChessTable(object):
    base_line = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    color_sep = '_'

    def __init__(self):
        self.fields = [Field(field_id) for field_id in range(64)]
        return

    def initTable(self):
        # black init section
        color = 'b'
        for i, figure in enumerate(self.base_line):
            self.fields[i].figure = color + self.color_sep + figure

        pawn = color + self.color_sep + 'pawn'
        start_idx = 8
        for i in range(8):
            self.fields[start_idx + i].figure = pawn

        # white init section
        start_idx = 48
        color = 'w'
        pawn = color + self.color_sep + 'pawn'
        for i in range(8):
            self.fields[start_idx + i].figure = pawn

        start_idx = 56
        for i, figure in enumerate(self.base_line):
            self.fields[start_idx + i].figure = color + self.color_sep + figure
        return

    def setField(self, field_id, figure):
        field = self.getField(field_id)
        field.figure = figure
        return

    def getField(self, field_id):
        return self.fields[field_id]

    def moveFigure(self, from_id, to_id):
        figure = self.fields[from_id].figure
        self.fields[to_id].figure = figure
        return

    def __str__(self):
        row_sep_str = "-" * 11 * 8 + "\n"
        table_str = row_sep_str
        for row in range(8):
            for col in range(8):
                field_id = row * 8 + col
                field = self.getField(field_id)
                table_str += "|%10s" % field.figure
            table_str += "|\n" + row_sep_str
        return table_str


if __name__ == '__main__':
    table = ChessTable()
    table.initTable()
    print(table)
