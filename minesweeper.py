
import casioplot
import random

# Constants
WIDTH = 384
HEIGHT = 192
CELL_SIZE = 24
GRID_WIDTH = 8
GRID_HEIGHT = 8
OFFSET_X = (WIDTH - GRID_WIDTH * CELL_SIZE) // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT * CELL_SIZE) // 2
NUM_MINES = 10

BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (128, 128, 128)
DARK_GRAY, LIGHT_GRAY = (64, 64, 64), (192, 192, 192)
RED, BLUE, GREEN = (255, 0, 0), (0, 0, 255), (0, 200, 0)
ORANGE, PURPLE = (255, 165, 0), (128, 0, 128)
CURSOR_COLOR = (0, 100, 200)
NUMBER_COLORS = {1: BLUE, 2: GREEN, 3: RED, 4: PURPLE, 5: (128, 0, 0), 6: (0, 128, 128), 7: BLACK, 8: GRAY}
HIDDEN, REVEALED, FLAGGED = 0, 1, 2

class Cell:
    def __init__(self):
        self.is_mine, self.adjacent_mines, self.state = False, 0, HIDDEN

class Board:
    def __init__(self, width, height, num_mines):
        self.width, self.height, self.num_mines = width, height, num_mines
        self.cells = [[Cell() for _ in range(width)] for _ in range(height)]
        self.first_click, self.flags_placed, self.cells_revealed = True, 0, 0
        
    def place_mines(self, safe_x, safe_y):
        mines_placed, safe_cells = 0, set()
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = safe_x + dx, safe_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_cells.add((nx, ny))
        while mines_placed < self.num_mines:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if not self.cells[y][x].is_mine and (x, y) not in safe_cells:
                self.cells[y][x].is_mine, mines_placed = True, mines_placed + 1
        self.calculate_adjacent_mines()
    
    def calculate_adjacent_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if not self.cells[y][x].is_mine:
                    count = sum(1 for dx in range(-1, 2) for dy in range(-1, 2) 
                               if not (dx == 0 and dy == 0) and 0 <= x + dx < self.width 
                               and 0 <= y + dy < self.height and self.cells[y + dy][x + dx].is_mine)
                    self.cells[y][x].adjacent_mines = count
    
    def reveal_cell(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        cell = self.cells[y][x]
        if cell.state != HIDDEN:
            return True
        if self.first_click:
            self.place_mines(x, y)
            self.first_click = False
        if cell.is_mine:
            cell.state = REVEALED
            return False
        to_reveal = [(x, y)]
        while to_reveal:
            cx, cy = to_reveal.pop()
            if cx < 0 or cx >= self.width or cy < 0 or cy >= self.height:
                continue
            ccell = self.cells[cy][cx]
            if ccell.state != HIDDEN or ccell.is_mine:
                continue
            ccell.state, self.cells_revealed = REVEALED, self.cells_revealed + 1
            if ccell.adjacent_mines == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if not (dx == 0 and dy == 0):
                            to_reveal.append((cx + dx, cy + dy))
        return True
    
    def toggle_flag(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        cell = self.cells[y][x]
        if cell.state == HIDDEN:
            cell.state, self.flags_placed = FLAGGED, self.flags_placed + 1
        elif cell.state == FLAGGED:
            cell.state, self.flags_placed = HIDDEN, self.flags_placed - 1
    
    def check_win(self):
        return self.cells_revealed == self.width * self.height - self.num_mines
    
    def reveal_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x].is_mine:
                    self.cells[y][x].state = REVEALED

def draw_cell(x, y, color):
    sx, sy = OFFSET_X + x * CELL_SIZE, OFFSET_Y + y * CELL_SIZE
    for j in range(CELL_SIZE - 2):
        for i in range(CELL_SIZE - 2):
            if i % 2 == 0 or j % 2 == 0:
                casioplot.set_pixel(sx + i + 1, sy + j + 1, color)

def draw_cell_border(x, y, color):
    sx, sy = OFFSET_X + x * CELL_SIZE, OFFSET_Y + y * CELL_SIZE
    for i in range(CELL_SIZE):
        casioplot.set_pixel(sx + i, sy, color)
        casioplot.set_pixel(sx + i, sy + 1, color)
        casioplot.set_pixel(sx + i, sy + CELL_SIZE - 1, color)
        casioplot.set_pixel(sx + i, sy + CELL_SIZE - 2, color)
    for j in range(CELL_SIZE):
        casioplot.set_pixel(sx, sy + j, color)
        casioplot.set_pixel(sx + 1, sy + j, color)
        casioplot.set_pixel(sx + CELL_SIZE - 1, sy + j, color)
        casioplot.set_pixel(sx + CELL_SIZE - 2, sy + j, color)

def draw_mine(x, y):
    sx, sy = OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2, OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2
    for i in range(-4, 5):
        casioplot.set_pixel(sx + i, sy, BLACK)
        casioplot.set_pixel(sx, sy + i, BLACK)
        if i != 0:
            casioplot.set_pixel(sx + i, sy - 1, BLACK)
            casioplot.set_pixel(sx + i, sy + 1, BLACK)
            casioplot.set_pixel(sx - 1, sy + i, BLACK)
            casioplot.set_pixel(sx + 1, sy + i, BLACK)
    for i in [-2, 2]:
        for j in [-2, 2]:
            casioplot.set_pixel(sx + i, sy + j, BLACK)

def draw_flag(x, y):
    sx, sy = OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2 - 3, OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2 - 5
    for i in range(7):
        casioplot.set_pixel(sx, sy + i, DARK_GRAY)
        if i < 2:
            casioplot.set_pixel(sx + 1, sy + i, DARK_GRAY)
    for i in range(5):
        for j in range(4):
            if j <= i // 2 + 1:
                casioplot.set_pixel(sx + j + 1, sy + i, RED)
    casioplot.set_pixel(sx, sy + 7, DARK_GRAY)
    casioplot.set_pixel(sx, sy + 8, DARK_GRAY)

def draw_number(x, y, num):
    if num == 0:
        return
    sx, sy = OFFSET_X + x * CELL_SIZE + CELL_SIZE // 2 - 3, OFFSET_Y + y * CELL_SIZE + CELL_SIZE // 2 - 4
    casioplot.draw_string(sx, sy, str(num), NUMBER_COLORS.get(num, BLACK), "medium")

def draw_single_cell(board, x, y, is_cursor):
    cell = board.cells[y][x]
    if cell.state == REVEALED:
        draw_cell(x, y, LIGHT_GRAY)
        if cell.is_mine:
            draw_mine(x, y)
        else:
            draw_number(x, y, cell.adjacent_mines)
    elif cell.state == FLAGGED:
        draw_cell(x, y, GRAY)
        draw_flag(x, y)
    else:
        draw_cell(x, y, GRAY)
    draw_cell_border(x, y, CURSOR_COLOR if is_cursor else (WHITE if cell.state != REVEALED else DARK_GRAY))

def draw_board(board, cursor_x, cursor_y):
    for y in range(board.height):
        for x in range(board.width):
            draw_single_cell(board, x, y, x == cursor_x and y == cursor_y)

def draw_ui(board):
    casioplot.draw_string(5, 5, "Mines:" + str(board.num_mines - board.flags_placed), BLACK, "small")
    casioplot.draw_string(5, 20, "Arrows/OK/Shift", BLACK, "small")

def main():
    casioplot.clear_screen()
    board = Board(GRID_WIDTH, GRID_HEIGHT, NUM_MINES)
    cursor_x, cursor_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
    old_cursor_x, old_cursor_y = cursor_x, cursor_y
    game_over = False
    won = False
    
    draw_board(board, cursor_x, cursor_y)
    draw_ui(board)
    casioplot.show_screen()
    
    last_key = None
    old_flags = board.flags_placed
    
    while not game_over:
        key = str(casioplot.getkey())
        
        if key == last_key:
            continue
        
        cursor_moved = False
        full_redraw = False
        new_cursor_x, new_cursor_y = cursor_x, cursor_y
        
        if key == "14":
            new_cursor_y = max(0, cursor_y - 1)
            cursor_moved = new_cursor_y != cursor_y
        elif key == "34":
            new_cursor_y = min(board.height - 1, cursor_y + 1)
            cursor_moved = new_cursor_y != cursor_y
        elif key == "23":
            new_cursor_x = max(0, cursor_x - 1)
            cursor_moved = new_cursor_x != cursor_x
        elif key == "25":
            new_cursor_x = min(board.width - 1, cursor_x + 1)
            cursor_moved = new_cursor_x != cursor_x
        elif key == "95":
            if not board.reveal_cell(cursor_x, cursor_y):
                game_over = True
                board.reveal_all_mines()
            elif board.check_win():
                game_over = True
                won = True
            full_redraw = True
        elif key == "24":
            board.toggle_flag(cursor_x, cursor_y)
            full_redraw = True
        
        last_key = key
        
        if cursor_moved:
            # Only redraw the two affected cells
            draw_single_cell(board, old_cursor_x, old_cursor_y, False)
            draw_single_cell(board, new_cursor_x, new_cursor_y, True)
            old_cursor_x, old_cursor_y = new_cursor_x, new_cursor_y
            cursor_x, cursor_y = new_cursor_x, new_cursor_y
            casioplot.show_screen()
        elif full_redraw:
            casioplot.clear_screen()
            draw_board(board, cursor_x, cursor_y)
            draw_ui(board)
            casioplot.show_screen()
            old_flags = board.flags_placed
        
        if old_flags != board.flags_placed:
            draw_ui(board)
            casioplot.show_screen()
            old_flags = board.flags_placed
    
    casioplot.clear_screen()
    draw_board(board, -1, -1)
    
    if won:
        msg_x = WIDTH // 2 - 30
        msg_y = HEIGHT // 2 - 10
        casioplot.draw_string(msg_x, msg_y, "YOU WIN!", GREEN, "large")
    else:
        msg_x = WIDTH // 2 - 40
        msg_y = HEIGHT // 2 - 10
        casioplot.draw_string(msg_x, msg_y, "GAME OVER", RED, "large")
    
    casioplot.show_screen()

main()

