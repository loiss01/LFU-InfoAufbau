from gpanel import *

BOARD_SICE = 3

FONT_ARIAL_PLAIN_17 = Font("Arial", Font.PLAIN, 17)

PLAYER_1_COLOR = "red"
PLAYER_2_COLOR = "green"

def drawBoard():
    for k in range(BOARD_SICE):
        for i in range(BOARD_SICE):
            rectangle(i, k, i + 1, k + 1)

def updateGameState(x,y):
    print(getPixelColor(x,y))
    color = "NONE";
    if getPixelColor(x,y) == makeColor("RED"):
        color = PLAYER_1_COLOR
    else: color = PLAYER_2_COLOR;

    x_int = int(x)
    y_int = int(y)
    print(x_int, y_int)

    list_to_change = board_state[ (BOARD_SICE-1) - y_int];
    list_to_change[x_int] = color;

def onMousePressed(x, y):
    if 0 < x < BOARD_SICE and 0 < y < BOARD_SICE:
        if getPixelColor(x, y) != makeColor("white"): return;

        if isLeftMouseButton():
            fill(x, y, "white", PLAYER_1_COLOR)
        elif isRightMouseButton():
            fill(x, y, "white", PLAYER_2_COLOR)
        print(x,y);
        updateGameState(x,y);

        print(board_state)

makeGPanel(-1, BOARD_SICE+1, -1, BOARD_SICE+1, mousePressed=onMousePressed)

drawBoard()

text(-1+1/50, -1+1/50, "Färbe mit der linken bzw. rechten Maustaste eines der neun Felder rot bzw. grün.", FONT_ARIAL_PLAIN_17, "darkgray", "white")

board_state = list()

for row_index in range(BOARD_SICE):
    row = list()
    for column_index in range(BOARD_SICE):
        row.append(None)
    board_state.append(row)