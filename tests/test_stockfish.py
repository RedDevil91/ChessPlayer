import unittest

from stockfish_interface import StockFishEngine


class TestStockFishEngine(unittest.TestCase):
    def run(self, result=None):
        with StockFishEngine() as engine:
            self.engine = engine
            super(TestStockFishEngine, self).run(result)

    def test_startpos_wo_move(self):
        self.engine.setPositionFromStart()
        self.engine.startCalculation()
        next_move, ponder = self.engine.getBestMove()
        return

    def test_startpos_w_move(self):
        self.engine.setPositionFromStart(["e2e4", "e7e5"])
        self.engine.startCalculation()
        next_move, ponder = self.engine.getBestMove()
        return

    def test_fenpos(self):
        self.engine.setFenPosition("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
        self.engine.startCalculation()
        next_move, ponder = self.engine.getBestMove()
        return


if __name__ == '__main__':
    unittest.main()
