from enum import *

class GameState:
    size = 3
    x = 2
    y = 0
    grid = list()
    snake = list()

    applex = 0
    appley = 0
    appleBool = False

    class gridStates(Enum):
        snake = "Snake"
        apple = "Apple"

    def __init__(self, GRIDSIZE):
        for i in range(GRIDSIZE):
            row = list()
            for y in range(GRIDSIZE):
                row.append(None)
            self.grid.append(row)

        self.snake.append((self.x, self.y))
        self.snake.append((1, 0))
        self.snake.append((0, 0))

        self.grid[0][2] = self.gridStates.snake
        self.grid[0][1] = self.gridStates.snake
        self.grid[0][0] = self.gridStates.snake

    def getState(self):
        return self.state

    def getSnake(self):
        return self.snake

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def addSize(self):
        self.size = self.size + 1

    def getGrid(self):
        return self.grid

    def setGrid(self, grid):
        self.grid = grid


    def setSnake(self, newSnake):
        self.snake = newSnake
