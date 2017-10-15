class Field(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.figure = None
        return

    def setFigure(self, figure):
        self.figure = figure
        return


class ChessTable(object):
    column_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    def __init__(self):
        self.fields = {(col + str(row + 1)): Field(row + 1, col) for row, col in enumerate(self.column_labels)}
        return

    def initTable(self):
        return

    def setField(self, row, col, figure):
        field = self.getField(row, col)
        field.setFigure(figure)
        return

    def getField(self, row, col):
        field_key = (col + str(row))
        return self.fields[field_key]

    def moveFigure(self, from_row, from_col, to_row, to_col):
        return


if __name__ == '__main__':
    pass
