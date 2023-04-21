from random import randint
INF = 10**9
class Creature:

    def __init__(self, polygon, color=5, brain=None, sp=0, outp_size=6):
        self.r = 4
        self.power = 10
        self.move_bits = 4
        self.last_act = 4 # изменение
        self.coord = [0, 0]
        self.alive = True
        self.polygon = polygon
        self.color = color
        self.eaten = 0
        self.health = 10
        self.polygon.pos_dict[self.coord[0] + self.coord[1] * 10**5] = self
        self.polygon.world[self.coord[0]][self.coord[1]] = self.color
        self.inp_size = (self.r ** 2) * self.polygon.index_bit_size + self.move_bits
        self.outp_size = outp_size
        if brain == None:
            self.brain = [[randint(0, 10) / 10 for i in range(self.outp_size)] for j in range(self.inp_size)]
        else:
            self.brain = [[0 for i in range(self.outp_size)] for j in range(self.inp_size)]
            for i in range(self.inp_size):
                for j in range(self.outp_size):
                    self.brain[i][j] = brain[i][j] + brain[i][j] * (randint(-100, 100) // 100) * sp
                    
                    
    def get(self):
        self.inp = []
        self.inp += self.polygon.position_transcript(self.coord, self.r)
        for i in range(self.move_bits): # изменение
            self.inp.append(self.last_act // (2 ** i) % 2)
                         
    

                    
    def action(self):
        if self.health <= 0:
            self.alive = False
        self.outp = [0 for i in range(self.outp_size)]
        for i in range(self.inp_size):
            for j in range(self.outp_size):
                self.outp[j] += self.inp[i] * self.brain[i][j]
        act_num = self.outp.index(max(self.outp))
        return act_num
        
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
        self.polygon.pos_dict[x1 + y1 * 10**5] = self
        
class Rabbit(Creature):
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0)]
    color = 2
    clas = "grass"
    def die(self):
        if self.health < 0:
            self.alive = False
            self.polygon.world[self.coord[0]][self.coord[1]] = 0
        
class Wolf(Creature):
    color = 4
    clas = "meat"
    actions = [(0, 1), (1, 0), (0, -1), (-1, 0), (0, 0), "bite"]
    
        
        
