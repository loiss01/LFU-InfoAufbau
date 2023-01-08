from gpanel import *

class tiger:

    def __init__(self, GRIDSIZE):
        self.GRIDSIZE = GRIDSIZE
        makeGPanel(-1, self.GRIDSIZE + 1, -1, self.GRIDSIZE + 1, keyPressed=self.onKeyPressed)
        self.drawBoard()
        pass

    def updateGrid(self, grid):
        self.grid = grid
        self.drawBoard()


    GRIDSIZE = 10
    grid = [[None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None]]
    direction = "up"



    def drawBoard(self):
        print("draw", self.grid)
        for k in range(self.GRIDSIZE):
            for i in range(self.GRIDSIZE):
                rectangle(i, k, i + 1, k + 1)

        for i in range(len(self.grid)):
            for u in range(len(self.grid[i])):
                if self.grid[i][u] == None:
                    fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "blue", "white")
                    fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "red", "white")
                    continue
                if self.grid[i][u] == "Apple":
                    fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "white", "red")
                    continue
                fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "white", "blue")


    def onKeyPressed(self, key_code):
        if (key_code == 38):
            self.direction = self.direction.up
        if (key_code == 39):
            self.direction = self.direction.right
        if (key_code == 40):
            self.direction = self.direction.down
        if (key_code == 37):
            self.direction = self.direction.left
        print("Keychanged ", key_code)


    def koordTransformation_X(self, x):
        return x


    def koordTransformation_Y(self,y):
        return self.GRIDSIZE - y






# print(koordTransformation(1,0))
# print(koordTransformation(2,0))
# print(koordTransformation(3,0))