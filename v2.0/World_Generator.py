def f1(h, b):
    if h != 0:
        h = h // 2 + 70
    if h <= 0:
        return (0, 0, 100)
    elif b == 0:
        return (h - 30, h - 30, h - 30)
    elif b == 1:
        return (h, h - 50, h - 100)
    else:
        return (h - b * 10, h + b * 20, h - b * 10)

import numpy as np
a = 1000
def world(h, w):
    world = np.zeros((h, w, 2))
    f = open("show.txt", "r")
    s = list(map(int, (f.read()).split()))
    for i in range(h):
        #print(i)
        for j in range(w):
            world[i, j, 0] = int(s[(a*i + j) * 2 ] * 0.3)
            world[i, j, 1] = int(s[(a*i + j) * 2 + 1])  
    f.close()
    return world