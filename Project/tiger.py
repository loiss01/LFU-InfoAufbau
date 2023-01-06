from gpanel import *
import time

GRIDSIZE = 10

data = [[None, None, "Snake", "Snake", "Snake", "Snake", None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, "Apple", None, None]]
direction = ""


def drawBoard():
    for k in range(GRIDSIZE):
        for i in range(GRIDSIZE):
            rectangle(i, k, i + 1, k + 1)

    for i in range(len(data)):
        for u in range(len(data[i])):
            if data[i][u] == None: continue
            if data[i][u] == "Apple":
                fill(koordTransformation_X(u) - 0.1, koordTransformation_Y(i) - 0.1, "white", "red")
                continue
            fill(koordTransformation_X(u) - 0.1, koordTransformation_Y(i) - 0.1, "white", "blue")


def onKeyPressed(key_code):
    if (key_code == 38):
        direction = "up"
    if (key_code == 39):
        direction = "rechts"
    if (key_code == 40):
        direction = "down"
    if (key_code == 37):
        diection = "left"
    print("Keychanged ", key_code)


def koordTransformation_X(x):
    return x


def koordTransformation_Y(y):
    return GRIDSIZE - y


makeGPanel(-1, GRIDSIZE + 1, -1, GRIDSIZE + 1, keyPressed=onKeyPressed)

drawBoard()

# print(koordTransformation(1,0))
# print(koordTransformation(2,0))
# print(koordTransformation(3,0))