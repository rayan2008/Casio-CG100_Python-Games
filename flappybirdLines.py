from casioplot import *
from random import randint

"""

import pygame

# Pygame input for debugging w/out calculator
pygame.init()
height = 100
width = 100
screen = pygame.display.set_mode((width,height))
def getkey():
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN: return "24"
"""

class Rect():

    def __init__(self,left,top,right,bottom,colour=(0,0,0)):
        self.top=top
        self.left=left
        self.bottom=bottom
        self.right=right
        self.colour=colour

    def draw(self):
        for x in range(self.left,self.right+1):
            set_pixel(x,self.top,self.colour)
            set_pixel(x,self.bottom,self.colour)
        
        for y in range(self.top+1,self.bottom):
            set_pixel(self.left,y,self.colour)
            set_pixel(self.right,y,self.colour)
    
    def move(self,amountX,amountY):
        self.left=(self.left)+amountX
        self.top=self.top-amountY
        self.right=self.right+amountX
        self.bottom=self.bottom-amountY

class Pipe():
    _registry=[]
    
    def __init__(self,xpos,height):
        self.xpos=xpos
        self.height=191-height
        self.cleared=False
        self.delete=False
        
        self.bottom = Rect(xpos-20,height+30,xpos+20,191,(117, 191, 48))
        self.top = Rect(xpos-20,0,xpos+20,height-30,(117, 191, 48))
        
        Pipe._registry.append(self)
    
    def move(self,amountX,amountY):
        self.bottom.move(amountX,amountY)
        self.top.move(amountX,amountY)
    
    def checkCollisions(self):
        if (bird.top<=self.top.bottom or bird.bottom>=self.bottom.top) and bird.right >= self.top.left and bird.left <= self.bottom.right:
            return True
    
    def birdPassed(self):
        if self.top.right<bird.left and self.cleared==False:
            self.cleared=True
            global score
            score+=1
            Pipe._registry.append(Pipe(380,randint(60,130)))
            self.delete=True
            
    def draw(self):
        self.top.draw()
        self.bottom.draw()

class Bird(Rect):
    def __init__(self,sizeX=20,sizeY=20,startX=40,startY=40,colour=(249, 241, 36)):
        self.colour=colour
        
        self.left=startX-int(1/2*sizeX)
        self.top=startY-int(1/2*sizeY)
        self.right=startX+int(1/2*sizeX)
        self.bottom=startY+int(1/2*sizeY)
    
    def isCrashed(self):
        if self.bottom >=191:
            return True

def centreText(text,colour=(0,0,0),size="large"):
    if size == "large": xAdjust=9
    elif size == "medium": xAdjust=5
    draw_string(191 - (len(text) * xAdjust) , 85, text, colour, size)


def main():
    global bird
    global score
    playing=True
    while playing == True:
        clear_screen()
        
        #moving
        bird.move(0,-5)
        for i in Pipe._registry: i.move(-5,0)
        
        #inputs
        
        key=getkey()
        if key in continueKeys: bird.move(0,10)
        elif key==12: playing = False
        elif key==36: playing = "Pause"

        #collisions
        for i in Pipe._registry:
            i.birdPassed()
            if i.checkCollisions(): playing = False
        if bird.isCrashed(): playing = False
        
        #draws
        for i in Pipe._registry: i.draw()
        bird.draw()
        draw_string(0,0,("Score: "+str(score)),(0,0,0),"medium")
        
        new_pipes=[]
        for i in Pipe._registry:
            if i.delete==False: new_pipes.append(i)
        Pipe._registry=new_pipes
        
        show_screen()
    if playing == "Pause":
        pause()
    else:
        end()

def end():
    centreText(("Score: "+str(score)),(0,0,0),"medium")
    show_screen()
    print("Your score was "+str(score)+" pipes passed")

def pause():
    centreText(("Paused, Score: "+str(score)),(0,0,0),"medium")
    show_screen()
    while not (getkey() in continueKeys):
        pass
    main()

bird = Bird()
score=0
continueKeys=(24,95)
Pipe._registry.append(Pipe(195,95))
Pipe._registry.append(Pipe(380,randint(60,130)))

main()

