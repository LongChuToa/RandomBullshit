import pygame
import sys
import time
from logic import TicTacToeLogic # Import lớp logic game
from gui import TicTacToeGUI     # Import lớp GUI
from log import Log

# --- Cài đặt chung (có thể dùng chung hằng số với GUI nếu muốn, hoặc định nghĩa lại) ---
# Lấy kích thước từ GUI để đảm bảo khớp
CELL_SIZE = 100 # Đảm bảo khớp với GUI
SCREEN_WIDTH = CELL_SIZE * 3
BOARD_SIZE = SCREEN_WIDTH
STATUS_BAR_HEIGHT = 50
SCREEN_HEIGHT = BOARD_SIZE + STATUS_BAR_HEIGHT
GAME_MODE = 'EVE'

# --- Khởi tạo Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# --- Tạo đối tượng Logic và GUI ---
game_logic = TicTacToeLogic()
game_gui = TicTacToeGUI(screen) # Truyền đối tượng screen cho GUI
game_log = Log()

# --- Các hàm cần ---
def screen_update():
    # --- Vẽ/Render ---
    # Yêu cầu GUI vẽ lại toàn bộ màn hình dựa trên trạng thái hiện tại của logic
    game_gui.draw(game_logic.get_board(), game_logic.get_current_player(), game_logic.get_winner())
    # --- Cập nhật hiển thị ---
    pygame.display.flip() # Hoặc pygame.display.update()

def bot_turn():
    row, col = game_logic.bot_playing()
    game_log.save((row, col), game_logic.current_player)
    if game_logic.is_game_over():
        game_logic.reset_game()
    else:
        game_logic.make_move(row, col)

# --- Vòng lặp game chính ---
running = True
while running:
    # --- Xử lý sự kiện ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Sự kiện đóng cửa sổ
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and GAME_MODE != 'EVE': # Sự kiện nhấp chuột
            mouse_x, mouse_y = event.pos
            # Chuyển tọa độ pixel sang chỉ số hàng/cột bằng phương thức của GUI
            clicked_row, clicked_col = game_gui.get_cell_from_coords(mouse_x, mouse_y)
            game_log.save((clicked_row, clicked_col), game_logic.current_player)
            # Kiểm tra xem click có nằm trong bảng không và game chưa kết thúc
            if clicked_row != -1 and clicked_col != -1:
                if game_logic.is_game_over():
                    # Nếu game kết thúc và người dùng click vào bảng, reset game
                    game_logic.reset_game()
                else:
                    # Nếu game chưa kết thúc, thử thực hiện nước đi
                    game_logic.make_move(clicked_row, clicked_col)
            # Có thể thêm logic xử lý click ngoài bảng ở đây nếu cần

    if GAME_MODE == 'PVE':
        if game_logic.current_player == 'O':
            bot_turn()

    elif GAME_MODE == 'EVE':
        if game_logic.current_player in ['X', 'O']:
            bot_turn()
            screen_update()
            time.sleep(0.2)

    if GAME_MODE != 'EVE':
        screen_update()

# --- Kết thúc Pygame ---
pygame.quit()
game_log.print()
game_logic.print_win_count()
sys.exit()