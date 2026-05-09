import casioplot
import random

WIDTH, HEIGHT, CELL_SIZE = 384, 192, 4
PLAY_WIDTH, PLAY_HEIGHT = 10, 20
OFFSET_X, OFFSET_Y = (WIDTH // CELL_SIZE - PLAY_WIDTH) // 2, (HEIGHT // CELL_SIZE - PLAY_HEIGHT) // 2

BLACK, WHITE, GRAY = (0, 0, 0), (255, 255, 255), (128, 128, 128)
CYAN, YELLOW, PURPLE = (0, 255, 255), (255, 255, 0), (128, 0, 128)
GREEN, RED, BLUE, ORANGE = (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 165, 0)

SHAPES = {
    'I': [[(0, 0), (1, 0), (2, 0), (3, 0)]],
    'O': [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    'T': [[(1, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (2, 1), (1, 2)],
          [(0, 1), (1, 1), (2, 1), (1, 2)], [(1, 0), (0, 1), (1, 1), (1, 2)]],
    'S': [[(1, 0), (2, 0), (0, 1), (1, 1)], [(1, 0), (1, 1), (2, 1), (2, 2)]],
    'Z': [[(0, 0), (1, 0), (1, 1), (2, 1)], [(2, 0), (1, 1), (2, 1), (1, 2)]],
    'J': [[(1, 0), (1, 1), (0, 2), (1, 2)], [(0, 0), (0, 1), (1, 1), (2, 1)],
          [(0, 0), (1, 0), (0, 1), (0, 2)], [(0, 1), (1, 1), (2, 1), (2, 2)]],
    'L': [[(0, 0), (0, 1), (0, 2), (1, 2)], [(0, 0), (1, 0), (2, 0), (0, 1)],
          [(0, 0), (1, 0), (1, 1), (1, 2)], [(2, 0), (0, 1), (1, 1), (2, 1)]]
}

SHAPE_COLORS = {'I': CYAN, 'O': YELLOW, 'T': PURPLE, 'S': GREEN, 'Z': RED, 'J': BLUE, 'L': ORANGE}
LEFT, RIGHT, DOWN, ROTATE = 23, 25, 34, 24

class Tetromino:
    def __init__(self, shape_type=None):
        self.shape_type = shape_type or random.choice(list(SHAPES.keys()))
        self.rotation = 0
        self.color = SHAPE_COLORS[self.shape_type]
        self.x, self.y = PLAY_WIDTH // 2 - 1, 0
    
    def get_blocks(self):
        return [(self.x + dx, self.y + dy) for dx, dy in SHAPES[self.shape_type][self.rotation]]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.shape_type])
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(PLAY_WIDTH)] for _ in range(PLAY_HEIGHT)]
    
    def is_valid_position(self, tetromino):
        for x, y in tetromino.get_blocks():
            if x < 0 or x >= PLAY_WIDTH or y >= PLAY_HEIGHT:
                return False
            if y >= 0 and self.grid[y][x] is not None:
                return False
        return True
    
    def lock_tetromino(self, tetromino):
        for x, y in tetromino.get_blocks():
            if y >= 0:
                self.grid[y][x] = tetromino.color
    
    def clear_lines(self):
        lines_cleared = 0
        y = PLAY_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y][x] is not None for x in range(PLAY_WIDTH)):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(PLAY_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1
        return lines_cleared
    
    def is_game_over(self):
        return any(self.grid[0][x] is not None for x in range(PLAY_WIDTH))

def draw_cell(x, y, color):
    sx, sy = (OFFSET_X + x) * CELL_SIZE, (OFFSET_Y + y) * CELL_SIZE
    for i in range(CELL_SIZE):
        for j in range(CELL_SIZE):
            casioplot.set_pixel(sx + i, sy + j, color)

def draw_board(board):
    for x in range(PLAY_WIDTH + 2):
        draw_cell(x - 1, -1, GRAY)
        draw_cell(x - 1, PLAY_HEIGHT, GRAY)
    for y in range(PLAY_HEIGHT):
        draw_cell(-1, y, GRAY)
        draw_cell(PLAY_WIDTH, y, GRAY)
    for y in range(PLAY_HEIGHT):
        for x in range(PLAY_WIDTH):
            if board.grid[y][x] is not None:
                draw_cell(x, y, board.grid[y][x])

def draw_tetromino(tetromino):
    for x, y in tetromino.get_blocks():
        if y >= 0:
            draw_cell(x, y, tetromino.color)

def draw_ui(score, level, lines):
    lx = 5
    casioplot.draw_string(lx, 5, "Score:", BLACK, "small")
    casioplot.draw_string(lx, 20, str(score), BLACK, "small")
    casioplot.draw_string(lx, 40, "Lines:", BLACK, "small")
    casioplot.draw_string(lx, 55, str(lines), BLACK, "small")
    casioplot.draw_string(lx, 75, "Level:", BLACK, "small")
    casioplot.draw_string(lx, 90, str(level), BLACK, "small")

def main():
    casioplot.clear_screen()
    board = Board()
    current_tetromino = Tetromino()
    score, lines_cleared_total, level = 0, 0, 1
    game_over = False
    DROP_DELAY, drop_counter, tick = 15, 0, 0
    last_key = None
    
    draw_board(board)
    draw_tetromino(current_tetromino)
    draw_ui(score, level, lines_cleared_total)
    casioplot.show_screen()
    
    while not game_over:
        tick += 1
        if tick % 2 == 0:
            continue
        
        needs_redraw = False
        key = str(casioplot.getkey())
        
        if key == str(LEFT):
            current_tetromino.move(-1, 0)
            if not board.is_valid_position(current_tetromino):
                current_tetromino.move(1, 0)
            else:
                needs_redraw = True
        elif key == str(RIGHT):
            current_tetromino.move(1, 0)
            if not board.is_valid_position(current_tetromino):
                current_tetromino.move(-1, 0)
            else:
                needs_redraw = True
        elif key == str(DOWN):
            current_tetromino.move(0, 1)
            if not board.is_valid_position(current_tetromino):
                current_tetromino.move(0, -1)
            else:
                score += 1
                needs_redraw = True
        elif key == str(ROTATE) and key != last_key:
            old_rotation = current_tetromino.rotation
            current_tetromino.rotate()
            if not board.is_valid_position(current_tetromino):
                for dx in [1, -1, 2, -2]:
                    current_tetromino.move(dx, 0)
                    if board.is_valid_position(current_tetromino):
                        needs_redraw = True
                        break
                    current_tetromino.move(-dx, 0)
                else:
                    current_tetromino.rotation = old_rotation
            else:
                needs_redraw = True
        
        last_key = key
        
        drop_counter += 1
        drop_speed = max(3, DROP_DELAY - level)
        
        if drop_counter >= drop_speed:
            drop_counter = 0
            current_tetromino.move(0, 1)
            
            if not board.is_valid_position(current_tetromino):
                current_tetromino.move(0, -1)
                board.lock_tetromino(current_tetromino)
                lines = board.clear_lines()
                if lines > 0:
                    lines_cleared_total += lines
                    line_scores = [0, 100, 300, 500, 800]
                    score += line_scores[min(lines, 4)] * level
                    level = lines_cleared_total // 10 + 1
                
                if board.is_game_over():
                    game_over = True
                else:
                    current_tetromino = Tetromino()
                    if not board.is_valid_position(current_tetromino):
                        game_over = True
                needs_redraw = True
            else:
                needs_redraw = True
        
        if needs_redraw:
            casioplot.clear_screen()
            draw_board(board)
            draw_tetromino(current_tetromino)
            draw_ui(score, level, lines_cleared_total)
            casioplot.show_screen()
    
    casioplot.clear_screen()
    casioplot.draw_string(WIDTH // 2 - 50, HEIGHT // 2 - 20, "GAME OVER", RED, "large")
    casioplot.draw_string(WIDTH // 2 - 40, HEIGHT // 2 + 10, "Score: " + str(score), BLACK, "medium")
    casioplot.draw_string(WIDTH // 2 - 40, HEIGHT // 2 + 30, "Lines: " + str(lines_cleared_total), BLACK, "medium")
    casioplot.show_screen()

main()