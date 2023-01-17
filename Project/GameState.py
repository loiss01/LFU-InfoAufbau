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
        # Create empty List
        for i in range(GRIDSIZE):
            row = list()
            for y in range(GRIDSIZE):
                row.append(None)
            self.grid.append(row)


        # Create Snake List
        self.snake.append((2, 0))
        self.snake.append((1, 0))
        self.snake.append((0, 0))

        # Add Snake to Grid List
        self.grid[0][2] = self.gridStates.snake
        self.grid[0][1] = self.gridStates.snake
        self.grid[0][0] = self.gridStates.snake


    # Returns the Snake List
    def getSnake(self):
        return self.snake


    # Set X cords of the Head of the Snake
    def setX(self, x):
        self.x = x


    # Set Y cords of the Head of the Snake
    def setY(self, y):
        self.y = y


    # add +1 to the integer that defines the length of the snake
    def addSize(self):
        self.size = self.size + 1


    # Returns the hole Grid List
    def getGrid(self):
        return self.grid


    # Sets a new Grid List
    def setGrid(self, grid):
        self.grid = grid


    # Sets a new Snake List
    def setSnake(self, newSnake):
        self.snake = newSnake
