import pygame
import random
import numpy as np
import os


tileLenght = 35
rows = 10
columns = 10

height = columns * tileLenght
width = rows * tileLenght

global reward, explore, Q
Q = np.zeros((128, 4))

explore = 0.1
discount = 0
learning = 1
reward = 0


def clear():
    _ = os.system('cls')

class heada():
    def __init__(self, tempx, tempy):
        self.x = tempx
        self.y = tempy

class bodyPart():
    def __init__(self,x,y,direction,color = (0,255,0)):
        self.color = color
        self.x = x
        self.y = y
        self.direction = direction

class snake():
    body = []

    def __init__(self, x, y,target , color = (0,255,0)):
        self.color = color
        self.x = tileLenght * x
        self.y = tileLenght * y
        self.direction = 0
        self.body.append(self)
        self.target = target
        self.dead = False
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.targetDirection = None
        self.headState = 0
        self.moves = 500


    def move(self):
        global score, reward, Q, wait
        if self.dead:
            return
        self.lookAround()
        self.lookForTarget()
        currentState = self.calculateState()
        distanceFromTarget = abs(self.body[0].x - self.target.x) + abs(self.body[0].y - self.target.y)
        bestAction = Q[int(currentState)].argmax()
        if random.random() < explore:
            bestAction = random.randint(0, 3)

        if wait:
            input()
        if bestAction == 0 and self.direction != 1:
            self.direction = 0
        elif bestAction == 1 and self.direction != 0:
            self.direction = 1
        elif bestAction == 2 and self.direction != 3:
            self.direction = 2
        elif bestAction == 3 and self.direction != 2:
            self.direction = 3
        """
        pressed = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.direction != 0 and pressed is False:
            self.direction = 1
            pressed = True
        elif keys[pygame.K_RIGHT] and self.direction != 1 and pressed is False:
            self.direction = 0
            pressed = True
        elif keys[pygame.K_UP] and self.direction != 3 and pressed is False:
            self.direction = 2
            pressed = True
        elif keys[pygame.K_DOWN] and self.direction != 2 and pressed is False:
            self.direction = 3
            pressed = True
        """
        if self.direction == 0: #right
            self.x += tileLenght
        elif self.direction == 1: #left
            self.x -= tileLenght
        elif self.direction == 2: #up
            self.y -= tileLenght
        elif self.direction == 3: #down
            self.y += tileLenght
        else:
            pass

        for i in range(len(self.body)):
            if i != 0:
                if self.body[0].x == self.body[i].x and self.body[0].y == self.body[i].y:
                    reward = -30
                    Q[int(currentState), int(bestAction)] += reward
                    reward = 0
                    self.dead = True
                    return

        for i in range(len(self.body)):
            if i != 0:
                self.body[-i].x = self.body[-i - 1].x
                self.body[-i].y = self.body[-i - 1].y
                self.body[-1].direction = self.body[-i - 1].direction


        self.moves -= 1
        print(self.moves)
        distanceFromTargetAfterMove = abs(self.body[0].x - self.target.x) + abs(self.body[0].y - self.target.y)
        if distanceFromTargetAfterMove < distanceFromTarget:
            reward = 4
        else:
            reward = -2


        if self.moves == 0:
            reward = -30
            Q[int(currentState), int(bestAction)] += reward
            reward = 0
            self.dead = True
            return

        if self.body[0].x < 0 or self.body[0].y < 0 or self.body[0].x > (rows-1) * tileLenght or self.body[0].y > (columns-1)* tileLenght:
            reward = -30
            Q[int(currentState), int(bestAction)] += reward
            reward = 0
            self.dead = True
            return

        self.lookAround()
        self.lookForTarget()
        currentState1 = self.calculateState()
        Q[int(currentState), int(bestAction)] = (1-learning) * Q[int(currentState), int(bestAction)] + learning * (reward + discount * Q[int(currentState1)].max())
        reward = 0

    def simulateNextState(self):
        tepx = 0
        tepy = 0
        crState = self.calculateState()
        bestAction = Q[int(crState)].argmax()

        if bestAction == 0:
            tepx = self.x + tileLenght
        elif bestAction == 1:
            tepx = self.x - tileLenght
        elif bestAction == 2:
            tepy = self.y - tileLenght
        elif bestAction == 3:
            tepy = self.y + tileLenght

        self.lookAround(True, tepx, tepy)
        self.lookForTarget(True, tepx, tepy)
        crState = self.calculateState()
        return crState

    def lookAround(self, simulate=False, tempx=0, tempy=0):
        if not simulate:
            head = self.body[0]
        else:
            head = heada(tempx,tempy)
        for i in range(len(self.body)):
            if head.x - tileLenght == self.body[i].x and head.y == self.body[i].y:
                self.left = 1
            else:
                self.left = 0
            if head.x + tileLenght == self.body[i].x and head.y == self.body[i].y:
                self.right = 1
            else:
                self.right = 0
            if head.y + tileLenght == self.body[i].y and head.x == self.body[i].x:
                self.down = 1
            else:
                self.down = 0
            if head.y - tileLenght == self.body[i].y and head.x == self.body[i].x:
                self.up = 1
            else:
                self.up = 0
        if head.x == 0:
            self.left = 1
        if head.y == 0:
            self.up = 1
        if head.x == (rows-1)*tileLenght:
            self.right = 1
        if head.y == (columns-1)*tileLenght:
            self.down = 1

        if self.up == 1:
            if self.right == 1:
                if self.down == 1:
                    if self.left == 1:
                        self.headState = 15
                    else:
                        self.headState = 12
                elif self.left == 1:
                    self.headState = 11
                else:
                    self.headState = 5
            elif self.down == 1:
                if self.left == 1:
                    self.headState = 13
                else:
                    self.headState = 6
            elif self.left == 1:
                self.headState = 7
            else:
                self.headState = 1
        elif self.right == 1:
            if self.down == 1:
                if self.left == 1:
                    self.headState = 14
                else:
                    self.headState = 8
            elif self.left == 1:
                self.headState = 9
            else:
                self.headState = 2
        elif self.down == 1:
            if self.left == 1:
                self.headState = 10
            else:
                self.headState = 3
        elif self.left == 1:
            self.headState = 4
        else:
            self.headState = 0

    def lookForTarget(self, simulate=False, tempx=0, tempy=0):
        if not simulate:
            head = self.body[0]
        else:
            head = heada(tempx, tempy)
        if head.x > self.target.x and head.y > self.target.y:
            self.targetDirection = 0
        elif head.x == self.target.x and head.y > self.target.y:
            self.targetDirection = 1
        elif head.x < self.target.x and head.y > self.target.y:
            self.targetDirection = 2
        elif head.x > self.target.x and head.y == self.target.y:
            self.targetDirection = 3
        elif head.x < self.target.x and head.y == self.target.y:
            self.targetDirection = 4
        elif head.x > self.target.x and head.y < self.target.y:
            self.targetDirection = 5
        elif head.x == self.target.x and head.y < self.target.y:
            self.targetDirection = 6
        elif head.x < self.target.x and head.y < self.target.y:
            self.targetDirection = 7

    def calculateState(self):
        state = self.targetDirection * 16 + self.headState
        return state

    def addBody(self):
        tail = self.body[-1]
        if tail.direction == 0: #right
            self.body.append(bodyPart(tail.x - tileLenght, tail.y, tail.direction))
        elif tail.direction == 1: #left
            self.body.append(bodyPart(tail.x + tileLenght, tail.y, tail.direction))
        elif tail.direction == 2: #up
            self.body.append(bodyPart(tail.x, tail.y + tileLenght, tail.direction))
        else: #down
            self.body.append(bodyPart(tail.x, tail.y - tileLenght, tail.direction))

    def draw(self, window):
        for i in range(len(self.body)):
            pygame.draw.rect(window, self.body[i].color, (self.body[i].x + 1, self.body[i].y + 1, tileLenght - 1, tileLenght -1))

    def reset(self, x, y):
        for i in range(len(self.body) - 1):
            self.body.pop(-1)
        self.direction = 0
        self.x = tileLenght * x
        self.y = tileLenght * y
        self.dead = False

class food():
    def __init__(self, x, y, color = (255,0,0)):
        self.color = color
        self.x = tileLenght * x
        self.y = tileLenght * y

    def consume(self):
        if c.x == self.x and c.y == self.y:
            global target, score, reward
            randomSpot = self.getSpot()
            target = food(randomSpot[0],randomSpot[1])
            score += 1
            reward = 100
            c.addBody()
            c.target = target
            c.moves = 500
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x + 1, self.y + 1, tileLenght - 1, tileLenght - 1))

    def reset(self, x, y):
        self.x = tileLenght*x
        self.y = tileLenght*y

    def getSpot(self):
        randomSpot = [random.randint(0, rows - 1), random.randint(0, columns - 1)]
        return randomSpot


def redrawWindow(win):
    win.fill((0, 0, 0))
    target.draw(win)
    drawGrid(width,height,win)
    c.draw(win)
    pygame.display.update()

def drawGrid(w,h,surface):
    x = 0
    y = 0
    for i in range(rows):
        x = x + tileLenght
        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, h))
    for l in range(columns):
        y = y + tileLenght
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))

def restart(c, target):
    global score, explore
    score = 0
    c.reset(2, 5)
    target.reset(3,4)
    explore -= 0.0001
    c.moves = 500


def main():
    global win, c, target, score, wait
    delay = 60
    tick = 60
    score = 0
    wait = False
    flag = True
    target = food(8, 8)
    c = snake(2,5, target)
    win = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    while flag:
        pygame.time.delay(delay)
        clock.tick(tick)
        c.move()
        target.consume()
        redrawWindow(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            delay = 60
            tick = 60
        if keys[pygame.K_y]:
            delay = 0
            tick = 10000
        if keys[pygame.K_r]:
            wait = True
        if c.dead:
            restart(c, target)

main()