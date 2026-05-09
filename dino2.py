from casioplot import *
from random import randint

SCREEN_W = 384
SCREEN_H = 192
GROUND_Y = 160
GRAVITY = 2
JUMP_POWER = 18
DINO_SIZE = 15
GAME_SPEED = 5

class Dino:
    def __init__(self):
        self.x = 50
        self.y = GROUND_Y - DINO_SIZE
        self.w = DINO_SIZE
        self.h = DINO_SIZE
        self.vy = 0
        self.on_ground = True
        self.color = (117, 191, 48)
    
    def jump(self):
        if self.on_ground:
            self.vy = -JUMP_POWER
            self.on_ground = False
    
    def update(self):
        self.vy += GRAVITY
        self.y += self.vy
        
        if self.y >= GROUND_Y - self.h:
            self.y = GROUND_Y - self.h
            self.vy = 0
            self.on_ground = True
    
    def draw(self):
        col = self.color
        x1 = max(0, self.x)
        x2 = min(SCREEN_W - 1, self.x + self.w)
        y1 = max(0, self.y)
        y2 = min(SCREEN_H - 1, self.y + self.h)
        
        for x in range(x1, x2):
            for y in range(y1, y2):
                set_pixel(x, y, col)

class Cactus:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y - 20
        self.w = 15
        self.h = 20
        self.color = (249, 36, 36)
        self.active = True
        self.scored = False
        self.type = 1
    
    def move(self, speed):
        self.x += speed
        if self.x + self.w < 0:
            self.active = False
    
    def draw(self):
        if self.x + self.w < 0 or self.x > SCREEN_W:
            return
        
        col = self.color
        x1 = max(0, self.x)
        x2 = min(SCREEN_W - 1, self.x + self.w)
        y1 = max(0, self.y)
        y2 = min(SCREEN_H - 1, self.y + self.h)
        
        for x in range(x1, x2):
            for y in range(y1, y2):
                set_pixel(x, y, col)
    
    def check_collision(self, dino):
        if dino.x + dino.w > self.x and dino.x < self.x + self.w:
            if dino.y + dino.h > self.y:
                return True
        return False

class Bird:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y - 50
        self.w = 18
        self.h = 12
        self.color = (200, 100, 200)
        self.active = True
        self.scored = False
        self.type = 2
    
    def move(self, speed):
        self.x += speed
        if self.x + self.w < 0:
            self.active = False
    
    def draw(self):
        if self.x + self.w < 0 or self.x > SCREEN_W:
            return
        
        col = self.color
        x1 = max(0, self.x)
        x2 = min(SCREEN_W - 1, self.x + self.w)
        y1 = max(0, self.y)
        y2 = min(SCREEN_H - 1, self.y + self.h)
        
        for x in range(x1, x2):
            for y in range(y1, y2):
                set_pixel(x, y, col)
    
    def check_collision(self, dino):
        if dino.x + dino.w > self.x and dino.x < self.x + self.w:
            if dino.y + dino.h > self.y and dino.y < self.y + self.h:
                return True
        return False

class TallCactus:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_Y - 35
        self.w = 20
        self.h = 35
        self.color = (249, 100, 36)
        self.active = True
        self.scored = False
        self.type = 3
    
    def move(self, speed):
        self.x += speed
        if self.x + self.w < 0:
            self.active = False
    
    def draw(self):
        if self.x + self.w < 0 or self.x > SCREEN_W:
            return
        
        col = self.color
        x1 = max(0, self.x)
        x2 = min(SCREEN_W - 1, self.x + self.w)
        y1 = max(0, self.y)
        y2 = min(SCREEN_H - 1, self.y + self.h)
        
        for x in range(x1, x2):
            for y in range(y1, y2):
                set_pixel(x, y, col)
    
    def check_collision(self, dino):
        if dino.x + dino.w > self.x and dino.x < self.x + self.w:
            if dino.y + dino.h > self.y:
                return True
        return False

def draw_ground():
    col = (0, 0, 0)
    for x in range(SCREEN_W):
        set_pixel(x, GROUND_Y, col)
        set_pixel(x, GROUND_Y + 1, col)

def draw_text_centered(text, y):
    x = (SCREEN_W // 2) - (len(text) * 4)
    draw_string(x, y, text, (0, 0, 0), "medium")

def main():
    dino = Dino()
    obstacles = []
    obstacles.append(Cactus(SCREEN_W))
    obstacles.append(Bird(SCREEN_W + 200))
    obstacles.append(TallCactus(SCREEN_W + 400))
    
    score = 0
    playing = True
    paused = False
    
    JUMP_KEYS = ("24", "95", "EXE", "8")
    EXIT_KEYS = ("12", "EXIT", "AC")
    PAUSE_KEYS = ("36", "MENU")
    
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
        
        clear_screen()
        
        k = str(getkey())
        
        if k in JUMP_KEYS:
            dino.jump()
        elif k in EXIT_KEYS:
            playing = False
        elif k in PAUSE_KEYS:
            paused = True
        
        dino.update()
        
        new_obstacles = []
        for obs in obstacles:
            if obs.active:
                new_obstacles.append(obs)
        obstacles = new_obstacles
        
        if len(obstacles) < 3:
            gap = randint(150, 250)
            last_x = obstacles[-1].x if len(obstacles) > 0 else SCREEN_W
            new_x = last_x + gap
            
            obstacle_type = randint(1, 3)
            if obstacle_type == 1:
                obstacles.append(Cactus(new_x))
            elif obstacle_type == 2:
                obstacles.append(Bird(new_x))
            else:
                obstacles.append(TallCactus(new_x))
        
        for obs in obstacles:
            obs.move(-GAME_SPEED)
            
            if not obs.scored and obs.x + obs.w < dino.x:
                score += 1
                obs.scored = True
            
            if obs.check_collision(dino):
                playing = False
            
            obs.draw()
        
        draw_ground()
        dino.draw()
        
        draw_string(0, 0, "Score: " + str(score), (0, 0, 0), "medium")
        show_screen()
    
    clear_screen()
    draw_text_centered("Game Over", 70)
    draw_text_centered("Score: " + str(score), 90)
    show_screen()
    print("Score: " + str(score))

main()