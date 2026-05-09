from casioplot import *
from random import randint

# Global Constants for Performance
SCREEN_W = 384
SCREEN_H = 191
PIPE_W = 40
BIRD_SIZE = 20
GRAVITY = 5
JUMP = 15 

# --- Pipe and Bird Classes ---

class Pipe:
    def __init__(self, x, gap_height):
        self.x = x
        self.w = PIPE_W
        self.gap_top_y = gap_height - 30
        self.gap_bot_y = gap_height + 30
        self.color = (117, 191, 48)
        self.cleared = False
        self.active = True

    def move(self, speed):
        self.x += speed
        # Pipe is marked inactive when fully off screen OR when scored (new logic handled in main)
        if self.x + self.w <= 0:
            self.active = False

    def draw(self):
        x_start = self.x
        x_end = self.x + self.w
        col = self.color
        
        if x_end < 0 or x_start > SCREEN_W: return
        draw_x1 = max(0, x_start)
        draw_x2 = min(SCREEN_W - 1, x_end)

        # Draw Top Pipe
        if self.gap_top_y > 0:
            for x in range(draw_x1, draw_x2):
                for y in range(0, self.gap_top_y):
                    set_pixel(x, y, col)

        # Draw Bottom Pipe
        if self.gap_bot_y < SCREEN_H:
            for x in range(draw_x1, draw_x2):
                for y in range(self.gap_bot_y, SCREEN_H + 1):
                    set_pixel(x, y, col)

    def check_collision(self, b_x, b_y, b_size):
        b_right = b_x + b_size
        b_bottom = b_y + b_size // 2
        b_top = b_y - b_size // 2

        p_left = self.x
        p_right = self.x + self.w

        if b_right > p_left and b_x - (b_size // 2) < p_right:
            if b_top < self.gap_top_y or b_bottom > self.gap_bot_y:
                return True
        return False

class Bird:
    def __init__(self):
        self.x = 40
        self.y = 40
        self.size = BIRD_SIZE
        self.color = (249, 241, 36)
        self.half_size = int(self.size / 2)

    def draw(self):
        x1 = self.x - self.half_size
        y1 = self.y - self.half_size
        
        col = self.color
        
        start_x = max(0, x1)
        end_x = min(SCREEN_W - 1, x1 + self.size)
        start_y = max(0, y1)
        end_y = min(SCREEN_H - 1, y1 + self.size)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                set_pixel(x, y, col)

    def update(self, dy):
        self.y += dy

    def is_crashed(self):
        if (self.y + self.half_size) >= SCREEN_H:
            return True
        return False

def draw_text_centered(text, y):
    x = (SCREEN_W // 2) - (len(text) * 4) 
    draw_string(x, y, text, (0,0,0), "medium")

# --- Main Logic with Object Limit ---

def main():
    bird = Bird()
    pipes = []
    
    # Initialize with 3 pipes spread out
    pipes.append(Pipe(195, 95))
    pipes.append(Pipe(195 + 165, randint(30, 125))) # 360
    pipes.append(Pipe(195 + 165 * 2, randint(30, 125))) # 525
    
    score = 0
    playing = True
    paused = False
    
    JUMP_KEYS = ("24", "95", "EXE", "8") 
    EXIT_KEYS = ("12", "EXIT", "AC")
    PAUSE_KEYS = ("36", "MENU")
    
    # Constant defining the maximum number of pipes allowed on screen
    MAX_PIPES = 3
    # The X position gap used to space new pipes
    PIPE_SPACING = 165 

    while playing:
        if paused:
            draw_text_centered("Paused. Score: " + str(score), 90)
            show_screen()
            
            k = str(getkey())
            if k in JUMP_KEYS:
                paused = False
            elif k in EXIT_KEYS:
                playing = False
            continue

        # --- Game Logic ---
        clear_screen()

        # 1. Input
        k = str(getkey())
        
        # 2. Bird Physics
        bird_dy = GRAVITY 
        
        if k in JUMP_KEYS:
            bird_dy = -JUMP
        elif k in EXIT_KEYS:
            playing = False
        elif k in PAUSE_KEYS:
            paused = True

        bird.update(bird_dy)

        # 3. Pipe Logic and Drawing
        
        # Filter (removes pipes marked 'active = False' either by being off-screen OR by scoring)
        new_pipes = []
        for p in pipes:
            if p.active:
                new_pipes.append(p)
        pipes = new_pipes
        
        #Maintain exactly MAX_PIPES
        if len(pipes) < MAX_PIPES:
            # Calculate the x-position for the new pipe, based on the last pipe's position
            new_x = SCREEN_W # Start off screen
            if len(pipes) > 0:
                new_x = pipes[-1].x + PIPE_SPACING
            
            pipes.append(Pipe(new_x, randint(30, 125)))

        # Move, Score, and Check Collision
        for p in pipes:
            p.move(-5)
            
            # Score counting logic:
            if not p.cleared and (p.x + p.w) < (bird.x - bird.half_size):
                score += 1
                p.cleared = True
                #Mark pipe inactive immediately when score is incremented**
                p.active = False
            
            if p.check_collision(bird.x, bird.y, bird.size):
                playing = False
            
            p.draw()

        # 4. Bird Logic & Draw
        if bird.is_crashed():
            playing = False
        
        bird.draw()
        
        # 5. UI
        draw_string(0, 0, "Score: " + str(score), (0,0,0), "medium")
        show_screen()

    # End Screen
    draw_text_centered("Game Over", 70)
    draw_text_centered("Score: " + str(score), 90)
    show_screen()
    print("Score: " + str(score))

main()