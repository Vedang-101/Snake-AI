import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
from neuralNetwork import NeuralNetwork

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
    def __init__(self, color, pos, nn):
        self.color = color
        self.head = cube(pos, self.color)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

        self.score = 0
        self.fitness = 0
        self.energy = self.body[0].rows * self.body[0].rows

        if nn!= None:
            self.brain = nn.copy()
        else:
            self.brain = NeuralNetwork([8,15,9,4])

    def keys_record(self, index):
        global snack, width

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        
        #inputs = wall to left, wall infront, wall right, angle to food, tail on left, tail on right, tail front, energy left
        inp = []
        dx = self.dirnx
        dy = self.dirny

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

        #angle to the food
        x1 = snack[index].pos[0] - self.body[0].pos[0]
        y1 = self.body[0].pos[1] - snack[index].pos[1]
        
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

        #tail on left
        if dx == 1 and (self.body[0].pos[1] - 1) == self.body[-1].pos[1]:
            inp.append(1)
        elif dx == -1 and (self.body[0].pos[1] + 1) == self.body[-1].pos[1]:
            inp.append(1)
        elif dy == 1 and (self.body[0].pos[0] + 1) == self.body[-1].pos[0]:
            inp.append(1)
        elif dy == -1 and (self.body[0].pos[0] - 1) == self.body[-1].pos[0]:
            inp.append(1)
        else:
            inp.append(0)

        #tail infront
        if dx == 1 and (self.body[0].pos[0] + 1) == self.body[-1].pos[0]:
            inp.append(1)
        elif dx == -1 and (self.body[0].pos[0] - 1) == self.body[-1].pos[0]:
            inp.append(1)
        elif dy == 1 and (self.body[0].pos[1] + 1) == self.body[-1].pos[1]:
            inp.append(1)
        elif dy == -1 and (self.body[0].pos[1] - 1) == self.body[-1].pos[1]:
            inp.append(1)
        else:
            inp.append(0)

        #tail to right
        if dx == 1 and (self.body[0].pos[1] + 1) == self.body[-1].pos[1]:
            inp.append(1)
        elif dx == -1 and (self.body[0].pos[1] - 1) == self.body[-1].pos[1]:
            inp.append(1)
        elif dy == 1 and (self.body[0].pos[0] - 1) == self.body[-1].pos[0]:
            inp.append(1)
        elif dy == -1 and (self.body[0].pos[0] + 1) == self.body[-1].pos[0]:
            inp.append(1)
        else:
            inp.append(0)

        inp.append(self.energy/(self.body[0].rows * self.body[0].rows))

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
            #self.score -= 10
            return True
        elif self.body[0].dirnx == 1 and self.body[0].pos[0] >= self.body[0].rows:
            #self.score -= 10
            return True
        elif self.body[0].dirny == -1 and self.body[0].pos[1] <=-1:
            #self.score -= 10
            return True
        elif self.body[0].dirny == 1 and self.body[0].pos[1] >= self.body[0].rows:
            #self.score -= 10
            return True
        for x in range(len(self.body)):
            if self.body[x].pos in list(map(lambda z:z.pos, self.body[x+1:])):
                #self.score -= 10
                return True
        if self.energy <= 0:
            return True
        return False

    def mutate(self):
        self.brain.mutate(0.1)

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
    for i in range(len(s)):
        s[i].draw(surface)
        snack[i].draw(surface)
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
    global width, rows, s, snack, population, generation, saved_snakes
    width = 500
    rows = 10
    generation = 1

    population = 1
    
    #win = pygame.display.set_mode((width,width))
    s = []
    snack = []
    for i in range(population):
        s.append(snake((255,255,255),(int(rows/2),int(rows/2)),None))
        snack.append(cube(randomSnack(rows, s[i]), (150,0,0)))
    print('Snakes Added')

    flag = True

    #clock = pygame.time.Clock()

    saved_snakes = []
    import time
    time1 = time.time()
    while flag:
        loop = 0
        while loop<len(s):
            print('here')
            s[loop].keys_record(loop)
            s[loop].move()
            s[loop].score += 0.01
            s[loop].energy -= 1
            if s[loop].body[0].pos == snack[loop].pos:
                s[loop].score += 100
                s[loop].energy = s[loop].body[0].rows * s[loop].body[0].rows
                s[loop].addCube()
                snack[loop] = cube(randomSnack(rows, s[loop]), (150,0,0))

            if s[loop].dead():
                print('dead')
                saved_snakes.append(s[loop])
                s.pop(loop)
                snack.pop(loop)
                loop -= 1
            loop += 1

        if (len(s) == 0):
            print('Time taken by generation: ', (time.time() - time1))
            time1 = time.time()
            print('New Generation creating...')
            generation += 1
            nextGeneration()
            
        #redrawWindow(win)
        input("redraw next?: length of s: "+str(len(s)))

def nextGeneration():
    global s, population, saved_snakes, generation, snack
    calculateFitness()

    print('adding new Snakes')
    for i in range(population):
        s.append(pickOne())
        snack.append(cube(randomSnack(rows, s[i]), (150,0,0)))
    pickOne().brain.save('savedBrain')
    print('Best Score of previous generation: ', len(pickOne().body))
    print("New Generation: ", generation)
    # if generation%10 == 0:
    #     c = input("Paused, press anything to continue")
    saved_snakes = []
    
def pickOne():
    global saved_snakes, rows
    
    index = 0

    #r = random.randrange(0,1)
    # while r>0:
    #     r = r - saved_snakes[index].fitness
    #     index += 1
    # index -= 1

    big = 1
    for i in range(len(saved_snakes)):
        if big < len(saved_snakes[i].body):
            big = len(saved_snakes[i].body)
            index = i

    parent = saved_snakes[index]
    parent.reset((int(rows/2),int(rows/2)))
    parent.mutate()
    return parent

    #child = snake(())

def calculateFitness():
    global population, saved_snakes
    score = 0
    for i in range(population):
        score += saved_snakes[i].score

    for i in range(population):
        saved_snakes[i].fitness = saved_snakes[i].score/score

main()