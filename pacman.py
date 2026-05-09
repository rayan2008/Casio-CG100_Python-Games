import casioplot, random

W,H=384,192
S=8
GW,GH=23,17
OX,OY=8,8

BK=(0,0,0); WH=(255,255,255)
YL=(255,255,0); BL=(0,120,255); RD=(255,60,60)

MAZE=[
"11111111111111111111111",
"10202020201102020202021",
"12111111101101111111101",
"10202020120021020202021",
"12101010101101010101101",
"10202010021120010202021",
"11111011101101110111111",
"12021202020020202001021",
"10101111101101111101001",
"12100202021020202021021",
"10101111111111111101001",
"12020202020202020202021",
"10111111101101111111101",
"12020202100000012020021",
"10111110111111110111101",
"12020202001102020202021",
"11111111111111111111111",
]

DIRS=((1,0),(-1,0),(0,1),(0,-1))

def delay(n):
    for _ in range(n):
        pass

def txy(tx,ty):
    return OX+tx*S, OY+ty*S

def fill8(tx,ty,c):
    x,y=txy(tx,ty)
    for yy in range(y,y+S):
        for xx in range(x,x+S):
            casioplot.set_pixel(xx,yy,c)

def pellet(tx,ty):
    x,y=txy(tx,ty)
    casioplot.set_pixel(x+S//2,y+S//2,WH)

def draw_tile(g,x,y):
    v=g[y][x]
    if v==1:
        fill8(x,y,BL)
    else:
        fill8(x,y,BK)
        if v==2: pellet(x,y)

def hud(sc,lv,left):
    y=OY+GH*S+6
    for yy in range(y-2,y+18):
        for xx in range(W):
            casioplot.set_pixel(xx,yy,BK)
    casioplot.draw_string(5,y,"Score:"+str(sc),WH,"small")
    casioplot.draw_string(145,y,"Lives:"+str(lv),WH,"small")
    casioplot.draw_string(275,y,"Left:"+str(left),WH,"small")

def parse():
    g=[]
    for r in MAZE:
        row=[]
        for ch in r:
            if ch=="1": row.append(1)
            elif ch=="2": row.append(2)
            else: row.append(0)
        g.append(row)
    return g

def count(g):
    n=0
    for y in range(GH):
        for x in range(GW):
            if g[y][x]==2: n+=1
    return n

def can(g,x,y):
    return g[y][x]!=1

# ===== YOUR CG100 KEY CODES =====
def key_dir(k):
    if k==25: return 1,0      # right
    if k==23: return -1,0     # left
    if k==14: return 0,-1     # up
    if k==34: return 0,1      # down
    return None

def is_exe(k): return k in (13,95)
def is_exit(k): return k==27

class Pac:
    def __init__(s,x,y):
        s.x,s.y=x,y
        s.dx,s.dy=1,0

class Ghost:
    def __init__(s,x,y,dx,dy):
        s.x,s.y=x,y
        s.dx,s.dy=dx,dy

class Game:
    def __init__(s):
        s.base=parse()
        s.menu()

    def menu(s):
        casioplot.clear_screen()
        casioplot.draw_string(60,30,"Mini Pac-Man",WH,"medium")
        casioplot.draw_string(45,60,"Arrows move EXE start",WH,"small")
        casioplot.show_screen()
        while True:
            k=casioplot.getkey()
            if k is None: continue
            if is_exit(k): s.quit=1; return
            if is_exe(k): break
        s.quit=0
        s.reset()

    def reset(s):
        s.g=[s.base[y][:] for y in range(GH)]
        s.sc=0; s.lv=3
        s.left=count(s.g)
        s.over=0; s.win=0
        s.p=Pac(1,1)
        s.gh=[Ghost(GW//2,GH//2,1,0),Ghost(GW//2+1,GH//2,-1,0)]
        s.draw_world()
        s.draw_sprite(s.p.x,s.p.y,YL)
        for q in s.gh: s.draw_sprite(q.x,q.y,RD)
        hud(s.sc,s.lv,s.left)
        casioplot.show_screen()

    def draw_world(s):
        casioplot.clear_screen()
        for y in range(GH):
            for x in range(GW):
                draw_tile(s.g,x,y)

    def redraw(s,x,y):
        draw_tile(s.g,x,y)

    def draw_sprite(s,x,y,c):
        fill8(x,y,c)

    def step_pac(s):
        nx=s.p.x+s.p.dx
        ny=s.p.y+s.p.dy
        if can(s.g,nx,ny):
            ox,oy=s.p.x,s.p.y
            s.p.x,s.p.y=nx,ny
            s.redraw(ox,oy)
            if s.g[ny][nx]==2:
                s.g[ny][nx]=0
                s.sc+=10
                s.left-=1
            s.draw_sprite(s.p.x,s.p.y,YL)

    def choose(s,q,px,py):
        opts=[]
        for dx,dy in DIRS:
            nx,ny=q.x+dx,q.y+dy
            if s.g[ny][nx]!=1:
                opts.append((dx,dy))
        if not opts: return 0,0
        rev=(-q.dx,-q.dy)
        if len(opts)>1 and rev in opts:
            opts.remove(rev)
        best=opts[0]; bd=9999
        for dx,dy in opts:
            d=abs(px-(q.x+dx))+abs(py-(q.y+dy))
            if d<bd: bd=d; best=(dx,dy)
        return best

    def step_ghosts(s):
        px,py=s.p.x,s.p.y
        for q in s.gh:
            ox,oy=q.x,q.y
            nx,ny=q.x+q.dx,q.y+q.dy
            if s.g[ny][nx]==1:
                q.dx,q.dy=s.choose(q,px,py)
                nx,ny=q.x+q.dx,q.y+q.dy
            q.x,q.y=nx,ny
            s.redraw(ox,oy)
            s.draw_sprite(q.x,q.y,RD)

    def collide(s):
        for q in s.gh:
            if q.x==s.p.x and q.y==s.p.y:
                return 1
        return 0

g=Game()

if not g.quit:
    t=0
    while not g.over:
        t+=1
        k=casioplot.getkey()
        if k is not None:
            if is_exit(k): break
            d=key_dir(k)
            if d: g.p.dx,g.p.dy=d

        g.step_pac()
        g.step_ghosts()

        if g.collide():
            g.lv-=1
            if g.lv<=0:
                g.over=1
            else:
                g.p.x,g.p.y=1,1

        if g.left<=0:
            g.over=1; g.win=1

        hud(g.sc,g.lv,g.left)
        casioplot.show_screen()

        delay(0)

casioplot.clear_screen()
msg="YOU WIN!" if g.win else "GAME OVER"
casioplot.draw_string(W//2-50,H//2,msg,YL if g.win else RD,"large")
casioplot.show_screen()
