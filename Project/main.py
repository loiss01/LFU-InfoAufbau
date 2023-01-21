from GameState import *
from random import randint
from tiger import *
from time import *

#Snake Game in 10x10 grid

# Set the Size of the Gamefielde 10x10
GRIDSIZE = 10


gamestate = GameState(GRIDSIZE)
gui = tiger(GRIDSIZE)

# Returns a free GridSpot which is not occupied
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

        for i in range(len(gamestate.getSnake())):
            if i == 0:
                # Get the head of snake
                x = gamestate.getSnake()[0][0]
                y = gamestate.getSnake()[0][1]
                x = x + 1

                # Add Head of the Snake to new Snake List
                newSnake.append((x, y))

            # Check if last entry is called if so last Item wil be removed (because the has to mave)
            if i == len(gamestate.getSnake()) - 1:
                gamestate.lastSegment = gamestate.getSnake()[i]
                break
            # Passing the Snake Tiles to the new List
            newSnake.append(gamestate.getSnake()[i])
        # gamestate.setSnake(newSnake)

    if gui.getDir() == "left":

        for i in range(len(gamestate.getSnake())):
            if i == 0:
                x = gamestate.getSnake()[0][0]
                y = gamestate.getSnake()[0][1]
                x = x - 1

                newSnake.append((x, y))

            if i == len(gamestate.getSnake()) - 1:
                gamestate.lastSegment = gamestate.getSnake()[i]
                break
            newSnake.append(gamestate.getSnake()[i])

    if gui.getDir() == "up":

        for i in range(len(gamestate.getSnake())):
            if i == 0:
                x = gamestate.getSnake()[0][0]
                y = gamestate.getSnake()[0][1]
                y = y + 1

                newSnake.append((x, y))

            if i == len(gamestate.getSnake()) - 1:
                gamestate.lastSegment = gamestate.getSnake()[i]
                break
            newSnake.append(gamestate.getSnake()[i])
        gamestate.setSnake(newSnake)

    if gui.getDir() == "down":

        for i in range(len(gamestate.getSnake())):
            if i == 0:
                x = gamestate.getSnake()[0][0]
                y = gamestate.getSnake()[0][1]
                y = y - 1

                newSnake.append((x, y))

            if i == len(gamestate.getSnake()) - 1:
                gamestate.lastSegment = gamestate.getSnake()[i]
                break
            newSnake.append(gamestate.getSnake()[i])

    gamestate.setSnake(newSnake)
    #print(gamestate.getGrid())
    #print(newSnake)


# Debug printout
def debug():
    print("Debug", gamestate.getSnake())
    print("Debug", gamestate.getGrid())
    pass


# Game Tick every 0. Seconds
def tick():
    #debug()
    move()

    # Check if eat Apple
    #print(gamestate.getSnake()[0], (gamestate.applex, gamestate.appley))
    if gamestate.getSnake()[0] == (gamestate.appley, gamestate.applex):
        print("EAT APPLE")
        gamestate.addSize()
        gamestate.appleBool = False
        snake = list(gamestate.getSnake())
        snake.append(gamestate.lastSegment)
        gamestate.setSnake(snake)


    # check if eat snake
    fist = True
    for i in gamestate.getSnake():
        if fist:
            fist = False
            continue
        if gamestate.getSnake()[0] == i:
            pass
            gameover()
            break

    if gamestate.appleBool:
        updateGrid(gamestate.getSnake())
    else:
        AppleKords = getFreeRadomGridSpot(gamestate.getGrid())
        print(AppleKords)
        gamestate.applex = AppleKords[0]
        gamestate.appley = AppleKords[1]
        print(gamestate.applex, gamestate.appley)
        updateGrid(gamestate.getSnake())
        gamestate.appleBool = True


def updateGrid(snake):
    grid = list()

    # Make new "empty" List
    for i in range(GRIDSIZE):
        row = list()
        for y in range(GRIDSIZE):
            row.append(None)
        grid.append(row)

    # Add Snake to new Grid
    for entry in snake:
        ex = entry[0]
        ey = entry[1]

        grid[ey][ex] = gamestate.gridStates.snake
        pass

    # Add Apple to Game Grid
    if gamestate.appleBool:
        grid[gamestate.applex][gamestate.appley] = gamestate.gridStates.apple

    gamestate.setGrid(grid)
    gui.updateGrid(grid)
    #print(grid)


def gameover():
    print("GAME OVER, Score: ", gamestate.size)
    exit(1)

while (True):
    sleep(0.25)
    try:
        tick()
    except Exception:
        gameover()

