import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from  neuralNetwork import NeuralNetwork

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
    def __init__(self, color, pos, savePath):
        self.color = color
        self.head = cube(pos, self.color)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.energy = self.body[0].rows * self.body[0].rows
        import pickle
        savedbrain = open(savePath, 'rb')
        self.brain = pickle.load(savedbrain)
        savedbrain.close()
        #self.brain = NeuralNetwork([24,18,18,4])

    def keys_record(self):
        #input('keys_record')
        global snack

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #inputs = dirX, dirY, wall to left, wall infront, wall to right, body to left, body infront, body to right, angle from food, energy
        inp = []
        dx = self.dirnx
        dy = self.dirny

        inp.append(dx)
        inp.append(dy)


        #wall to left
        if dx == 1 and (self.body[0].pos[1] - 1) == -1:
            inp.append(1)
        elif dx == -1 and (self.body[0].pos[1] + 1) == self.body[0].rows:
            inp.append(1)
        elif dy == 1 and (self.body[0].pos[0] + 1) == self.body[0].rows:
            inp.append(1)
        elif dy == -1 and (self.body[0].pos[0] - 1) == -1:
            inp.append(1)
        else:
            inp.append(0)

        #wall infront
        if dx == 1 and (self.body[0].pos[0] + 1) == self.body[0].rows:
            inp.append(1)
        elif dx == -1 and (self.body[0].pos[0] - 1) == -1:
            inp.append(1)
        elif dy == 1 and (self.body[0].pos[1] + 1) == self.body[0].rows:
            inp.append(1)
        elif dy == -1 and (self.body[0].pos[1] - 1) == -1:
            inp.append(1)
        else:
            inp.append(0)

        #wall to right
        if dx == 1 and (self.body[0].pos[1] + 1) == self.body[0].rows:
            inp.append(1)
        elif dx == -1 and (self.body[0].pos[1] - 1) == -1:
            inp.append(1)
        elif dy == 1 and (self.body[0].pos[0] - 1) == -1:
            inp.append(1)
        elif dy == -1 and (self.body[0].pos[0] + 1) == self.body[0].rows:
            inp.append(1)
        else:
            inp.append(0)

        posRight = (self.body[0].pos[0]+1,self.body[0].pos[1])
        posLeft = (self.body[0].pos[0]-1,self.body[0].pos[1])
        posUp = (self.body[0].pos[0],self.body[0].pos[1]-1)
        posDown = (self.body[0].pos[0],self.body[0].pos[1]+1)
        apended = False
        #Body On Left
        if dx == 1:
            for x in range(len(self.body)):
                if posUp in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dx == -1:
            for x in range(len(self.body)):
                if posDown in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dy == 1:
            for x in range(len(self.body)):
                if posRight in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dy == -1:
            for x in range(len(self.body)):
                if posLeft in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        if apended == False:
            inp.append(0)

        apended = False
        #Body On Front
        if dx == 1:
            for x in range(len(self.body)):
                if posRight in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dx == -1:
            for x in range(len(self.body)):
                if posLeft in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dy == 1:
            for x in range(len(self.body)):
                if posDown in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dy == -1:
            for x in range(len(self.body)):
                if posUp in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        if apended == False:
            inp.append(0)

        apended = False
        #Body On Right
        if dx == 1:
            for x in range(len(self.body)):
                if posDown in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dx == -1:
            for x in range(len(self.body)):
                if posUp in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dy == 1:
            for x in range(len(self.body)):
                if posLeft in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        elif dy == -1:
            for x in range(len(self.body)):
                if posRight in list(map(lambda z:z.pos, self.body[x+1:])):
                    apended = True
                    inp.append(1)
                    break
        if apended == False:
            inp.append(0)

        #angle to the food
        x1 = snack.pos[0] - self.body[0].pos[0]
        y1 = self.body[0].pos[1] - snack.pos[1]
        
        dot = -dy*y1 + dx * x1
        if x1+y1 != 0:
            cosAngle = dot/((x1*x1 + y1*y1) ** 0.5)
            angle = (math.acos(cosAngle) * 180)/math.pi
        else:
            angle = 0
        if (dx == 1 and y1<0) or (dx == -1 and y1>0) or (dy == 1 and x1<0) or (dy == -1 and x1<0):
            angle *= -1

        angle = angle/180
        inp.append(angle)

        print(inp)

        keys = self.brain.feedforward(inp)

        big = keys[0]
        index = 0
        for i in range(1,len(keys)):
            if(keys[i]>big):
                big = keys[i]
                index = i
        
        #Output = Left,Right,Up,Down
        if index == 0:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif index == 1:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif index == 2:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif index == 3:
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

    def dead(self):
        if self.body[0].dirnx == -1 and self.body[0].pos[0] <= -1:
                return True
        elif self.body[0].dirnx == 1 and self.body[0].pos[0] >= self.body[0].rows:
            return True
        elif self.body[0].dirny == -1 and self.body[0].pos[1] <=-1:
            return True
        elif self.body[0].dirny == 1 and self.body[0].pos[1] >= self.body[0].rows:
            return True
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z:z.pos, self.body[x+1:])):
                return True
        return False

    def reset(self, pos):
        self.head = cube(pos, self.color)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

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
        for c in range(len(self.body)):
            self.body[c].draw(surface)

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
    #drawGrid(width,rows,surface)
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
    s = snake((255,255,255),(5,5),'savedBrain.nn')
    snack = cube(randomSnack(rows, s), (150,0,0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.keys_record()
        s.move()
        s.energy -= 1
        if s.body[0].pos == snack.pos:
            s.addCube()
            s.energy = s.body[0].rows * s.body[0].rows
            snack = cube(randomSnack(rows, s), (150,0,0))

        if s.dead():
            print('Score: ', len(s.body))
            message_box('AI Lost','Try Again?')
            s.reset((5,5))
        redrawWindow(win)
        #input('draw next?')

main()