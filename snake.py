import casioplot
import random

# Constants
WIDTH = 384
HEIGHT = 192
CELL_SIZE = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        # Start in the middle of the screen
        start_x = (WIDTH // CELL_SIZE) // 2
        start_y = (HEIGHT // CELL_SIZE) // 2
        self.body = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.growing = False
        
    def get_head(self):
        return self.body[0]
    
    def move(self):
        # Update direction (prevent 180-degree turns)
        if (self.direction[0] + self.next_direction[0] != 0 or 
            self.direction[1] + self.next_direction[1] != 0):
            self.direction = self.next_direction
        
        # Calculate new head position
        head = self.get_head()
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Insert new head
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
    
    def grow(self):
        self.growing = True
    
    def check_collision(self):
        head = self.get_head()
        
        # Check wall collision
        if (head[0] < 0 or head[0] >= WIDTH // CELL_SIZE or
            head[1] < 0 or head[1] >= HEIGHT // CELL_SIZE):
            return True
        
        # Check self collision
        if head in self.body[1:]:
            return True
        
        return False
    
    def set_direction(self, direction):
        if self.next_direction == direction:
            return False
        self.next_direction = direction
        return True

class Food:
    def __init__(self, snake):
        self.position = self.spawn(snake)
    
    def spawn(self, snake):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1)
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1)
            if (x, y) not in snake.body:
                return (x, y)
    
    def respawn(self, snake):
        self.position = self.spawn(snake)

def draw_cell(x, y, color):
    """Draw a cell (scaled pixel) on the screen"""
    for i in range(CELL_SIZE):
        for j in range(CELL_SIZE):
            casioplot.set_pixel(x * CELL_SIZE + i, y * CELL_SIZE + j, color)

def draw_snake(snake):
    """Draw the entire snake"""
    # Draw head in a different color
    head = snake.get_head()
    draw_cell(head[0], head[1], BLUE)
    
    # Draw body
    for segment in snake.body[1:]:
        draw_cell(segment[0], segment[1], GREEN)

def draw_food(food):
    """Draw the food"""
    draw_cell(food.position[0], food.position[1], RED)

def draw_score(score):
    """Draw the score on screen"""
    casioplot.draw_string(5, 5, "Score: " + str(score), BLACK, "small")

def get_input(snake, iteration):
    """Simulate input based on iteration (you can modify this for actual input)"""
    return str(casioplot.getkey())

def main():
    # Initialize game
    casioplot.clear_screen()
    snake = Snake()
    food = Food(snake)
    score = 0
    game_over = False
    
    # Game settings
    MOVE_DELAY = 10  # Move snake every X iterations
    iteration = 0
    
    # Main game loop
    while not game_over:
        iteration += 1
        
        # Get input
        key = get_input(snake, iteration)
        if key == "14":
            snake.set_direction(UP)
        elif key == "23":
            snake.set_direction(LEFT)
        elif key == "25":
            snake.set_direction(RIGHT)
        elif key == "34":
            snake.set_direction(DOWN)

        # Only move snake every MOVE_DELAY iterations
        if iteration % MOVE_DELAY == 0:
            # Move snake
            snake.move()
            
            # Check if snake ate food
            if snake.get_head() == food.position:
                snake.grow()
                food.respawn(snake)
                score += 10
            
            # Check for collisions
            if snake.check_collision():
                game_over = True
            
            # Clear screen and redraw
            casioplot.clear_screen()
            draw_snake(snake)
            draw_food(food)
            draw_score(score)
            casioplot.show_screen()
    
    # Game over screen
    casioplot.clear_screen()
    casioplot.draw_string(WIDTH // 2 - 50, HEIGHT // 2 - 10, "GAME OVER", RED, "large")
    casioplot.draw_string(WIDTH // 2 - 40, HEIGHT // 2 + 20, "Score: " + str(score), WHITE, "medium")
    casioplot.show_screen()

main()