from gpanel import *

class tiger:

    def __init__(self, GRIDSIZE):
        self.GRIDSIZE = GRIDSIZE
        makeGPanel(0, self.GRIDSIZE, 0, self.GRIDSIZE, keyPressed=self.onKeyPressed)
        # makeGPanel(-1, self.GRIDSIZE + 1, -1, self.GRIDSIZE + 1, keyPressed=self.onKeyPressed)
        #self.drawBoard()
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
    direction = "right"

    def drawBoard(self):
        #print("draw", self.grid)

        # Draw Grid
        for k in range(self.GRIDSIZE):
            for i in range(self.GRIDSIZE):
                rectangle(i, k, i + 1, k + 1)


        for y in range(self.GRIDSIZE):
            for x in range(self.GRIDSIZE):
                # Draw when empty
                if self.grid[y][x] == None:
                    fill(x + 0.1, y + 0.1, "blue", "white")
                    fill(x + 0.1, y + 0.1, "red", "white")
                    continue

                # Draw when "Apple"
                if self.grid[y][x] == "Apple":
                    fill(x + 0.1, y + 0.1, "white", "red")
                    continue

                # Draw Snake
                fill(x + 0.1, y + 0.1, "white", "blue")


    # def drawBoard(self):
    #     #print("draw", self.grid)
    #     for k in range(self.GRIDSIZE):
    #         for i in range(self.GRIDSIZE):
    #             rectangle(i, k, i + 1, k + 1)
    #
    #     for i in range(len(self.grid)):
    #         for u in range(len(self.grid[i])):
    #             if self.grid[i][u] == None:
    #                 fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "blue", "white")
    #                 fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "red", "white")
    #                 continue
    #             if self.grid[i][u] == "Apple":
    #                 fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "white", "red")
    #                 continue
    #             fill(self.koordTransformation_X(u) - 0.1, self.koordTransformation_Y(i) - 0.1, "white", "blue")


    # Changes the direction with a press of the arrow keys
    def onKeyPressed(self, key_code):
        if (key_code == 40):
            self.direction = "down"
            print("Keychanged ", key_code, " -- down")
        if (key_code == 39):
            self.direction = "right"
            print("Keychanged ", key_code, " -- right")
        if (key_code == 38):
            self.direction = "up"
            print("Keychanged ", key_code, " -- up")
        if (key_code == 37):
            self.direction = "left"
            print("Keychanged ", key_code, " -- left")



    # Returns the current Direction the snake should move
    def getDir(self):
        return self.direction




# print(koordTransformation(1,0))
# print(koordTransformation(2,0))
# print(koordTransformation(3,0))