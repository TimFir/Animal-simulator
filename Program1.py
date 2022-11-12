#import pygame
import archive
import sys
import math
from random import randint
from Polygon_3 import *
from Creature1 import *


def f(x):
    return 1 / (1 + 1.5**(-x))

#pygame.init()

#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

session = randint(0, 1000000)
r = 5
timer = 0
sound_length = 3
index_bit_size = 4
freq_types = 10
pace_bits = 8
move_bits = 3
INF = 10**9

rabbit_col = 2
wolf_col = 4
food = 1
border = 15


pol = Polygon(10, 10)
 
for i in range(pol.height):
    for j in range(pol.width):
        pol.world[i][j] = (randint(1, 2) // 2)
        
generations = 5000
rab_top_size = 3
rab_mult = 2
wolf_top_size = 2
wolf_mult = 4
rabbits = [Rabbit(pol, rabbit_col) for i in range(rab_top_size)]
wolfs = [Wolf(pol, wolf_col) for i in range(wolf_top_size)]
speed = 0.3
wresults = []
rresults = []
c = -1 # изменение
    
while True:
    c += 1
    for i in range(pol.height):
        for j in range(pol.width):
            pol.world[i][j] = (randint(1, 2) // 2)   
    pol.pos_dict = dict()
    for i in range(rab_top_size):
        for j in range(rab_mult - 1):
            rabbits.append(Rabbit(pol, rabbit_col, rabbits[i].brain, speed))
    for i in range(wolf_top_size):
        for j in range(wolf_mult - 1):
            wolfs.append(Wolf(pol, wolf_col, wolfs[i].brain, speed)) 
            
    for i in rabbits:
        i.update()
    for i in wolfs:
        i.update()
    pol.print()
    print(c, pol.count(1), pol.count(2), pol.count(4))
    #print(pol.pos_dict)
    for t in range(200):
        for i in wolfs:
            i.get()
            pol.move(i, i.action())
        for i in rabbits:
            i.die()
            if i.alive:
                i.get()
                pol.move(i, i.action())
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
    print("--------")
    if c % 100 == 0: # изменение
        archive.exp(rabbits[0].brain, "rabbit_Ses_" + str(session) + "_Gen_" + str(c))
        archive.exp(wolfs[0].brain, "wolf_Ses_" + str(session) + "_Gen_" + str(c))