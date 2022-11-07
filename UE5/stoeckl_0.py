from gpanel import *

FONT_ARIAL_PLAIN_17 = Font("Arial", Font.PLAIN, 17)

def onMousePressed(x, y):
    move(x, y)

def onMouseDragged(x, y):
    draw(x, y)
    

def onKeyPressed(key_code):
    if(key_code == 82):
        setColor("red");
    elif(key_code == 71):
        setColor("green");
    elif(key_code == 66):
        setColor("blue");
    elif(key_code == 67):
        setColor("black");

makeGPanel(mousePressed=onMousePressed, mouseDragged=onMouseDragged, keyPressed=onKeyPressed)

text(1/100, 1/100, "Zeichne mit gedrückter Maustaste. Wähle Farbe mit [R]-, [G]-, [B]- oder [C]-Taste.", FONT_ARIAL_PLAIN_17, "darkgray", "white")