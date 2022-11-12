import math
from random import randint


session = randint(0, 1000000)
timer = 0
sound_length = 3
index_bit_size = 4
freq_types = 10
pace_bits = 8
move_bits = 3
INF = 10**9

rabbit_col = 2
food = 1
border = 15

def f(x):
    return 1 / (1 + 1.5**(-x))

class Polygon:
    translate = [(1, 0), (0, 1), (-1, 0), (0, -1), (0, 0), "bite"]
    def __init__(self, height=100, width=100):
        self.index_bit_size = 4
        self.sounds = set()
        self.height = height
        self.width = width
        self.pos_dict = dict()
        self.creatures = []
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
    
    def position_transcript(self, coord, r):
        vector = []
        for i in range(coord[0] - r, coord[0] + r + 1):
            for j in range(coord[1] - r, coord[1] + r + 1):
                if (self.width > j and self.height > i and i >= 0 and j >= 0):
                    for k in range(index_bit_size):
                        vector.append(self.world[i][j] // (2 ** i) % 2)
                else:
                    for k in range(index_bit_size):
                        vector.append(border // (2 ** i) % 2) 
        return vector
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
                vector_sounds[i[2]] += 1 / (math.hypot(coord[0] - i[0][0], coord[1] - i[0][1]) + 1)
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
    
    def move(self, cr, act):
        self.world[cr.coord[0]][cr.coord[1]] = 0
        self.pos_dict.pop(cr.coord[0] + (cr.coord[1]) * 10**5)
        if act < 5:
            x = cr.coord[0] + self.translate[act][0]
            y = cr.coord[1] + self.translate[act][1]
            if -1 < x < self.height and -1 < y < self.width and self.world[x][y] < 2:
                cr.coord[0] = x
                cr.coord[1] = y
            if self.world[cr.coord[0]][cr.coord[1]] == 1 and cr.clas == "grass":
                cr.eaten += 1

                 

        elif act == 5:
            for i in [(0, 1), (1, 0), (-1, 0), (0, -1)]:
                if cr.coord[0] + i[0] + (cr.coord[1] + i[1]) * 10**5 in self.pos_dict:
                    self.pos_dict[cr.coord[0] + i[0] + (cr.coord[1] + i[1]) * 10**5].health -= cr.power
                    cr.eaten += 1
        self.pos_dict[cr.coord[0] + (cr.coord[1]) * 10**5] = cr
        self.world[cr.coord[0]][cr.coord[1]] = cr.color
    def print(self):
        print("Polygon")
        for i in self.world:
            print(*i)
        print("end")
