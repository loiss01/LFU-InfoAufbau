from gpanel import *

makeGPanel(0, 20, 0, 20)

x = 1;
y = 1;

for i in range(0,19*19):
    
    if (x == y):
        setColor("yellow");
    else:
        if (x < y):
           setColor("red");
        else:
           setColor("green");
    
    move(x,y);
    fillCircle(0.5);

    if(x == 19):
        x = 0;
        y = y + 1;

    x = x + 1;