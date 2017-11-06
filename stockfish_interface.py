import subprocess
import time
import psutil

stockfish_engine_pth = r"C:\Users\RedDevil91\StockFish\stockfish-8-win\Windows\stockfish_8_x64.exe"


class StockFishEngine(object):
    def __init__(self, depth=20):
        self.stockfish_proc = subprocess.Popen(
            stockfish_engine_pth,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        self.depth = depth
        self.setOptions()
        return

    def setOptions(self):
        self.newCommand("uci")
        self.isReady()
        thread_cnt = psutil.cpu_count() - 2
        hash_size = psutil.virtual_memory().available / (2 * 1024 * 1024)
        self.newCommand("setoption name Threads value %d" % thread_cnt)
        self.isReady()
        self.newCommand("setoption name Hash value %d" % int(hash_size))
        self.isReady()
        return

    def newCommand(self, command):
        self.stockfish_proc.stdin.write(command + "\n")
        return

    def isReady(self):
        self.newCommand("isready")
        while True:
            line = self.stockfish_proc.stdout.readline().strip()
            if line == "readyok":
                return True

    def setPositionFromStart(self, moves):
        move_str = " ".join(moves)
        self.newCommand("position startpos moves %s" % move_str)
        return

    def setFenPosition(self, fen):
        self.newCommand("position fen %s" % fen)
        return

    def getBestMove(self):
        self.newCommand("go depth %d" % self.depth)
        while True:
            line = self.stockfish_proc.stdout.readline().strip()
            if line.startswith("bestmove"):
                break
        return line.split(" ")[1]


if __name__ == '__main__':
    chess_engine = StockFishEngine()
    start = time.time()
    test_moves = ["e2e4", "e7e5"]
    chess_engine.setPositionFromStart(test_moves)
    next_move = chess_engine.getBestMove()
    test_moves.append(next_move)
    print(next_move)
    chess_engine.setPositionFromStart(test_moves)
    next_move = chess_engine.getBestMove()
    print(next_move)
    print(time.time() - start)

    start = time.time()
    chess_engine.setFenPosition("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w")
    next_move = chess_engine.getBestMove()
    print(next_move)
    print(time.time() - start)
    print("END")
