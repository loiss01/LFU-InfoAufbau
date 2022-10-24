from gpanel import *
from random import randint

makeGPanel(0, 20, 0, 20)
setColor("blue")

repeat 200:
    line([0,0],[randint(0,20),randint(0,20)])