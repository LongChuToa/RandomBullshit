import numpy as np

class Log:
    """
    Log là nơi để lưu lại các nước đánh của người và máy
    Có tác dụng trong việc học máy
    """
    def __init__(self):
        self.file = 'game_log.txt'
        self.predicted_board = np.zeros((3, 3), dtype=int)
        self.Xbias = np.zeros((3, 3), dtype=int)
        self.Obias = np.zeros((3, 3), dtype=int)
        self.turn = 1


    def read(self):
        self.predicted_board = []
        with open(self.file, 'r', encoding='utf-8') as f:
            for line in f:
                row = list(map(int, line.strip().split()))
                self.predicted_board.append(row)

    def write(self, new_predict_board):
        with open(self.file, 'w', encoding='utf-8') as f:
            for row in new_predict_board:
                line = ' '.join(map(str, row))
                f.write(line + '\n')

    def save(self, pos, signal):
        row, col = pos
        self.predicted_board[row][col] += 3
        if signal == 'X':
            self.Xbias[row][col] += 1
        else:
            self.Obias[row][col] += 1

    def _reset_bias(self):
        self.Xbias = np.zeros((3, 3), dtype=int)
        self.Obias = np.zeros((3, 3), dtype=int)

    def winner_learn(self, signal):
        if signal == 'X':
            self.predicted_board = (self.predicted_board - self.Obias) * self.Xbias - self.predicted_board
        elif signal == 'O':
            self.predicted_board = (self.predicted_board - self.Xbias) * self.Obias - self.predicted_board
        self._reset_bias()

    def print(self):
        print (self.predicted_board)
