import numpy as np

SQUARE_SIZE = 80
TABLE_FIELD_NUM = 8


class Field(object):
    __slots__ = "_figure", "_center"

    def __init__(self):
        self._figure = 'empty'
        self._center = None
        return

    def __repr__(self):
        return "Field({figure})".format(figure=self.figure)

    @property
    def center(self):
        assert self._center is not None, "Center point is None!"
        return self._center

    @center.setter
    def center(self, center):
        self._center = center.astype(np.int16)
        return

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, figure):
        self._figure = figure
        return

    @property
    def fen_char(self):
        return self.getFenChar()

    def getFenChar(self):
        try:
            color, figure = self.figure.split("_")
            if figure == "knight":
                fen_char = "n"
            else:
                fen_char = figure[0]
            if color == "w":
                return fen_char.upper()
            else:
                return fen_char
        except ValueError:  # when there is no figure just return with 1
            return 1

    @staticmethod
    def getTranslation(row, col):
        return np.array([col * SQUARE_SIZE + SQUARE_SIZE / 2, row * SQUARE_SIZE + SQUARE_SIZE / 2])


class ChessTable(object):
    __slots__ = "player", "top_left", "_fields", "_labels"
    col_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    base_line = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
    color_sep = '_'

    def __init__(self, player, top_left=np.array([0, 0])):
        self.player = player
        assert self.player in ("white", "black"), "Wrong color for player!"
        self.top_left = top_left
        self._fields = None
        self._labels = self.col_labels.copy()
        if self.player == "black":
            self._labels.reverse()
        return

    def initTable(self):
        self._fields = None
        colors = ['w', 'b']
        start_pos = [1, 7]
        reverse = [False, True]
        for col, st, rev in zip(colors, start_pos, reverse):
            pawn = col + self.color_sep + 'pawn'
            for label, figure in zip(self._labels, self.base_line):
                fig = col + self.color_sep + figure
                first_figure = fig if not rev else pawn
                second_figure = pawn if not rev else fig
                self.setField(label + str(st), first_figure)
                self.setField(label + str(st+1), second_figure)
        return

    @property
    def fields(self):
        if self._fields is None:
            self._fields = {row_idx: [Field() for _ in range(TABLE_FIELD_NUM)] for row_idx in range(TABLE_FIELD_NUM)}
        return self._fields

    def setFields(self, fields_prop):
        [self.setField(i, figure, translate_vec) for i, (figure, translate_vec) in enumerate(fields_prop)]
        return

    def setField(self, field_id, figure, translation=np.array([0, 0])):
        field = self.getField(field_id)
        field.figure = figure
        field.center = self.top_left + translation
        return field

    def getField(self, field_id):
        if type(field_id) is int:
            col_idx = field_id % 8
            row_idx = field_id // 8
            if self.player == "white":
                row_idx = TABLE_FIELD_NUM - 1 - row_idx
        else:
            # string type
            col_idx = self._labels.index(field_id[0])
            row_idx = int(field_id[1]) - 1  # indexing starts from zero
        return self.fields[row_idx][col_idx]

    def getFenString(self):
        rows = [[field.fen_char for field in fields] for _, fields in self.fields.items()]
        rows.reverse()  # to start with the black rows first
        out_list = []
        for row in rows:
            if row.count(1) > 1:
                prev_char = None
                alt_row = []
                for char in row:
                    if prev_char is None or isinstance(char, str) or isinstance(prev_char, str):
                        alt_row.append(char)
                    else:
                        alt_row[-1] += char
                    prev_char = char
            else:
                alt_row = row.copy()
            out_list.append("".join([str(e) for e in alt_row]))
        return "/".join(out_list) + " " + self.player[0]

    def __repr__(self):
        return self.getFenString()
