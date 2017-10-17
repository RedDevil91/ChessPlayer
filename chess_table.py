SQUARE_SIZE = 80
TABLE_FIELD_NUM = 8


class Field(object):
    def __init__(self, number):
        self.number = number
        self.figure = 'empty'
        return

    def getPosition(self):
        row = self.number / TABLE_FIELD_NUM
        col = self.number % TABLE_FIELD_NUM
        return row, col


class ChessTable(object):
    base_line = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    color_sep = '_'

    def __init__(self):
        self.fields = [Field(field_id) for field_id in range(TABLE_FIELD_NUM**2)]
        return

    def initTable(self):
        # black init section
        color = 'b'
        for i, figure in enumerate(self.base_line):
            self.fields[i].figure = color + self.color_sep + figure

        pawn = color + self.color_sep + 'pawn'
        start_idx = TABLE_FIELD_NUM
        for i in range(TABLE_FIELD_NUM):
            self.fields[start_idx + i].figure = pawn

        # white init section
        start_idx = 6 * TABLE_FIELD_NUM
        color = 'w'
        pawn = color + self.color_sep + 'pawn'
        for i in range(TABLE_FIELD_NUM):
            self.fields[start_idx + i].figure = pawn

        start_idx = 7 * TABLE_FIELD_NUM
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
        row_sep_str = "-" * 11 * TABLE_FIELD_NUM + "\n"
        table_str = row_sep_str
        for row in range(TABLE_FIELD_NUM):
            for col in range(TABLE_FIELD_NUM):
                field_id = row * TABLE_FIELD_NUM + col
                field = self.getField(field_id)
                table_str += "|%10s" % field.figure
            table_str += "|\n" + row_sep_str
        return table_str


if __name__ == '__main__':
    table = ChessTable()
    table.initTable()
    print(table)
