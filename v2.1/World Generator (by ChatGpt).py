import math

seed_h = 109202
seed_b = 477828
qual = 300
lim = 28
heigh = 0.2
variate = [100, 100, 80, 95]
rad = 1000000


def f1(x):
    return max(((x+0.3) * (1 - (x+0.3)/1.3) + 0.1) * 3, 0)


def f2(x):
    if x < 1:
        return 1
    else:
        return 0


def rand_v(x, y, seed):
    x %= 1000000007
    y %= 1000000009

    pre = y * (seed - y) * (2 * seed - y) + x * (seed - x) * (2 * seed - x) - pow(x + y, 3)
    pre %= qual
    return float(pre) / qual * 2 * math.pi


def val(x, y, seed):
    x_int = x // qual
    y_int = y // qual

    x %= qual
    y %= qual

    xd = float(x) / qual
    yd = float(y) / qual

    mv = [(0, 0), (0, 1), (1, 0), (1, 1)]

    value = 0
    mas = 0

    for i in mv:
        ang = rand_v(x_int + i[0], y_int + i[1], seed)
        x1 = xd - i[0]
        y1 = yd - i[1]

        len = x1 * x1 + y1 * y1 + 0.001
        len = math.sqrt(len)

        m = max(1 / len / len - 1, 0)

        value += (math.cos(ang) * x1 + math.sin(ang) * y1 + 0.001) * m
        mas += m

    return value / mas


def val_h(x, y, seed):
    value_h = 0
    for i in range(8):
        value_h += val(int(x / pow(2, i)), int(y / pow(2, i)), seed) * pow(1.6, i)
    return value_h


def grad_h(x, y, seed):
    return (val_h(x + 1, y, seed) - val_h(x, y, seed), val_h(x, y + 1, seed) - val_h(x, y, seed))


def val_b(x, y, seed):
    a = [0, 0.5, 1]
    cnt = 0
    vh = val_h(x, y, seed_h)
    vb = val_h(x, y, seed_b)
    for i in range(len(a)):
        if math.atan(vh) / math.pi + vb / lim > a[i]:
            cnt += 1
    return cnt


def Ray(x, y, ang, alpha):
    len = 10
    vh = val_h(x, y, seed_h)
    while len < rad and val_h(x + int(len * math.cos(ang)), y + int(len * math.sin(ang)), seed_h) > len * alpha + vh and ((int(pow(x + len * math.cos(ang), 1.5) - pow(y + len * math.sin(ang), 2)) % 100 + 100) % 100 <= variate[val_b(x + int(len * math.cos(ang)), y + int(len * math.sin(ang)), seed_b)]):
        len *= 1.1

    return (val_b(x + int(len * math.cos(ang)), y + int(len * math.sin(ang)), seed_b), len)


class Ant:

    def __init__(self):
        self.ang = 0
        self.protein = 0
        self.fat = 0
        self.water = 0

        self.lens = [0, 0, 0, 0]
        self.got = [False, False, False, False]
        self.power = [False, False, False, False]

a = 1000
with open("show.txt", "w") as f:
    for i in range(a):
        print(i)
        for j in range(a):
            f.write(str(max(int(val_h(i * 100, j * 100, seed_h) * 50), 0)) + " ")
            f.write(str(val_b(i * 100, j * 100, seed_b)) + " ")
        f.write("\n")
f.close()
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
            
#from PIL import Image, ImageDraw, ImageFont
#a = 100
#img = Image.new('RGB', (a, a), 'black')
#f = open("show.txt", "r")
#s = list(map(int, (f.read()).split()))
#for i in range(a * a):
#    img.putpixel((i // a, i % a), f1(int(s[i * 2] * 0.3), s[i * 2 + 1]))
#img.show()    