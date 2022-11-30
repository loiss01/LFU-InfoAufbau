from gpanel import *
from random import random

GPANEL_WINDOW_WIDTH = 600
GPANEL_WINDOW_HEIGHT = 600

DOT_SIZE = 5 / 1000

APPROX = 100000


def onMousePressed(x, y):
    if isLeftMouseButton():
        setColor("darkslategray")
        fillCircle(x, y, DOT_SIZE)
        print(x,y)
        polygon_vertices.append((x, y))
    elif isRightMouseButton():
        title("Zeichne Polygon … – Warte bitte!")

        setColor("ghostwhite")
        fillPolygon(polygon_vertices)

        setColor("black")
        polygon(polygon_vertices)

        title("APPROXIMIERE … – Warte bitte!")

        inside = 0;
        outside = 0;
        for i in range(APPROX):
            x = random()
            y = random()


            pixel_color = getPixelColorStr(x, y)
            if (pixel_color == "ghostwhite"):
                inside = inside +1;
            else:
                outside = outside +1;



        print("in", inside)
        print("out", outside)

        a = inside/APPROX;
        print(a);

        title("APPROX: 600*600*" + str(a) + " = "+ str(a*600*600) + "pixel^2")
        # title("Pixel mit Koordinaten (" + str(round(x, 2)) + ", " + str(round(y, 2)) + ") ist '" + pixel_color + "'")


makeGPanel(Size(GPANEL_WINDOW_HEIGHT, GPANEL_WINDOW_WIDTH), mousePressed=onMousePressed)

title("Klicke mit linker Maustaste um Polygon zu zeichnen, rechter um Fläche zu bestimmen ...")

polygon_vertices = []