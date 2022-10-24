from gpanel import *

makeGPanel(-22, 22, -2, 20)

setColor("orange")

w = 40
y = 0

while(y < 20):
    move(0, y)
    
    fillRectangle(w, 2)
    
    w = w - 4
    y = y + 2

#repeat 10:
#    move(0, y)
#    
#    fillRectangle(w, 2)
#    
#    w = w - 4
#    y = y + 2