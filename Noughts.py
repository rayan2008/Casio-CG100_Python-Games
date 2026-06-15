# Maintainer: Chiron Horwood
# Github: Chiron8
# Email: chiron.dev8@gmail.com

# The calculator doesn't support the time package so I just have the turtle move round a couple times to give the same effect

from turtle import *
#variables
pos = [[0, 0], [-100, -60], [-5, -60], [85, -60], [-100, -5], [-5, -5], [85, -5], [-100, 45], [-5, 45], [85, 45]]
plays = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
turn = 0
won = 2
key = 0
full = False

#turtle config
speed("fastest")
pencolor("black")
width(3)
hideturtle()

#grid
for i in [-50, 50]:
  penup()
  setposition(i, 75)
  pendown()
  goto(i, -75)

for i in [-25, 25]:
  penup()
  setposition(-125, i)
  pendown()
  goto(125, i)

#pause
penup()
for i in range(1, 10):
    goto(-100, -100)
    goto(100, 100)

#main loop
while won == 2:
  penup()
  pencolor("black")
  for i in range(1, 10):
    goto(-100, -100)
    goto(100, 100)
  if full == True:
    clear()
    penup()
    goto(-150, 0)
    pendown()
    write("Draw")
    penup()
    won = -1
    break
    
  key = int(input("Enter Key: "))
  if plays[key] == 2:
    setposition(pos[key][0], pos[key][1])
    pendown()
    if turn == 1:
      pencolor("orange")
      goto(xcor()+10, ycor()+10)
      penup()
      setposition(xcor()-10, ycor())
      pendown()
      goto(xcor()+10, ycor()-10)
      turn = 0
      plays[key] = 1
      penup()
    elif turn == 0:
      pencolor("blue")
      goto(xcor()+10, ycor())
      goto(xcor(), ycor()+10)
      goto(xcor()-10, ycor())
      goto(xcor(), ycor()-10)
      turn = 1
      plays[key] = 0
      penup()

    pencolor("red")
    full = True
    for i in range(1, 9):
      if plays[i] == 2:
        full = False
      if i == 1 or i == 4 or i == 9:
        if plays[i] == plays[i+1] == plays[i+2] and plays[i] != 2:
          won = plays[i]
          setposition(pos[i][0]+5, pos[i][1]+5)
          pendown()
          goto(pos[i+2][0]+5, pos[i+2][1]+5)
          penup()
      if i == 7 or i == 8 or i == 9:
        if plays[i] == plays[i-3] == plays[i-6] and plays[i] != 2:
          won = plays[i]
          setposition(pos[i][0]+5, pos[i][1]+5)
          pendown()
          goto(pos[i-6][0]+5, pos[i-6][1]+5)
          penup()
      if i == 1:
        if plays[i] == plays[i+4] == plays[i+8] and plays[i] != 2:
          won = plays[1]
          setposition(pos[i][0]+5, pos[i][1]+5)
          pendown()
          goto(pos[i+8][0]+5, pos[i+8][1]+5)
          penup()
      if i == 7:
        if plays[i] == plays[i-2] == plays[i-4] and plays[i] != 2:
          won = plays[7]
          setposition(pos[i][0]+5, pos[i][1]+5)
          pendown()
          goto(pos[i-4][0]+5, pos[i-4][1]+5)
          penup()

  else:
    print("Already played, try again")

for i in range(1, 7):
    goto(-100, -100)
    goto(100, 100)

clear()
pencolor("black")


if won == 0:
  penup()
  goto(-150, 0)
  pendown()
  write("Noughts wins!")
else:
  penup()
  goto(-150, 0)
  pendown()
  write("Crosses wins!")

penup()
for i in range(1, 10):
    goto(-100, -100)
    goto(100, 100)
x = input()
