#import pygame
import archive
import sys
import math
from random import randint
from Polygon import *
from Creature import *
import pygame
SIZE = 700
screen = pygame.display.set_mode((SIZE + 5, SIZE))
colors = {0: (0, 0, 0), 1: (100, 100, 100), 2: (0, 255, 0), 4: (255, 0, 0), 15: (0, 0, 255)}
def draw_line(screen, fraq):
    pygame.draw.rect(screen, (255, 255, 255), (SIZE + 1, 0, 5, SIZE  * fraq), 0)
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


pol = Polygon(300, 300)
#pygame.mixer.init()
#soundtrack = pygame.mixer.Sound("sound.mp3")
#soundtrack.play()
        
generations = 5000
top_size = 15
rab_top_size = 40
rab_mult = 2
wolf_top_size = 10
wolf_mult = 2
rabbits = [Rabbit(pol) for i in range(rab_top_size)]
wolfs = [Wolf(pol) for i in range(wolf_top_size)]
speed = 1
wresults = []
rresults = []
top_rabbits = []
c = -1 # изменение
for i in range(150):
    Food(pol)
    
while True:
    #pol.board.restart()
    for i in pol.foods:
        i.update()
    c += 1             
    pol.pos_dict = dict()
    for i in top_rabbits:
        rabbits.append(Rabbit(pol, i.brain, 0))
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
    #print(pol.pos_dict)
    for t in range(2000):
    #    for i in range(pol.height):
    #        for j in range(pol.width):
    #            if pol.world[i][j] == 0:
    #                pol.world[i][j] = (randint(1, 15000) // 15000)         
        alive = 0
        for i in wolfs:
            i.health -= 0.2
            i.die()
            if i.alive:
                alive += 1
                i.lifetime += 1
                i.get()
                pol.move(i, i.action())
        for i in rabbits:
            i.health -= 0.2
            i.die()
            if i.alive:
                alive += 1
                i.lifetime += 1
                i.get()
                pol.move(i, i.action())
        if alive == 0:
            break
        pol.update()
        if (c % 1 == 0):
            pol.draw()
    rabbits.sort(key=lambda x: (-x.alive, -x.lifetime, -x.health, -x.eaten))
    for i in rabbits:
        r = Rabbit(None, i.brain, 0)
        r.lifetime = i.lifetime
        r.alive = i.alive
        r.eaten = i.eaten
        top_rabbits += [r]
    top_rabbits.sort(key=lambda x: (-x.alive, -x.lifetime, -x.health, -x.eaten))
    top_rabbits = top_rabbits[:top_size]
    wolfs.sort(key=lambda x: (-x.alive, -x.lifetime, -x.health, -x.eaten))
    print("ev: " + str(rabbits[0].brain.evolution_speed) + " lea: " + str(rabbits[0].brain.learning_speed))
    print(c, "best_r_eaten:", rabbits[0].eaten, "best_w_eaten:", wolfs[0].eaten)
    print("r", [i.lifetime for i in rabbits])
    print("w", [i.lifetime for i in wolfs])
    #print(c, pol.count(1), pol.count(2), pol.count(4))
    print("best rabbit brain:")
    print(rabbits[0].brain.matrix)
    #for i in rabbits[0].brain.matrix:
    #    for j in i:
    #        print(round(j, 4), end='  ')
    #    print()
    rresults.append(rabbits[0].eaten)
    wresults.append(wolfs[0].eaten)
    #pol.print()
    while len(rabbits) > rab_top_size:
        rabbits.pop()
    while len(wolfs) > wolf_top_size:
        wolfs.pop() 
    print("top rabbits: [", end = "")
    for i in top_rabbits:
        print(i.lifetime, end = " ")
    print("]")
    if (c > 25):
        print(c, "avg25", "best_r_eaten:", sum(rresults[-25:]) / 25, "best_w_eaten:", sum(wresults[-25:]) / 25)     
    if (c > 50):
        print(c, "avg50", "best_r_eaten:", sum(rresults[-50:]) / 50, "best_w_eaten:", sum(wresults[-50:]) / 50)    
    if (c > 100):
        print(c, "avg100", "best_r_eaten:", sum(rresults[-100:]) / 100, "best_w_eaten:", sum(wresults[-100:]) / 100)
    if (c > 250):
        print(c, "avg250", "best_r_eaten:",sum(rresults[-250:]) / 250, "best_w_eaten:", sum(wresults[-250:]) / 250)
    if (c > 500):
        print(c, "avg500", "best_r_eaten:",sum(rresults[-500:]) / 500, "best_w_eaten:", sum(wresults[-500:]) / 500)       
    #print("--------")
    #if c % 100 == 0:
    #    archive.exp(rabbits[0].brain, "rabbit_Ses_" + str(session) + "_Gen_" + str(c))
    #    archive.exp(wolfs[0].brain, "wolf_Ses_" + str(session) + "_Gen_" + str(c))