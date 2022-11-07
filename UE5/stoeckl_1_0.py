from gpanel import *

FONT_ARIAL_PLAIN_17 = Font("Arial", Font.PLAIN, 17)

def drawGrid():
    for k in range(3):
        for i in range(3):
            rectangle(i, k, i + 1, k + 1)  

def onMousePressed(x, y):

    if isLeftMouseButton() and 0 < x < 3 and 0 < y < 3:
        fill(x, y, "white", "red")
    if isRightMouseButton() and 0 < x < 3 and 0 < y < 3:
        fill(x, y, "white", "green")

makeGPanel(-1, 4, -1, 4, mousePressed=onMousePressed)

drawGrid()

text(-1+1/50, -1+1/50, "Färbe mit der linken bzw. rechten Maustaste eines der weißen Felder rot bzw. grün.", FONT_ARIAL_PLAIN_17, "darkgray", "white")