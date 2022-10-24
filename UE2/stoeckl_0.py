from gpanel import *
from random import randint

def drawCircle(x_coordinate, y_coordinate, red_intensity, green_intensity, blue_intensity):
    print("drawing", color, "circle at x =", x_coordinate, "and y =", y_coordinate)

    setColor(red_intensity, green_intensity, blue_intensity);
    move(x_coordinate, y_coordinate);
    
    fillCircle(2)
    
makeGPanel(-10, 10, -10, 10)

repeat 5:
    drawCircle(randint(-10, 10), randint(-10, 10), randint(0, 255), randint(0, 255), randint(0, 255))