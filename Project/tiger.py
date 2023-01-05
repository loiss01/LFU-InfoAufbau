from gpanel import *

GRIDSIZE = 10

data = [[None, "Snake", "Snake", "Snake", None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None, None, None],
        [None, None, None, "Apple", None, None, None, None, None, None]]

makeGPanel(-1, GRIDSIZE + 1, -1, GRIDSIZE + 1)


def drawBoard():
    for k in range(GRIDSIZE):
        for i in range(GRIDSIZE):
            rectangle(i, k, i + 1, k + 1)

    for i in range(len(data)):
        for u in range(len(data[i])):
            if data[i][u] == None: continue
            if data[i][u] == "Apple":
                fill(i + 0.1, u + 0.1, "white", "red")
                continue
            fill(i + 0.1, u + 0.1, "white", "blue")


drawBoard()
fill(1, 1, "white", "red")