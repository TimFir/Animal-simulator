from random import randint
from math import exp
import Brain as br
import numpy as np
INF = 10**9


class Creature:

    def __init__(self, polygon, brain=None, sp=0, outp_size=5):
        if polygon is not None:
            polygon.creatures.append(self)
        self.r = 4
        self.lifetime = 0
        self.power = 5
        self.move_bits = 2
        self.pace_bits = 6
        self.freq_types = 3
        self.last_act = 4 # изменение
        self.coord = [0, 0]
        self.alive = True
        self.polygon = polygon
        self.eaten = 0
        self.health = 50
        self.inp_size = 2*3*4 + 1 + self.pace_bits
        self.outp_size = outp_size
        if brain == None:
            self.brain = br.Brain((self.inp_size, self.outp_size))
        else:
            self.brain = br.Brain((self.inp_size, self.outp_size), brain.matrix)
                    
    def get(self):
        self.inp = []
        self.inp += self.polygon.up_transcript(self.coord, self.r)
        self.inp += self.polygon.simple_transcript(self.coord, self.r)
        self.inp += [randint(1, 255)]
        self.inp += self.polygon.pace_transcript(self.pace_bits)
        #self.inp += self.polygon.sound_transcript(self.coord)
        #self.inp += self.polygon.sound_transcript([self.coord[0] + 5, self.coord[1]])
        #self.inp += self.polygon.sound_transcript([self.coord[0], self.coord[1] + 5])
        #for i in range(self.move_bits): # изменение
            #self.inp.append(self.last_act // (2 ** i) % 2)
                         
    

                    
    def action(self):
        if self.health <= 0:
            self.alive = False
        self.outp = self.brain.out(np.array(self.inp))
        act_num = np.argmax(self.outp)
        self.act = act_num
        return act_num
        
    def update(self):
        self.eaten = 0
        self.lifetime = 0
        self.health = 50
        self.alive = True
        x1 = randint(10, self.polygon.height - 1 - 10)
        y1 = randint(10, self.polygon.width - 1 - 10)        
        while self.polygon.world[x1][y1] != 0 or self.polygon.coord_h(x1, y1) == 0 or not self.born_loc(x1, y1):
            x1 = randint(0, self.polygon.height - 1)
            y1 = randint(0, self.polygon.width - 1)
        self.coord = [x1, y1]
        self.polygon.world[x1][y1] = self
        self.polygon.pos_dict[x1 + y1 * 10**5] = self
    def learn(self, x):
        #if x == 7:
        #    print(self.coord)
        self.brain.learn(x)
        
    def die(self):
        if self.alive and self.health <= 0:
            self.alive = False
            self.polygon.world[self.coord[0]][self.coord[1]] = 0
            
            
class Rabbit(Creature):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0), "bite"]
    color = (255, 255, 255)
    clas = "grass"
    def born_loc(self, y, x):
        return  self.polygon.coord_h(y, x) < 90
    
        
class Wolf(Creature):
    color = (255, 0, 0)
    clas = "meat"
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0), "bite"]
    def born_loc(self, y, x):
        return self.polygon.coord_b(y, x) == 1
    
        
        
