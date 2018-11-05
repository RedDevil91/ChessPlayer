import subprocess
import psutil
import re

MAX_HASH_SIZE = 1048576
MAX_THREAD_COUNT = 128
ENGINE_PATH = r"C:\Users\RedDevil91\StockFish\stockfish-8-win\Windows\stockfish_8_x64.exe"


class StockFishEngine(object):
    best_move_ponder = re.compile("^bestmove\s(?P<best>\w+)\sponder\s(?P<ponder>\w+)$")
    ready_ok = re.compile("^readyok$")

    set_option_cmd = "setoption name"
    start_pos = "position startpos"
    fen_pos = "position fen"

    def __init__(self):
        self.process = None
        return

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return

    def open(self):
        self.process = subprocess.Popen(
            ENGINE_PATH,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True
        )
        self.setOptions()
        return

    def close(self):
        self.runCommand("quit")
        self.process.terminate()
        return

    def runCommand(self, command, *args):
        self.process.stdin.write(command + " ".join(args) + "\n")
        return

    def setOptions(self):
        # TODO: read configs from config file!!!
        self.runCommand("uci")
        thread_cnt = psutil.cpu_count() - 2
        thread_cnt = thread_cnt if thread_cnt <= MAX_THREAD_COUNT else MAX_THREAD_COUNT
        hash_size = psutil.virtual_memory().available
        hash_size = hash_size if hash_size <= MAX_HASH_SIZE else MAX_HASH_SIZE
        self.runCommand(self.set_option_cmd, *["Threads", "value", str(thread_cnt)])
        self.runCommand(self.set_option_cmd, *["Hash", "value", str(hash_size)])
        self.isReady()
        return

    def isReady(self):
        self.runCommand("isready")
        while True:
            line = self.process.stdout.readline().strip()
            if self.ready_ok.match(line):
                return True

    def setPositionFromStart(self, moves=None):
        self.runCommand(self.start_pos, *["moves", *moves] if moves else [])
        return

    def setFenPosition(self, fen):
        self.runCommand(self.fen_pos, *[fen])
        return

    def startCalculation(self, options=None):
        self.runCommand("go", *options if options else [])

    def getBestMove(self):
        while True:
            line = self.process.stdout.readline().strip()
            res = self.best_move_ponder.search(line)
            if res:
                res_dict = res.groupdict()
                return res_dict["best"], res_dict["ponder"]
