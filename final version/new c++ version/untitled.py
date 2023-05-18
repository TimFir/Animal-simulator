import pygame
from math import sqrt, log2

SIZE = 500

screen = pygame.display.set_mode((SIZE, SIZE))

f = open("spider6.txt")

s = f.read().split()
print(len(s))

for x in range(SIZE):
    for y in range(SIZE):
        #ss = 2500 / sqrt(int(s[(x // 10) * 10 + y // 10]))
        s1 = 255 - log2(int(s[x * SIZE + y])) * 10
        s2 = min(max(255 - int(s[x * SIZE + y]) // 2, 0), 255)
        s3 = int(min(max(255 - sqrt(int(s[x * SIZE + y])) * 3, 0), 255))
        color = (s2, s3, s1) 
        screen.set_at((x, y), color)

while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit() 
