import math
import noise

from PIL import Image
from PIL import ImageColor

octaves = 8
scale = 1/1240
H = 0.8

C1 = (255,205,131)
C2 = (255,105,9)

C3 = (24,163,0)
C4 = (178,255,164)

C5 = (12,159,238)
C6 = (132,175,255)

C7 = (16, 16, 16)
C8 = (200, 200, 200)

def color_mixer(c1, c2):
    f = (c1[0] - (c1[0] - c2[0]) / 2, c1[1] - (c1[1] - c2[1]) / 2, c1[2] - (c1[2] - c2[2]) / 2)
    final = []
    mult = 1
    for t in f:
        if t > 255:
            mult = t / 255
    
    for t in f:
        final.append(int(t * mult))
    
    return tuple(final)


def add_vec(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def mult_vec(alpha, v):
    return (v[0] * alpha, v[1] * alpha) 

def fbm(vec):
    t = 0.0
    for i in range(0, octaves):
        f = pow(2.0, float(i))
        a = pow(f, -H)
        t += a * noise.snoise2(vec[0] * f, vec[1] * f)
    
    return t

def gradVal(value, c1, c2):
    color = [0, 0, 0]
    for i in range(0, 3):
        color[i] = int(c1[i] + (value) * (c2[i] - c1[i]))
    
    return tuple(color)

def genSingleGrad(b, c1, c2):
    if b > 1.0:
        b = 1.0
    
    if b < 0:
        b = 0.00001
    return gradVal(b, c1, c2)

def genColor(value):
    b1 = ((value[0] + 1) / 2) + 0.001
    b2 = ((value[1] + 1) / 2) + 0.001
    b3 = ((value[2] + 1) / 2) + 0.001

    return color_mixer(color_mixer(genSingleGrad(b1, C5, C6), genSingleGrad(b2, C1, C2)), genSingleGrad(b3, C7, C8))

def pattern(v):
    l1 = (fbm(v) + v[0], fbm(v) + v[1])
    l2 = (fbm(l1) + v[0], fbm(l1) + v[1])
    l3 = (fbm(l2) + v[0], fbm(l2) + v[1])
    return fbm(l3), fbm(l2), fbm(l1)

'''
def pattern(v):
    l1 = (fbm(v) + v[0], fbm(v) + v[1])
    l2 = (fbm(l1) + v[0], fbm(l1) + v[1])

    return fbm(l2), fbm(l1)
'''

img = Image.new('RGB', (1240, 720), 'black')
pixel = img.load()

for y in range(0, 720):
    for x in range(0, 1240):
        b = genColor(pattern((x * scale, y * scale)))
        for t in b:
            if t > 255:
                print(f'FOUND INVALID COLOR: {t}')
        pixel[x, y] = b

img.show()
img.save('example2.png')