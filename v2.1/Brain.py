
import numpy as np
import time
import random


class Brain:
    evolution_speed = 10**(-6)
    learning_speed = 10**(-6)
    discont = 0.8
    #ln = 0
    def __init__(self, dim, br_m=None, ev=False):
        if br_m is None:
            self.matrix = np.random.sample(dim) 
        else:
            self.matrix = np.zeros(dim)
            self.matrix += br_m
        self.dim = dim
        self.inp_lib = np.zeros((20, dim[0]))
        self.out_lib = np.zeros(20)
        self.outp_lib = np.zeros(20)
        self.last = 0
        if ev:
            self.evolve()        
        
    def evolve(self):
        #ev_d = (np.random.sample(self.dim)-0.5) * self.evolution_speed 
        #self.matrix = np.add(self.matrix, ev_d)
        pass
        
    def learn(self, result):
        #print(result)
        deltas = np.zeros(self.dim)
        #self.ln += 1
        #if self.ln % 100 == 0:
        #print(self.inp_lib[0])
        #print(self.inp_lib[0].shape)
        for i in range(self.last - 1, -1, -1):
            d1 = np.zeros(self.dim)
            k = int(self.out_lib[i])
            x1 = np.zeros((self.dim))
            x1 = np.dot(self.inp_lib[i][:, np.newaxis], np.ones((1, self.dim[1])))
            d1[:, k] += (self.inp_lib[i] * self.matrix[:, k]) * (self.learning_speed * (self.discont ** (self.last - i - 1)) * result)
            d1[:,] -= (x1 * self.matrix) * (self.learning_speed * (self.discont ** (self.last - i - 1)) * result) / (self.dim[1])
            deltas += d1
        #if result == 7:
            #print(deltas)
        self.matrix += deltas
        self.matrix = np.abs(self.matrix)
            
    def out(self, inp):
        outp = np.dot(inp, self.matrix)
        self.inp_lib[self.last] = inp
        #print(np.where(outp == np.max(outp)))
        self.out_lib[self.last] = np.argmax(outp)
        self.outp_lib[self.last] = np.max(outp)
        self.last += 1
        if (self.last == 20):
            self.last = 10
            self.inp_lib[:10] = self.inp_lib[10:20]
            self.inp_lib[10:] = np.zeros((10, self.dim[0]))
            self.out_lib[:10] = self.out_lib[10:20]
            self.out_lib[10:] = np.zeros((10))   
            self.outp_lib[:10] = self.outp_lib[10:20]
            self.outp_lib[10:] = np.zeros((10))             
        return outp
        


br = Brain((30, 4))
t1 = time.time()
#for i in range(1000):
    #br.evolve()
    #inp = np.random.sample((1, 30))
    #k = br.out(inp)
    #print(k)
    #print(np.argmax(k))
    #print(br.outp_lib[br.last - 1])
    #if (np.argmax(k)) == 3:
    #    br.learn(100)
    #else:
    #    br.learn(-1)
    #print(br.matrix)
    #print(br.out(np.array([1, 2])))
#print(br.matrix)