from gpanel import *

makeGPanel(0, 20, 0, 20)

setColor("blue")

x = 1;

while x < 20:
    y = 19
    while y >= x:
        move(x, y)
        fillCircle(0.5)
        y -= 1
    x += 1
