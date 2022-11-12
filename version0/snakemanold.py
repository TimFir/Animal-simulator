from random import randint
from math import e

INF = 10**9
m1 = 30
n1 = 30
n2 = 30
m2 = 30
r = 5
speed = 0.2
start_size = 100
top_size = 10
pop_mult = 5
speed_const = 1
dop_size = 0
tact_num = 8

generations = 3000

outp_size = 4
inp_size = (2 * r + 1) ** 2 + dop_size + tact_num + outp_size
translate = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Snake_Man:
    def __init__(self, brain=None, sp=0):
        self.eaten = set()
        self.out = [0 for i in range(outp_size)]
        self.coord = [n // 2, m // 2]
        self.way = set()
        self.tact = 0
        if brain == None:
            self.brain = [[randint(0, 10) / 10 for i in range(outp_size)] for j in range(inp_size)]
        else:
            self.brain = [[0 for i in range(outp_size)] for j in range(inp_size)]
            for i in range(inp_size):
                for j in range(outp_size):
                    self.brain[i][j] += brain[i][j]
                    self.brain[i][j] += (randint(-10, 10) / 10) * sp

    def get(self, n, m):
        self.inp = []
        self.inp += self.out
        for i in range(self.coord[0] - r, self.coord[0] + r + 1):
            for j in range(self.coord[1] - r, self.coord[1] + r + 1):
                self.inp.append(int(i >= 0 and j >= 0 and i < n and j < m and world[i][j] == 1 and ((i, j) not in self.eaten)) - 1 * (i < 0 or j < 0 or i >= n or j >= m))
        for i in range(tact_num):
            self.inp.append(int(self.tact & (1 << i) > 0))
        self.tact += 1

    def action(self, n, m):
        self.outp = [0 for i in range(outp_size)]
        for i in range(inp_size):
            for j in range(outp_size):
                self.outp[j] += self.inp[i] * self.brain[i][j]
        for i in range(outp_size):
            if self.coord[0] + translate[i][0] < 0 or self.coord[0] + translate[i][0] >= n or self.coord[1] + translate[i][1] < 0 or self.coord[1] + translate[i][1] >= m:
                self.outp[i] = -INF
        act = self.outp.index(max(self.outp))
        self.out = [0 for i in range(outp_size)]
        self.out[act] = 1
        self.coord[0] += translate[act][0]
        self.coord[1] += translate[act][1]
        self.way.add((self.coord[0], self.coord[1]))
        if world[self.coord[0]][self.coord[1]] == 1 and ((self.coord[0], self.coord[1]) not in self.eaten):
            self.eaten.add((self.coord[0], self.coord[1]))


print("-----")
top = []
way = set()
n = randint(n1, n2)
m = randint(m1, m2)    
world = [[randint(0, 6) // 6 for i in range(m)] for j in range(n)]
for i in range(start_size):
    top.append(Snake_Man())
population = top[:]
results = []

for c in range(generations):

    speed = 0.5 - 0.5 * c / generations
    for i in population:
        i.eaten = set()
        i.coord = [randint(0, n - 1), randint(0, m - 1)]
        i.way = set()
    ticks = 0
    while ticks < 100:
        ticks += 1
        for i in population:
            i.get(n, m)
        for i in population:
            i.action(n, m)

    population.sort(key=lambda x: -len(x.eaten))
    # print(len(population[0].eaten))
    results.append(len(population[0].eaten))
    if c > 100:
        print(c, sum(results[-100:]) / 100, len(population[0].way))
    # print(len(population))
    #for i in range(len(population) - 1, -1, -1):
    #    print(len(population[i].eaten), end=" ")
    #print()
    top = []
    for i in range(n):
        for j in range(m):
            if ((i, j) in population[0].way):
                print("*", end="")
            else:
                print(world[i][j], end="")
        print()
    print("---------")
    way = set()
    while len(population) > top_size:
        population.pop()
    #for i in population:
    #    print(i.brain[0][0], end = " ")
    #print()    
    for i in range(top_size):
        for j in range(pop_mult):
            population.append(Snake_Man(population[i].brain, speed))    
            #print(population[-1].brain[0][0])
            
    n = randint(n1, n2)
    m = randint(m1, m2)    
    world = [[randint(0, 6) // 6 for i in range(m)] for j in range(n)]    
#file = open("bestbrains.txt", "a") 
#file.write(str(population[0].brain))
#file.write("\n")
#file.close()
#file = open("bestresults.txt", "a") 
#file.write(str(sum(results[-100:]) / (100)))
#file.write("\n")
#file.close()
#file = open("results.txt", "a") 
#file.write(str(results))
#file.write("\n")
#file.close()
print(sum(results[-100:]) / (100))
print(results)
print(population[0].brain)
while True:
    pass