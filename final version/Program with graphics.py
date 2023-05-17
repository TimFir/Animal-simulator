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


pol = Polygon(200, 200)
#pygame.mixer.init()
#soundtrack = pygame.mixer.Sound("sound.mp3")
#soundtrack.play()
        
generations = 5000
top_size = 4
rab_top_size = 20
rab_mult = 1
wolf_top_size = 10
wolf_mult = 1
#imported_rab = []
imported_rab = ["rabbit_Ses_478009_Gen_11_res_40", "rabbit_Ses_586017_Gen_5_res_59", "rabbit_Ses_586017_Gen_7_res_43", "rabbit_Ses_586017_Gen_14_res_49", "rabbit_Ses_692921_Gen_4_res_47", "rabbit_Ses_790918_Gen_23_res_50"]
#imported_wol = []
imported_wol = ["wolf_Ses_586017_Gen_5_res_21", "wolf_Ses_586017_Gen_7_res_10", "wolf_Ses_790918_Gen_0_res_15", "wolf_Ses_790918_Gen_4_res_11", "wolf_Ses_848409_Gen_1_res_19"]
drink_pen = 0
rabbits = [Rabbit(pol) for i in range(rab_top_size)]
wolfs = [Wolf(pol) for i in range(wolf_top_size)]
for i in imported_rab:
    for j in range(2):
        rabbits.append(Rabbit(pol))
        rabbits[-1].brain.matrix = np.array(archive.imp(i), dtype=np.float64)
for i in imported_wol:
    for j in range(2):
        wolfs.append(Wolf(pol))
        wolfs[-1].brain.matrix = np.array(archive.imp(i), dtype=np.float64)
#rabbits[0].brain.matrix[1][3] = 10**10
#rabbits[0].brain.matrix[4][1] = 10**10
#rabbits[0].brain.matrix[7][2] = 10**10
#rabbits[0].brain.matrix[10][0] = 10**10
#rabbits[0].brain.matrix[25][4] = 10**20
#0001
#0100
#0010
#1000
speed = 1
wresults = []
rresults = []
top_rabbits = []
c = -1 # изменение
for i in range(180):
    Food(pol)
    
while True:
    #pol.board.restart()
    for i in pol.foods:
        i.update()
    c += 1
    pol.timer = 0
    pol.pos_dict = dict()
    for i in top_rabbits:
        rabbits.append(Rabbit(pol, i.brain, True))
    for i in range(rab_top_size):
        for j in range(rab_mult - 1):
            rabbits.append(Rabbit(pol, rabbits[i].brain, True))
    for i in range(wolf_top_size):
        for j in range(wolf_mult - 1):
            wolfs.append(Wolf(pol, wolfs[i].brain, True)) 
    for i in rabbits:
        i.update()
        #print(i.alive)
        #print(i.coord)
    for i in wolfs:
        i.update()  
    print(len(rabbits), len(wolfs))
    #pol.print()
    print(c, pol.count(1), pol.count(2), pol.count(4))
    #print(pol.pos_dict)
    for t in range(1500):
    #    for i in range(pol.height):
    #        for j in range(pol.width):
    #            if pol.world[i][j] == 0:
    #                pol.world[i][j] = (randint(1, 15000) // 15000)         
        alive = 0
        for i in pol.foods:
            i.restore()
        for i in wolfs:
            i.health -= 0.4
            i.learn(-0.4)
            #i.drink -= drink_pen
            #if i.drink < 0:
            #    i.health -= 5
             #   i.learn(-5)            
            i.die()
            if i.alive:
                alive += 1
                i.lifetime += 1
                i.get()
                pol.move(i, i.action())
            if i.health >= 200:
                for x in [(0, 1), (1, 0), (-1, 0), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]:
                    if pol.world[i.coord[0] + x[0]][i.coord[1] + x[1]] == 0:
                        i.health -= 100
                        w = Wolf(pol, i.brain, True)
                        wolfs.append(w)
                        w.update()
                        w.coord = [i.coord[0] + x[0], i.coord[1] + x[1]]
                        print("w", end="")
                        break           
        for i in rabbits:
            i.health -= 0.4
            i.learn(-0.4)
            i.drink -= drink_pen
            if i.drink < 0:
                i.health -= 3
                i.learn(-3)
            i.die()
            if i.alive:
                alive += 1
                i.lifetime += 1
                i.get()
                pol.move(i, i.action())
            if i.health >= 200:
                for x in [(0, 4), (4, 0), (-4, 0), (0, -4), (-3, -3), (-3, 3), (3, 3), (3, -3)]:
                    if pol.coord(i.coord[0] + x[0],i.coord[1] + x[1]) == 0:
                        i.health -= 100
                        r = Rabbit(pol, i.brain, True)
                        rabbits.append(r)
                        r.update()
                        pol.world[r.coord[0]][r.coord[1]] = 0
                        r.coord = [i.coord[0] + x[0], i.coord[1] + x[1]]
                        pol.world[i.coord[0] + x[0]][i.coord[1] + x[1]] = r
                        print("r", end="")
                        break
        if alive == 0:
            break
        pol.update()
        if (c % 1 == 0):
            pol.draw()
        #print(rabbits[0].inp)
        temp = 0
        while temp < 100000:
            temp+=1
    rabbits.sort(key=lambda x: (-x.eaten, -x.alive, -x.lifetime, -x.health))
    for i in wolfs:
        i.die()
        i.alive = False    
    for i in rabbits:
        i.die()
        i.alive = False
        r = Rabbit(None, i.brain, False)
        r.lifetime = i.lifetime
        r.alive = i.alive
        r.eaten = i.eaten
        top_rabbits += [r]
    top_rabbits.sort(key=lambda x: (-x.eaten, -x.alive, -x.lifetime, -x.health))
    top_rabbits = top_rabbits[:top_size]
    wolfs.sort(key=lambda x: (-x.eaten, -x.alive, -x.lifetime, -x.health))
    print("ev: " + str(rabbits[0].brain.evolution_speed) + " lea: " + str(rabbits[0].brain.learning_speed))
    print(c, "best_r_eaten:", rabbits[0].eaten, "best_w_eaten:", wolfs[0].eaten)
    print("r", [i.eaten for i in rabbits])
    print("w", [i.eaten for i in wolfs])
    #print(c, pol.count(1), pol.count(2), pol.count(4))
    print("best wolf brain:")
    print(wolfs[0].brain.matrix)
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
    if rabbits[0].eaten > 10:
        archive.exp(rabbits[0].brain.matrix, "rabbit_Ses_" + str(session) + "_Gen_" + str(c) + "_res_" + str(rabbits[0].eaten))
    if wolfs[0].eaten > 7:
        archive.exp(wolfs[0].brain.matrix, "wolf_Ses_" + str(session) + "_Gen_" + str(c) + "_res_" + str(wolfs[0].eaten))
        #archive.exp(wolfs[0].brain.matrix, "wolf_Ses_" + str(session) + "_Gen_" + str(c))