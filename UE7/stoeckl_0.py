from gpanel import *
from math import pow

X_MIN = -4
X_MAX = 4

STEP_SIZE = 1/100
ROOT_POINT_RADIUS = 1/10


def f(x):
    return pow(x,3)-9*x;

def f_a(x):
    return pow(3*x,2)-9;

def newton(x):
    mem = x - f(x)/f_a(x);
    for i in range(0,100):
        mem = mem - f(mem)/f_a(mem);
    print(mem);
    return mem;


makeGPanel(-6, 6, -30, 30)
drawGrid(-5, 5, -25, 25, "gray")
lineWidth(2)

x = X_MIN

move(x, f(x))

while x < X_MAX:
    y = f(x)
      
    draw(x, y)

    x = x + STEP_SIZE

x = X_MIN

Nullstellen = [];     
while x < X_MAX:
    if int(newton(x)) in Nullstellen:
        continue;
    print(int(newton(x)));
    #Rundungsfehler beim convertieren von double to int -3.0 wird zu -2???    
    fillCircle( int(newton(x)) ,0,ROOT_POINT_RADIUS);
    
    x = x + 2;