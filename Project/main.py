from GameState import *
from random import randint
from tiger import *
from time import *

#Snake Game in 10x10 grid

# Set the Size of the Gamefielde 10x10
GRIDSIZE = 10


GameState = GameState(GRIDSIZE)
gui = tiger(GRIDSIZE)
APPLE = False

# Returns a free GridSpot
def getFreeRadomGridSpot(grid):
    freeGridSpots = list()

    for i in range(GRIDSIZE):
        for u in range(GRIDSIZE):
            if grid[i][u] is None:
                freeGridSpots.append((i, u))

    return freeGridSpots[randint(0, len(freeGridSpots) - 1)]


class direction(Enum):
    up = "up"
    down = "down"
    right = "right"
    left = "let"


def move():
    # Check if player is pressing a key
    movement = direction.right
    newSnake = list()

    # If the Player goes to the right
    if movement == direction.right:

        for i in range(len(GameState.getSnake())):
            if i == 0:
                x = GameState.getSnake()[0][0]
                y = GameState.getSnake()[0][1]
                x = x + 1

                newSnake.append((x, y))

            if i == len(GameState.getSnake()) - 1:
                break
            newSnake.append(GameState.getSnake()[i])
        GameState.setSnake(newSnake)
        print(newSnake)

    if movement == direction.left:

        for i in range(len(GameState.getSnake())):
            if i == 0:
                x = GameState.getSnake()[0][0]
                y = GameState.getSnake()[0][1]
                x = x - 1

                newSnake.append((x, y))

            if i == len(GameState.getSnake()) - 1:
                break
            newSnake.append(GameState.getSnake()[i])
        GameState.setSnake(newSnake)

    if movement == direction.up:

        for i in range(len(GameState.getSnake())):
            if i == 0:
                x = GameState.getSnake()[0][0]
                y = GameState.getSnake()[0][1]
                y = y - 1

                newSnake.append((x, y))

            if i == len(GameState.getSnake()) - 1:
                break
            newSnake.append(GameState.getSnake()[i])
        GameState.setSnake(newSnake)

    if movement == direction.down:

        for i in range(len(GameState.getSnake())):
            if i == 0:
                x = GameState.getSnake()[0][0]
                y = GameState.getSnake()[0][1]
                y = y + 1

                newSnake.append((x, y))

            if i == len(GameState.getSnake()) - 1:
                break
            newSnake.append(GameState.getSnake()[i])
    GameState.setSnake(newSnake)


# Debug printout
def debug():
    print("Debug", GameState.getSnake())
    print("Debug", GameState.getGrid())


# Game Tick every 0.5 Seconds
def tick():
    debug()
    move()

    if GameState.getAppleBool():
        updateGrid(GameState.getSnake(), None)
    else:
        updateGrid(GameState.getSnake(), getFreeRadomGridSpot(GameState.getGrid()))
        GameState.setAppleBool(True)

def updateGrid(snake, applepos):
    grid = list()

    # Make new "empty" List
    for i in range(GRIDSIZE):
        row = list()
        for y in range(GRIDSIZE):
            row.append(None)
        grid.append(row)

    for entry in snake:
        ex = entry[0]
        ey = entry[1]

        grid[ey][ex] = GameState.gridStates.snake
        pass

    if applepos != None:
        grid[applepos[0]][applepos[1]] = GameState.gridStates.apple

    GameState.setGrid(grid)
    gui.updateGrid(grid)
    print(grid)
    


while (True):
    sleep(0.5)
    tick()
    print("tick")

#tick()
#debug()
#tick()
#debug()