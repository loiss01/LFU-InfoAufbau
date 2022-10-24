from gpanel import *
makeGPanel(0, 20, 0, 20)

setColor("blue");
for position in range(21):
    line((20 - position, 0), (0, position))

setColor("red")

for position in range(21):
    line(position, 0, 20, position)
    
setColor("green");
for position in range(21):
    line(0, position, position, 20)
    
setColor("violet");
for position in range(21):
    line((position, 20), (20, 20 - position))