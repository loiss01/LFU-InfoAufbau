from gpanel import *

class tiger:


    def updateGrid(self, grid):
        self.grid = grid
        drawBoard()
    pass

GRIDSIZE = 10

grid = [[None, None, "Snake", "Snake", "Snake", "Snake", None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None]]
direction = ""



def drawBoard():
    print("draw", grid)
    for k in range(GRIDSIZE):
        for i in range(GRIDSIZE):
            rectangle(i, k, i + 1, k + 1)

    for i in range(len(grid)):
        for u in range(len(grid[i])):
            if grid[i][u] == None: continue
            if grid[i][u] == "Apple":
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