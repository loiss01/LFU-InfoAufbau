from gpanel import *

makeGPanel(0, 20, 0, 20)

setColor("red")

x = 1;
y = 1;

#while x < 20:
#    y = 1
#    while y <= x:
#        move(x, y)
#        fillCircle(0.5)
#        y += 1
#    x += 1

for i in range(0,19*19):
    move(x,y);
    fillCircle(0.5);

    if(x == 19):
        x = 0;
        y = y + 1;

    x = x + 1;