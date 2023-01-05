from GameState import *
from random import randint

#Snake Game in 10x10 grid

# Set the Size of the Gamefielde 10x10
GRIDSIZE = 10
GameState = GameState(GRIDSIZE)
apple = False

# Returns a free GridSpot
def getFreeRadomGridSpot(grid):
    freeGridSpots = list()

    for i in range(GRIDSIZE):
        for u in range(GRIDSIZE):
            if grid[i][u] is None:
                freeGridSpots.append((i, u))

    return freeGridSpots[randint(0, len(freeGridSpots) - 1)]


class direction(Enum):
    up = "uparror"
    down = "downarror"
    right = "rightarror"
    left = "leftarror"


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
    print(GameState.getSnake())
    print(GameState.getGrid())


# Game Tick every 0.5 Seconds
def tick():
    if not apple:
        print(getFreeRadomGridSpot(GameState.grid))
        pass
    move()

    updateGrid(GameState.getSnake(), getFreeRadomGridSpot(GameState.getGrid()))


def updateGrid(snake, applepos):
    grid = list()

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

    grid[applepos[0]][applepos[1]] = GameState.gridStates.apple
    GameState.setGrid(grid)


tick()
debug()
tick()
debug()