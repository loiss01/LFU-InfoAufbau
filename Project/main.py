from GameState import *
from random import randint
from tiger import *
from time import *

#Snake Game in 10x10 grid

# Set the Size of the Gamefielde 10x10
GRIDSIZE = 10


GameState = GameState(GRIDSIZE)
gui = tiger(GRIDSIZE)

# Returns a free GridSpot
def getFreeRadomGridSpot(grid):
    freeGridSpots = list()

    for i in range(GRIDSIZE):
        for u in range(GRIDSIZE):
            if grid[i][u] is None:
                freeGridSpots.append((i, u))

    return freeGridSpots[randint(0, len(freeGridSpots) - 1)]


def move():
    # Check if player is pressing a key
    newSnake = list()

    # If the Player goes to the right
    if gui.getDir() == "right":

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

    if gui.getDir() == "left":

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

    if gui.getDir() == "up":

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

    if gui.getDir() == "down":

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
    pass

# Game Tick every 0. Seconds
def tick():
    #debug()
    move()
    if GameState.appleBool:
        updateGrid(GameState.getSnake())
    else:
        AppleKords = getFreeRadomGridSpot(GameState.getGrid())

        GameState.applex = AppleKords[0]
        GameState.appley = AppleKords[1]

        updateGrid(GameState.getSnake())
        GameState.appleBool = True


def updateGrid(snake):
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

    if GameState.appleBool:
        grid[GameState.applex][GameState.appley] = GameState.gridStates.apple

    GameState.setGrid(grid)
    gui.updateGrid(grid)
    #print(grid)
    


while (True):
    sleep(0.25)
    tick()
    print(GameState.applex, " ", GameState.appley, " - ", GameState.appleBool)
    #print("tick")

#tick()
#debug()
#tick()
#debug()