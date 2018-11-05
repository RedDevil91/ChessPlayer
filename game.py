from win_interface import Mouse
from stockfish_interface import StockFishEngine
from lichess_interface import LichessInterface
from chess_table import ChessTable, SQUARE_SIZE, TABLE_FIELD_NUM


class GameEngine:
    def __init__(self):
        self.engine = StockFishEngine()
        self.mouse = Mouse()
        self.lichess = LichessInterface()
        self._table = None
        return

    @property
    def table(self):
        if self._table is None:
            table_roi, table_image = self.lichess.get_table_from_screen()
            player_color = self.get_player_color(table_image)
            self._table = ChessTable(player_color, top_left=table_roi.top_left)
        return self._table

    def setFields(self, table_image):
        fields = [LichessInterface.get_field_properties(table_image, row, col)
                  for row in range(TABLE_FIELD_NUM) for col in range(TABLE_FIELD_NUM)]
        self.table.setFields(fields)
        return

    def move(self, from_pos, to_pos):
        from_field = self.table.getField(from_pos)
        from_point = from_field.center
        to_field = self.table.getField(to_pos)
        to_point = to_field.center
        self.mouse.click(from_point[0], from_point[1])
        self.mouse.click(to_point[0], to_point[1])
        return

    @classmethod
    def get_player_color(cls, image):
        topleft_square = image[0:SQUARE_SIZE, 0:SQUARE_SIZE]
        topleft_figure = LichessInterface.evaluate_square(topleft_square)
        if topleft_figure.startswith("b_"):
            return 'white'
        return 'black'


if __name__ == '__main__':
    game = GameEngine()
