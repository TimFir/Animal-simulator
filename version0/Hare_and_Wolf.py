#import pygame
import sys
import math
from random import randint

def f(x):
    if x > 23:
        return 1
    elif x < -23:
        return 0
    else:
        return 1 / (1 + math.e**(-x))

#pygame.init()

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

r = 5
timer = 0
sound_length = 3
index_bit_size = 4
freq_types = 10
pace_bits = 8
INF = 10**9

rabbit_col = 2
food = 1
border = 15

class Polygon:

    def __init__(self, height=100, width=100):
        self.sounds = set()
        self.height = height
        self.width = width
        self.world = [[None for i in range(width)] for j in range(height)]

    def coord(a, b):
        if a < 0 or b < 0 or a >= self.length or b >= self.width:
            return -1
        return self.world[a][b]

    def build(self, obj, a):
        if self.world[a[0]][a[1]] == 0:
            self.world[a[0]][a[1]] = obj

    def sound(self, a, freq):
        self.sounds.add((a, freq, timer))

    def sounds_update(self):
        sounds = set()
        for i in self.sounds:
            if timer - sound_length <= i[2]:
                sounds.add(i)
        self.sounds = sounds

    def transcript(self, coord):
        vector = []
        for i in range(coord[0] - r, coord[0] + r + 1):
            for j in range(coord[1] - r, coord[1] + r + 1):
                if (self.width > j and self.height > i and i >= 0 and j >= 0):
                    for k in range(index_bit_size):
                        vector.append(self.world[i][j] // (2 ** i) % 2)
                else:
                    for k in range(index_bit_size):
                        vector.append(border // (2 ** i) % 2)                    

        vector_sounds = [0] * sound_length
        for i in self.sounds:
            if timer - sound_length <= i[2]:
                vector_sounds[i[2]] += 1 / math.hypot(coord[0] - i[0][0], coord[1] - i[0][1])
        for i in range(sound_length):
            vector_sounds[i] = f(vector_sounds[i])

        pace_vector = []
        for i in range(pace_bits):
            pace_vector.append(int(timer / (2 ** i) % 2 >= 1))

        return (vector + vector_sounds + pace_vector) # подаётся на вход нейросети

    def update(self):
        timer += 1
        sounds.update()
        
    def count(self, num):
        c = 0
        for i in self.world:
            for j in i:
                if j == num:
                    c += 1
        return c
        
    def print(self):
        print("Polygon")
        for i in self.world:
            print(*i)
        print("end")

class Creature:

    def __init__(self, polygon, brain=None, sp=0, outp_size=5):
        self.coord = [0, 0]
        self.alive = True
        self.polygon = polygon
        self.eaten = 0
        self.inp_size = len(self.polygon.transcript([0, 0]))
        self.outp_size = outp_size
        if brain == None:
            self.brain = [[randint(0, 10) / 10 for i in range(self.outp_size)] for j in range(self.inp_size)]
        else:
            self.brain = [[0 for i in range(self.outp_size)] for j in range(self.inp_size)]
            for i in range(self.inp_size):
                for j in range(self.outp_size):
                    self.brain[i][j] = brain[i][j] + brain[i][j] * (randint(-100, 100) // 100) * sp
                    
    def act(self, num):
        pass
    
    def get(self):
        self.inp = self.polygon.transcript(self.coord)
                    
    def action(self):
        self.outp = [0 for i in range(self.outp_size)]
        for i in range(self.inp_size):
            for j in range(self.outp_size):
                self.outp[j] += self.inp[i] * self.brain[i][j]
        translate = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for i in range(len(translate)):
            if self.coord[0] + translate[i][0] < 0 or self.coord[0] + translate[i][0] >= self.polygon.height or self.coord[1] + translate[i][1] < 0 or self.coord[1] + translate[i][1] >= self.polygon.width or self.polygon.world[self.coord[0] + translate[i][0]][self.coord[1] + translate[i][1]] >= self.color:
                self.outp[i] = -INF
        act_num = self.outp.index(max(self.outp))
        self.act(act_num)
        
    def update(self):
        self.eaten = 0
        self.alive = True
        x1 = randint(0, self.polygon.height - 1)
        y1 = randint(0, self.polygon.width - 1)        
        while self.polygon.world[x1][y1] != 0:
            x1 = randint(0, self.polygon.height - 1)
            y1 = randint(0, self.polygon.width - 1)
        self.coord = [x1, y1]
        self.polygon.world[x1][y1] = self.color
        
class Rabbit(Creature):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]
    color = rabbit_col
    def act(self, num):
        self.polygon.world[self.coord[0]][self.coord[1]] = 0
        self.coord[0] += self.actions[num][0]
        self.coord[1] += self.actions[num][1]
        if self.polygon.world[self.coord[0]][self.coord[1]] == food:
            self.eaten += 1
        self.polygon.world[self.coord[0]][self.coord[1]] = self.color
    def die(self):
        if self.polygon.world[self.coord[0]][self.coord[1]] == 4:
            self.alive = False
        
class Wolf(Creature):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]
    color = 4
    def act(self, num):
        self.polygon.world[self.coord[0]][self.coord[1]] = 0
        self.coord[0] += self.actions[num][0]
        self.coord[1] += self.actions[num][1]
        if self.polygon.world[self.coord[0]][self.coord[1]] == rabbit_col:
            self.eaten += 1
        self.polygon.world[self.coord[0]][self.coord[1]] = self.color    
        
        
        
pol = Polygon(100, 100)
for i in range(pol.height):
    for j in range(pol.width):
        pol.world[i][j] = (randint(1, 2) // 2)
        
generations = 500
rab_top_size = 6
rab_mult = 4
wolf_top_size = 3
wolf_mult = 3
rabbits = [Rabbit(pol) for i in range(rab_top_size)]
wolfs = [Wolf(pol) for i in range(wolf_top_size)]
speed = 0.3
wresults = []
rresults = []
    
for c in range(generations):
    for i in range(pol.height):
        for j in range(pol.width):
            pol.world[i][j] = (randint(1, 2) // 2)   
            
    for i in range(rab_top_size):
        for j in range(rab_mult - 1):
            rabbits.append(Rabbit(pol, rabbits[i].brain, speed))
    for i in range(wolf_top_size):
        for j in range(wolf_mult - 1):
            wolfs.append(Wolf(pol, wolfs[i].brain, speed)) 
            
    for i in rabbits:
        i.update()
    for i in wolfs:
        i.update()
    #pol.print()
    print(c, pol.count(1), pol.count(2), pol.count(4))
    for t in range(100):
        for i in wolfs:
            i.get()
            i.action()
        for i in rabbits:
            i.die()
            if i.alive:
                i.get()
                i.action()
        #pol.print()
    rabbits.sort(key=lambda x: (-x.alive, -x.eaten))
    wolfs.sort(key=lambda x: (-x.alive, -x.eaten))
    print(c, rabbits[0].eaten, wolfs[0].eaten)
    print(c, pol.count(1), pol.count(2), pol.count(4))
    rresults.append(rabbits[0].eaten)
    wresults.append(wolfs[0].eaten)
    #pol.print()
    while len(rabbits) > rab_top_size:
        rabbits.pop()
    while len(wolfs) > wolf_top_size:
        wolfs.pop()    
    if (c > 100):
        print(c, "avg", sum(rresults[-100:]) / 100, sum(wresults[-100:]) / 100)
print(rabbits[0].brain)
print(wolfs[0].brain)
while True:
    pass
