import pygame

# --- Cài đặt Màn hình & Màu sắc (có thể đặt ở đây hoặc main và truyền vào) ---
# Giả định kích thước ô và màu sắc được truyền vào hoặc định nghĩa cục bộ
# Để đơn giản, ta định nghĩa lại các hằng số cần thiết cho việc vẽ
CELL_SIZE = 100 # Kích thước mỗi ô vuông (giả định khớp với logic)
SCREEN_WIDTH_GUI = CELL_SIZE * 3
BOARD_SIZE_GUI = SCREEN_WIDTH_GUI
STATUS_BAR_HEIGHT_GUI = 50 # Không gian cho dòng trạng thái
SCREEN_HEIGHT_GUI = BOARD_SIZE_GUI + STATUS_BAR_HEIGHT_GUI

# Màu sắc (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Font
pygame.font.init() # Khởi tạo font nếu chưa được khởi tạo ở main (an toàn)
font = pygame.font.SysFont(None, 30)

class TicTacToeGUI:
    """
    Chứa các phương thức để vẽ giao diện game Tic-Tac-Toe bằng Pygame.
    """
    def __init__(self, screen):
        """
        screen: Đối tượng surface của Pygame để vẽ lên.
        """
        self.screen = screen
        self.cell_size = CELL_SIZE # Sử dụng CELL_SIZE được định nghĩa ở trên
        self.board_size = BOARD_SIZE_GUI
        self.status_bar_height = STATUS_BAR_HEIGHT_GUI
        self.screen_width = SCREEN_WIDTH_GUI
        self.screen_height = SCREEN_HEIGHT_GUI # Tổng chiều cao cửa sổ


    def draw(self, board, current_player, winner):
        """
        Vẽ toàn bộ giao diện game dựa trên trạng thái logic hiện tại.
        board: Bảng cờ 3x3 từ logic.
        current_player: Người chơi hiện tại từ logic.
        winner: Kết quả game ('X', 'O', 'Draw', None) từ logic.
        """
        self._draw_board()
        self._draw_marks(board)
        self._display_status(current_player, winner)

    def _draw_board(self):
        """Vẽ lưới bảng cờ."""
        # Vẽ nền phần bảng
        self.screen.fill(BLACK, (0, 0, self.board_size, self.board_size)) # Vẽ nền trắng cho phần bảng

        # Vẽ 2 đường dọc
        pygame.draw.line(self.screen, WHITE, (self.cell_size, 0), (self.cell_size, self.board_size), 3)
        pygame.draw.line(self.screen, WHITE, (self.cell_size * 2, 0), (self.cell_size * 2, self.board_size), 3)

        # Vẽ 2 đường ngang
        pygame.draw.line(self.screen, WHITE, (0, self.cell_size), (self.board_size, self.cell_size), 3)
        pygame.draw.line(self.screen, WHITE, (0, self.cell_size * 2), (self.board_size, self.cell_size * 2), 3)

    def _draw_marks(self, board):
        """Vẽ ký hiệu X và O lên bảng."""
        for row in range(3):
            for col in range(3):
                mark = board[row][col]
                # Tính toán tâm của ô
                center_x = col * self.cell_size + self.cell_size // 2
                center_y = row * self.cell_size + self.cell_size // 2

                if mark == 'X':
                    # Vẽ X (hai đường chéo)
                    pygame.draw.line(self.screen, BLUE, (center_x - 30, center_y - 30), (center_x + 30, center_y + 30), 5)
                    pygame.draw.line(self.screen, BLUE, (center_x + 30, center_y - 30), (center_x - 30, center_y + 30), 5)
                elif mark == 'O':
                    # Vẽ O (hình tròn)
                    pygame.draw.circle(self.screen, RED, (center_x, center_y), 40, 5)

    def _display_status(self, current_player, winner):
        """Hiển thị dòng trạng thái (ai đi, ai thắng, hòa)."""
        # Vẽ nền cho khu vực trạng thái
        status_bar_y = self.board_size # Vị trí y bắt đầu của thanh trạng thái
        self.screen.fill(GRAY, (0, status_bar_y, self.screen_width, self.status_bar_height)) # Nền xám

        text = ""
        if winner == 'Draw':
            text = "Draw!"
        elif winner:
            text = f"'{winner}' Win!"
        else:
            text = f"'{current_player}''s turn"

        # Render text
        status_text_surface = font.render(text, True, WHITE)
        # Lấy hình chữ nhật bao quanh text để căn giữa
        text_rect = status_text_surface.get_rect(center=(self.screen_width // 2, status_bar_y + self.status_bar_height // 2))

        # Vẽ text lên màn hình
        self.screen.blit(status_text_surface, text_rect)

    def get_cell_from_coords(self, x, y):
        """
        Chuyển đổi tọa độ pixel (x, y) trên màn hình sang chỉ số (row, col) của bảng.
        Trả về (row, col) hoặc (-1, -1) nếu click ngoài khu vực bảng.
        """
        # Chỉ xử lý click trong phạm vi bảng cờ (phần trên)
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            row = y // self.cell_size
            col = x // self.cell_size
            return (row, col)
        else:
            return (-1, -1) # Click ngoài bảng