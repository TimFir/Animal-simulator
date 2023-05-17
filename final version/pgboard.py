import pygame
import math
import random
import numpy as np
import World_Generator as wg
def f1(h, b):
    if h != 0:
        h = h // 2 + 70
    if h <= 0:
        return (0, 0, 100)
    elif b == 0:
        return (h - 30, h - 30, h - 30)
    elif b == 1:
        return (max(h, 100), max(h, 100) - 50, max(h, 100) - 100)
    else:
        return (h - b * 10, min(255, h + b * 20), h - b * 10)

class Board():
    pos = 0j
    move = False
    prmouse = pos
    def __init__(self,worlddim, screen, w = 700, h = 700):
        self.sc = screen
        self.scale = 10
        self.w = w
        self.h = h
        self.ww = worlddim[1]
        self.wh = worlddim[0]
        self.world = wg.world(worlddim[0], worlddim[1])
    def draw(self):
        pygame.draw.rect(self.sc, (0, 0, 0), (0, 0, self.h, self.w))
        pygame.draw.circle(self.sc, (255, 255, 255), (self.pos.real, self.pos.imag), 3) 
        step = 1
        if self.scale < 10:
            step = int(1 + (10 - self.scale) // 3 )
        for i in range(0, self.ww, step):
            for j in range(0, self.wh, step):
                #print(self.world[i, j, 0], self.world[i, j, 1])
                #print(f1(self.world[i, j, 0], self.world[i, j, 1]))
                if (0 <= self.pos.real + self.scale * i <= self.h and 0 <= self.pos.imag + self.scale * j <= self.w):
                    pygame.draw.rect(self.sc, f1(self.world[i, j, 0], self.world[i, j, 1]), (self.pos.real + self.scale * i, self.pos.imag + self.scale * j, self.scale * step + 1, step * self.scale + 1))
    def drawpoint(self, y, x, color, size=3):
        pygame.draw.circle(self.sc, color, (self.pos.real + self.scale * y + self.scale / 2, self.pos.imag + self.scale * x + self.scale / 2), max(size, self.scale / 2))
    def event(self, e):
        if e.type == pygame.QUIT:
            quit()        
        if self.move:
            if e.type == pygame.MOUSEMOTION:          
                self.pos += e.pos[0] + 1j * e.pos[1] - self.prmouse
                self.prmouse = e.pos[0] + 1j * e.pos[1]
            if e.type == pygame.MOUSEBUTTONUP and e.button == 2:
                self.move = False            
        else:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 2:
                self.move = True
                self.prmouse = e.pos[0] + e.pos[1] * 1j
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 5:
            self.scale **= 0.9
            self.pos -= (self.pos - e.pos[0] - 1j * e.pos[1])*0.05
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 4:
            self.scale **= 1.1
            self.pos += (self.pos - e.pos[0] - 1j * e.pos[1])*0.05
    def restart(self):
        self.world = wg.world(self.wh, self.ww)
#pygame.init()     
#SIZE = 700
#screen = pygame.display.set_mode((SIZE + 5, SIZE))
#b = Board((500, 500), screen)
#while True:
    #print(1)
#    b.draw()
#    pygame.display.update()  
#    for event in pygame.event.get():
#        b.event(event)      