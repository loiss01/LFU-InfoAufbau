from gpanel import *

makeGPanel(0, 20, 0, 20)

setColor("red")

x = 1;
y = 1;

while x < 20:
    y = 1
    while y <= 20:
        move(x, y)
        fillCircle(0.5)
        y += 2
    x += 2
