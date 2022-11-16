from gpanel import *
from random import randint

NUMBER_OF_ROLLS = 10000

def drawBin(x, height, width=0.5):
    setColor("red")
    fillRectangle(x-width/2, 0, x+width/2, height)
    setColor("black")

makeGPanel(-1, 14, -1/10*NUMBER_OF_ROLLS/2, (1+1/10)*NUMBER_OF_ROLLS/2)
title("Häufigkeitsverteilung der Augenzahlen bei " + str(NUMBER_OF_ROLLS) + " Würfen eines fairen Würfels.")

drawGrid(0, 13, 0, NUMBER_OF_ROLLS//2, 7, 10, "gray")

histogram = [0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0]

for _ in range(NUMBER_OF_ROLLS):
    pip = randint(1, 6) + randint(1,6)
    histogram[pip-1] += 1

for x in range(0, 12):
    drawBin(x+1, histogram[x])