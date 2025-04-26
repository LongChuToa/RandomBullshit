import random
class TicTacToeLogic:
    """
    Chứa logic của game Tic-Tac-Toe.
    """
    def __init__(self):
        self.last_game_first_player = ''
        self.reset_game()
        self.win_count = [0, 0, 0]

    def reset_game(self):
        """Đặt lại trạng thái bảng cờ và người chơi."""
        self.board = [[' ' for _ in range(3)] for _ in range(3)] # Bảng 3x3, ' ' là ô trống
        self.prio_board = [[2, 4, 2],
                           [4, 3, 4],
                           [2, 4, 2]]
        self.current_player = 'X' if self.last_game_first_player == 'O' else 'O'
        self.last_game_first_player = self.current_player
        self.game_over = False
        self.winner = None # 'X', 'O', 'Draw', or None


    def make_move(self, row, col):
        """
        Xử lý nước đi của người chơi.
        Trả về True nếu nước đi hợp lệ và được thực hiện, False nếu không.
        """
        if self.game_over:
            # Nếu game kết thúc, không cho phép đi tiếp
            return False

        # Kiểm tra xem ô có hợp lệ và trống không
        if 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == ' ':
            self.board[row][col] = self.current_player # Đánh dấu vào ô
            self.prio_board[row][col] = -1
            # Kiểm tra thắng sau nước đi
            if self._check_win(self.current_player):
                self.winner = self.current_player
                self.win_count[0 if self.winner == 'X' else 2] += 1
                self.game_over = True
            # Kiểm tra hòa (chỉ khi chưa có ai thắng)
            elif self._check_draw():
                self.winner = 'Draw'
                self.win_count[1] += 1
                self.game_over = True
            else:
                # Chuyển lượt chơi nếu game chưa kết thúc
                # Thực tế, máy sẽ chơi tiếp tại đây
                self._switch_player()

            return True # Nước đi hợp lệ
        else:
            return False # Nước đi không hợp lệ (ô đã đầy hoặc ngoài bảng)

    def _switch_player(self):
        """Chuyển đổi giữa 'X' và 'O'."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def _check_win(self, player):
        """Kiểm tra xem người chơi 'player' có thắng không."""
        # Kiểm tra hàng ngang
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == player:
                return True

        # Kiểm tra hàng dọc
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == player:
                return True

        # Kiểm tra đường chéo chính
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == player:
            return True

        # Kiểm tra đường chéo phụ
        if self.board[0][2] == self.board[1][1] == self.board[0][2] == player: # Lưu ý: board[0][2] != board[2][0]
             if self.board[0][2] == self.board[1][1] == self.board[2][0] == player: # Sửa lỗi logic
                 return True


        return False

    def _check_draw(self):
        """Kiểm tra xem game có hòa không (tất cả ô đầy mà không có ai thắng)."""
        # Kiểm tra xem còn ô trống nào không
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    return False # Vẫn còn ô trống, chưa hòa
        return True # Hết ô trống

    # Các hàm getter để truy cập trạng thái từ bên ngoài
    def get_board(self):
        return self.board

    def get_current_player(self):
        return self.current_player

    def is_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner

    def print_win_count(self):
        print(f"X win: {self.win_count[0]}\nO win: {self.win_count[2]}\nDraw: {self.win_count[1]}")

    # Method dành cho bot
    def check_prio(self, pos, signal):
        row, col = pos

        # Check hàng
        count = 0
        empty = None
        for c in range(3):
            if self.board[row][c] == signal:
                count += 1
            elif self.board[row][c] == ' ':
                empty = c
        if count == 2 and empty is not None:
            self.prio_board[row][empty] = 1 if signal == 'X' else 0

        # Check cột
        count = 0
        empty = None
        for r in range(3):
            if self.board[r][col] == signal:
                count += 1
            elif self.board[r][col] == ' ':
                empty = r
        if count == 2 and empty is not None:
            self.prio_board[empty][col] = 1 if signal == 'X' else 0

        # Check đường chéo chính
        if row == col:
            count = 0
            empty = None
            for i in range(3):
                if self.board[i][i] == signal:
                    count += 1
                elif self.board[i][i] == ' ':
                    empty = i
            if count == 2 and empty is not None:
                self.prio_board[empty][empty] = 1 if signal == 'X' else 0

        # Check đường chéo phụ
        if row + col == 2:
            count = 0
            empty = None
            for i in range(3):
                if self.board[i][2 - i] == signal:
                    count += 1
                elif self.board[i][2 - i] == ' ':
                    empty = i
            if count == 2 and empty is not None:
                self.prio_board[empty][2 - empty] = 1 if signal == 'X' else 0

    def change_prio(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] in ['X', 'O']:
                    self.check_prio((row, col), self.board[row][col])

    def bot_playing(self):
        min_prio = 99
        best_moves = []
        self.change_prio()

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    if self.prio_board[i][j] < min_prio:
                        min_prio = self.prio_board[i][j]
                        best_moves = [(i, j)]
                    elif self.prio_board[i][j] == min_prio:
                        best_moves.append((i, j))
        if best_moves:
            row, col = random.choice(best_moves)
            return row, col
        else:
            return -1, -1
