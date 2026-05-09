import casioplot
import random

W,H=384,192
BK,WH,RD,GR,YL,CY=(0,0,0),(255,255,255),(255,0,0),(0,255,0),(255,255,0),(0,255,255)
BL,OR=(0,0,255),(255,165,0)

class P:
 def __init__(s):
  s.x,s.y,s.a,s.lv=W//2-8,H-25,1,3
 def m(s,d):
  s.x=max(10,min(W-26,s.x+d))
 def d(s):
  if s.a:
   c=s.x+8
   for i in range(-2,3):
    casioplot.set_pixel(c+i,s.y,GR)
    casioplot.set_pixel(c+i,s.y+1,GR)
   for i in range(-4,5):
    casioplot.set_pixel(c+i,s.y+4,GR)
    casioplot.set_pixel(c+i,s.y+5,GR)
   for i in range(-6,7):
    casioplot.set_pixel(c+i,s.y+7,GR)
    casioplot.set_pixel(c+i,s.y+8,GR)
    casioplot.set_pixel(c+i,s.y+9,GR)
   casioplot.set_pixel(c,s.y+2,GR)
   casioplot.set_pixel(c,s.y+3,GR)

class B:
 def __init__(s,x,y,e=0):
  s.x,s.y,s.e,s.a=x,y,e,1
 def u(s):
  s.y+=3 if s.e else -5
  if s.y<0 or s.y>H:
   s.a=0
 def d(s):
  if s.a:
   c=RD if s.e else YL
   for i in range(4):
    casioplot.set_pixel(s.x,s.y+i,c)
    casioplot.set_pixel(s.x+1,s.y+i,c)
    casioplot.set_pixel(s.x+2,s.y+i,c)

class A:
 def __init__(s,x,y,r):
  s.x,s.y,s.r,s.a=x,y,r,1
 def d(s):
  if s.a:
   c=CY if s.r<2 else (BL if s.r<3 else WH)
   casioplot.set_pixel(s.x+2,s.y,c)
   casioplot.set_pixel(s.x+7,s.y,c)
   for i in range(3,7):
    casioplot.set_pixel(s.x+i,s.y+1,c)
    casioplot.set_pixel(s.x+i,s.y+2,c)
   casioplot.set_pixel(s.x+3,s.y+3,BK)
   casioplot.set_pixel(s.x+6,s.y+3,BK)
   for i in range(2,8):
    casioplot.set_pixel(s.x+i,s.y+4,c)
    casioplot.set_pixel(s.x+i,s.y+5,c)
   casioplot.set_pixel(s.x+1,s.y+6,c)
   casioplot.set_pixel(s.x+2,s.y+6,c)
   casioplot.set_pixel(s.x+7,s.y+6,c)
   casioplot.set_pixel(s.x+8,s.y+6,c)

class G:
 def __init__(s):
  s.p=P()
  s.b,s.eb,s.al=[],[],[]
  s.di,s.c,s.sc,s.go,s.w=1,0,0,0,0
  s.sd,s.es=0,0
  for r in range(4):
   for o in range(8):
    s.al.append(A(45+o*18,15+r*14,r))
 def u(s):
  if s.go or s.w:
   return
  for bu in s.b:
   bu.u()
  s.b=[x for x in s.b if x.a]
  for bu in s.eb:
   bu.u()
  s.eb=[x for x in s.eb if x.a]
  s.c+=1
  if s.c>=7:
   s.c,de=0,0
   for al in s.al:
    if al.a:
     al.x+=s.di*3
     if al.x<=10 or al.x>=W-20:
      de=1
   if de:
    s.di*=-1
    for al in s.al:
     if al.a:
      al.y+=10
      if al.y>=H-35:
       s.go=1
  s.es+=1
  if s.es>25 and len(s.eb)<4:
   av=[x for x in s.al if x.a]
   if av:
    sh=random.choice(av)
    s.eb.append(B(sh.x+5,sh.y+7,1))
    s.es=0
  for bu in s.b:
   if bu.a:
    for al in s.al:
     if al.a:
      if bu.x>=al.x and bu.x<=al.x+10:
       if bu.y>=al.y and bu.y<=al.y+7:
        al.a,bu.a=0,0
        s.sc+=(4-al.r)*10
        break
  for bu in s.eb:
   if bu.a and s.p.a:
    if bu.x>=s.p.x and bu.x<=s.p.x+16:
     if bu.y>=s.p.y and bu.y<=s.p.y+10:
      s.p.lv-=1
      bu.a=0
      if s.p.lv<=0:
       s.p.a,s.go=0,1
  if all(not x.a for x in s.al):
   s.w=1
  if s.sd>0:
   s.sd-=1
 def sh(s):
  if len(s.b)<3 and s.sd==0:
   s.b.append(B(s.p.x+7,s.p.y-5,0))
   s.sd=8
 def d(s):
  casioplot.clear_screen()
  s.p.d()
  for al in s.al:
   al.d()
  for bu in s.b:
   bu.d()
  for bu in s.eb:
   bu.d()
  casioplot.draw_string(5,5,"Score:"+str(s.sc),BK,"small")
  lives="Lives:" if s.p.a else "DEAD"
  casioplot.draw_string(W-55,5,lives,BK,"small")
  casioplot.show_screen()

g=G()
g.d()
lk,t=None,0
while not g.go and not g.w:
 t+=1
 k=str(casioplot.getkey())
 if k=="23":
  g.p.m(-4)
 elif k=="25":
  g.p.m(4)
 elif k=="95" and k!=lk:
  g.sh()
 lk=k
 g.u()
 if t%2==0:
  g.d()
casioplot.clear_screen()
ms="YOU WIN!" if g.w else "GAME OVER"
co=GR if g.w else RD
casioplot.draw_string(W//2-50,H//2-15,ms,co,"large")
casioplot.draw_string(W//2-40,H//2+10,"Score:"+str(g.sc),BK,"medium")
casioplot.show_screen()