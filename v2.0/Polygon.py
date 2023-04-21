import math
from random import randint
import numpy as np
import pgboard
import pygame as pg
import Creature


session = randint(0, 1000000)
timer = 0
sound_length = 3
index_bit_size = 3
freq_types = 3
pace_bits = 8
move_bits = 3
INF = 10**9
SIZE = 700

rabbit_col = 2
food = 1
border = 15

def f(x):
    return 1 / (1 + 1.5**(-x))

class Polygon:
    translate = [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0), "bite"]
    def __init__(self, height=100, width=100):
        self.timer = 0
        self.index_bit_size = 3
        self.sounds = []
        self.height = height
        self.width = width
        self.pos_dict = dict()
        self.creatures = []
        self.foods = []
        pg.init()
        self.screen = pg.display.set_mode((SIZE + 5, SIZE))
        self.board = pgboard.Board((height, width), self.screen) #land layer
        self.world = [[0 for i in range(width)] for j in range(height)] #object layer

    def col(self, y, x):
        if x < 0 or y < 0 or y >= self.height or x >= self.width:
            return (0, 0, 0)
        if self.world[y][x] != 0:
            return self.world[y][x].color
        return pgboard.f1(self.board.world[y, x, 0], self.board.world[y, x, 1])
    def coord(self, y, x):
        if x < 0 or y < 0 or y >= self.height or x >= self.width:
            return -1
        if self.world[y][x] != 0:
            return self.world[y][x]
        else:
            return 0
    def coord_h(self, y, x):
        return self.board.world[y, x, 0]
    def coord_b(self, y, x):
        return self.board.world[y, x, 1]
    
    def position_transcript(self, coord, r):
        vector = []
        for i in range(coord[0] - r, coord[0] + r + 1):
            for j in range(coord[1] - r, coord[1] + r + 1):
                col = self.col(i, j)
                vector.append(col[0]) 
                vector.append(col[1]) 
                vector.append(col[2]) 
        return vector
    def simple_transcript(self, coord, rad):
        u = [0, 0, 0]
        d = [0, 0, 0]
        r = [0, 0, 0]
        l = [0, 0, 0]
        for i in range(-rad, rad + 1):
            for j in range(-rad, rad + 1):
                if i != 0 and j != 0:
                    c = self.col(coord[0] + i, coord[1] + j)
                    if (i < 0):
                        u[0] += c[0] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        u[1] += c[1] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        u[2] += c[2] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                    else:
                        d[0] += c[0] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        d[1] += c[1] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        d[2] += c[2] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5    
                    if (j > 0):
                        r[0] += c[0] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        r[1] += c[1] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        r[2] += c[2] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                    else:
                        l[0] += c[0] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        l[1] += c[1] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        l[2] += c[2] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5  
        return u + d + r + l 
    def up_transcript(self, coord, rad):
        u = [0, 0, 0]
        d = [0, 0, 0]
        r = [0, 0, 0]
        l = [0, 0, 0]
        for i in range(-rad, rad + 1):
            for j in range(-rad, rad + 1):
                if i != 0 and j != 0:
                    c = self.col(coord[0] + i, coord[1] + j)
                    if self.coord(coord[0] + i, coord[1] + j) == 0:
                        c = [0, 0, 0]
                    if (i < 0):
                        u[0] += 5*c[0] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        u[1] += 5*c[1] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        u[2] += 5*c[2] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                    else:
                        d[0] += 5*c[0] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        d[1] += 5*c[1] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        d[2] += 5*c[2] * abs(i) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5    
                    if (j > 0):
                        r[0] += 5*c[0] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        r[1] += 5*c[1] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        r[2] += 5*c[2] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                    else:
                        l[0] += 5*c[0] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        l[1] += 5*c[1] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5 
                        l[2] += 5*c[2] * abs(j) / (abs(i) + abs(j)) / (i ** 2 + j ** 2) ** 0.5  
        return u + d + r + l     
    def pace_transcript(self, n):
        pace_vector = []
        for i in range(n):
            pace_vector.append(2000 * int(self.timer / (2 ** i) % 2 >= 1))      
        return pace_vector

    def update(self):
        self.timer += 1
        i = 0
        while i < len(self.creatures):
            if self.creatures[i].alive == False:
                self.creatures.pop(i)
            else:
                i += 1
        for event in pg.event.get():
                self.board.event(event)    
        
    def count(self, num):
        c = 0
        for i in self.world:
            for j in i:
                if j == num:
                    c += 1
        return c
    
    def move(self, cr, act):
        self.world[cr.coord[0]][cr.coord[1]] = 0
        if act < 4:
            x = cr.coord[0] + self.translate[act][0]
            y = cr.coord[1] + self.translate[act][1]
            if -1 < x < self.height and -1 < y < self.width and self.world[x][y] == 0 and self.coord_h(x, y) != 0:
                cr.coord[0] = x
                cr.coord[1] = y
            elif self.coord(x, y) == -1 or self.coord_h(x, y) == 0:
                cr.health -= 100
                cr.brain.learn(-11)

            
                 

        elif act == 4:
            for i in [(0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
                if isinstance(self.coord(cr.coord[0] + i[0],cr.coord[1] + i[1]), Creature.Creature) and cr.clas == "meat":
                    self.world[cr.coord[0] + i[0]][cr.coord[1] + i[1]].health -= 10
                    self.world[cr.coord[0] + i[0]][cr.coord[1] + i[1]].learn(-10)
                    cr.eaten += 1
                    cr.health += 10
                    cr.learn(10)
                if isinstance(self.coord(cr.coord[0] + i[0], cr.coord[1] + i[1]), Food) and cr.clas == "grass":
                    cr.eaten += 1
                    cr.health += 7
                    cr.learn(7)   
                    self.coord(cr.coord[0] + i[0],cr.coord[1] + i[1]).die()
                    self.world[cr.coord[0] + i[0]][cr.coord[1] + i[1]] = 0
        self.pos_dict[cr.coord[0] + (cr.coord[1]) * 10**5] = cr
        self.world[cr.coord[0]][cr.coord[1]] = cr
    def print(self):
        print("Polygon")
        for i in self.world:
            print(*i)
        print("end")
    def draw(self):
        if (len(self.creatures) > 10 or self.timer % 5 == 0):
            self.board.draw()
            for i in self.foods:
                if i.alive:
                    self.board.drawpoint(i.coord[0], i.coord[1], i.color)   
                else:
                    self.board.drawpoint(i.coord[0], i.coord[1], (255, 255, 0), 4)         
            for i in self.creatures:
                self.board.drawpoint(i.coord[0], i.coord[1], i.color)
                if i.act == 4:
                    self.board.drawpoint(i.coord[0], i.coord[1], (0, 0, 0), 2)            
    
            pg.display.update()
        
class Food:
    color = (0, 255, 255)
    def __init__(self, pol):
        self.polygon = pol
        self.polygon.foods.append(self)
        self.alive = False
    def update(self):
        if self.alive:
            self.polygon.world[self.coord[0]][self.coord[1]] = 0
        self.coord = [0, 0]
        y = randint(0, self.polygon.height - 1)
        x = randint(0, self.polygon.width - 1)
        while self.polygon.coord(y, x) != 0 or self.polygon.coord_h(y, x) == 0 or not self.born_loc(y, x):
            y = randint(0, self.polygon.height)
            x = randint(0, self.polygon.width)
        self.coord[0] = y
        self.coord[1] = x
        self.polygon.world[y][x] = self
        self.alive = True
    def die(self):
        self.alive = False
        self.polygon.world[self.coord[0]][self.coord[1]] = 0
    def born_loc(self, y, x):
        return self.polygon.coord_b(y, x) == 2 and self.polygon.coord_h(y, x) > 100