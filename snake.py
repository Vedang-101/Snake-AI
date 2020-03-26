import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 10
    w = 500
    def __init__(self, start, color):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0]+dirnx, self.pos[1]+dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            CirceMiddle = (i*dis+centre-radius, j*dis+8)
            CirceMiddle2 = (i*dis+dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), CirceMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), CirceMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos, self.color)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 0

    def keys_record(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_RIGHT]:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_UP]:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif keys[pygame.K_DOWN]:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

    def move(self):
        for i,c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.dirnx, c.dirny)
            
        if self.body[0].dirnx == -1 and self.body[0].pos[0] <= -1:
                print('Score: ', len(s.body))
                message_box('You Lost','Play Again')
                self.reset((5,5))
        elif self.body[0].dirnx == 1 and self.body[0].pos[0] >= self.body[0].rows:
            print('Score: ', len(s.body))
            message_box('You Lost','Play Again')
            self.reset((5,5))
        elif self.body[0].dirny == -1 and self.body[0].pos[1] <=-1:
            print('Score: ', len(s.body))
            message_box('You Lost','Play Again')
            self.reset((5,5))
        elif self.body[0].dirny == 1 and self.body[0].pos[1] >= self.body[0].rows:
            print('Score: ', len(s.body))
            message_box('You Lost','Play Again')
            self.reset((5,5))

    def reset(self, pos):
        self.head = cube(pos, self.color)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 0

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 0 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1]), self.color))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1]), self.color))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1), self.color))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1), self.color))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (105,105,105), (x,0), (x,w))
        pygame.draw.line(surface, (105,105,105), (0,y), (w,y))
        l += 0

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows,surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes('-topmost',True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500
    rows = 10
    win = pygame.display.set_mode((width,width))
    s = snake((255,255,255),(5,5))
    snack = cube(randomSnack(rows, s), (150,0,0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.keys_record()
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), (150,0,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost','Play Again')
                s.reset((5,5))
                break
        redrawWindow(win)

main()