# gpanel.py
# Version 1.05; Jan 31, 2017

'''
Module to create a graphics window of default size 501x501 pixels (client drawing area)
using a coordinate system with x-axis from left to right, y-axis from bottom to top
(called user coordinates, default range 0..1, 0..1).

The module provides a global namespace for GPanel class methods. It also contaisn
the class GPane that can be used to embed a GPanel graphics window together with
other widgets in a GUI application.

The drawing methods perform drawing operation in an offscreen buffer (QPixmap)
and automatically renders it on the screen, so the graphics is shown step-by-step.

User coordinates:  (ux, uy)
Pixel coordinates: (px, py) (screen pixels)
Transformation: px = px(ux), py = py(uy)
Pixel coordinate range: 0..winWidth - 1 (inclusive), 0..winHeight - 1 (inclusive); (0,0) upper left corner, x to the right, y downwards
User coordinate range: xmin..xmax (inclusive), ymin..ymax (inclusive); (0,0) lower left corner, x to the right, y upwards.

Transformation: user(ux, uy) to pixel(px, py):
(width = winWidth - 1, height = winHeight - 1)
px = a * ux + b
py = c * uy + d
with a = width / (xmax - xmin)
b = width * xmin / (xmin - xmax)
c = height / (ymin - ymax)
d = height * ymax / (ymax - ymin)

Inverse:
ux = (px - b) / a
uy = (py - d) / c

Because of the transformation from float to pixel coordinates, some rounding errors
may happen. If you need pixel accuracy, define a GPanel window with some user defined width x height,
e.g. makeGPanal(Size(501, 401)). Define then user coordinates in the range 0..width-1, 0..height-1, e.g.
window(0, 500, 0, 400). Now pixels in the range 0..500 x 0..400 (inclusive) may be addressed with no
rounding errors. (This is a total of 501 x 401 pixels.)

If you prefer a coordinate system with the origin at the upper left corner, define the y-range in reverse
order, e.g. window(0, 500, 400, 0).

WARNING: Because PyQt is not thread-safe, in principle all graphics drawings should be
executed in the GUI thread (for GPanel the main thread or a GUI callback).

In order to get notifications for keyboard and mouse callbacks, the main thread should
not be blocked otherwise than within the keep() function.

Typical program:

from pygpanel import *

makeGPanel(0, 10, 0, 10)
for ypt in range(0, 11, 1):
    line(0, ypt, 10 - ypt, 0)
    time.sleep(0.1) # to see what happens
keep()

keep() is blocking and keeps the graphics window open until the close button is hit or the
Python process terminates.
'''

from __future__ import division
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import thread
import sys, time, math
import random

_p = None
isTigerJython = False

class _WindowNotInitialized(Exception): pass

def _isGPanelValid():
   if _p == None:
      raise _WindowNotInitialized("Use \"makeGPanel()\" to create the graphics window before calling GPanel methods.")

def makeGPanel(*args, **kwargs):
    '''
    Constructs a GPanel and displays a non-resizable graphics window.
    Defaults with no parameter:
    Window size: 501x501 pixels
    Window title: "GPanel".
    User coordinates: 0, 1, 0, 1.
    Background color: white.
    Pen color: black.
    Pen size: 1.

    1 Parameter: Size(window_width, window_height).
    4 Parameters: xmin, xmax, ymin, ymax.

    KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
    @param Size: a Size reference to define the dimension of the graphics windows.
    @param xmin: left x user coordinate
    @param xmax: right x user coordinate
    @param ymin: lower y  user coordinate
    @param ymax: upper y user coordinate
    @param kwargs: mousePressed, mouseReleased, mouseDragged, keyPressed, keyReleased, closed
    '''
    global _p

    if _p == None:
        _p = GPanel(*args)

    for key in kwargs:
        if key == "mousePressed":
            _p.addMousePressListener(kwargs[key])
        elif key == "mouseReleased":
            _p.addMouseReleaseListener(kwargs[key])
        elif key == "mouseDragged":
            _p.addMouseDragListener(kwargs[key])
        elif key == "keyPressed":
            _p.addKeyPressListener(kwargs[key])
        elif key == "keyReleased":
            _p.addKeyReleaseListener(kwargs[key])
        elif key == "closed":
            _p.addCloseListener(kwargs[key])
    return _p

def addCloseListener(closeListener):
    '''
    Registers the given function that is called when the title bar
    close button is hit.

    If a listener (!= None) is registered, the automatic closing is disabled.
    To close the window, call sys.exit().

    KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
    @param closeListener: a callback function called when the close button is hit
    '''
    _isGPanelValid()
    _p.addCloseListener(closeListener)

def addKeyPressListener(onKeyPressed):
    '''
    Registers a callback that is invoked when a key is pressed (and the graphics window has the focus).

    KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
    @param onKeyPressed: a callback function called when a key is pressed
    '''
    _isGPanelValid()
    _p.addKeyPressListener(onKeyPressed)

def addKeyReleaseListener(onKeyReleased):
    '''
    Registers a callback that is invoked when a key is released (and the graphics window has the focus).

    KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
    @param onKeyReleased: a callback function called when a key is pressed
    '''
    _isGPanelValid()
    _p.addKeyReleaseListener(onKeyReleased)

def addMouseDragListener(onMouseDragged):
    '''
    Registers a callback that is invoked when the mouse is moved while a mouse button is pressed (drag).

    KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
    @param onMouseDragged: a callback function called when the moused is dragged
    '''
    _isGPanelValid()
    _p.addMouseMoveListener(onMouseDragged)

def addMousePressListener(onMousePressed):
    '''
    Registers a callback that is invoked when a mouse button is pressed.
    Use isLeftMouseButton() or isRightMouseButton() to check which button used.

    KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
    @param onMousePressed: a callback function called when a mouse button is pressed
    '''
    _isGPanelValid()
    _p.addMousePressListener(onMousePressed)

def addMouseReleaseListener(onMouseReleased):
    '''
    Registers a callback that is invoked when a mouse button is releases.
    Use isLeftMouseButton() or isRightMouseButton() to check which button used.

    KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
    @param onMouseReleased: a callback function called when a mouse button is released
    '''
    _isGPanelValid()
    _p.addMouseReleaseListener(onMouseReleased)

def arc(radius, startAngle, spanAngle):
    '''
    Draws a circle sector with center at the current graph cursor position,
    given radius and given start and span angles.
    @param radius: the radius of the arc
    @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
    @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
    '''
    _isGPanelValid()
    _p.arc(radius, startAngle, spanAngle)

def bgColor(*args):
    '''
    Same as setBgColor().
    '''
    setBgColor(*args)

def chord(radius, startAngle, spanAngle):
    '''
    Draws a circle chord with center at the current graph cursor position,
    given radius and given start and span angles (in degrees, positive
    counter-clockwise, zero to east).
    @param radius: the radius of the arc
    @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
    @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
    '''
    _isGPanelValid()
    _p.chord(radius, startAngle, spanAngle)

def circle(radius):
    '''
    Draws a circle with center at the current graph cursor position
    with given radius in horizontal window coordinates.
    @param radius: the radius of the circle
    '''
    _isGPanelValid()
    _p.circle(radius)

def clear():
    '''
    Clears the graphics window and the offscreen buffer used by the window
    (fully paint with background color).
    Sets the current graph cursor position to (0, 0).
    If enableRepaint(false) only clears the offscreen buffer.
    '''
    _isGPanelValid()
    _p.clear()

def delay(delayTime):
    '''
    Stop execution for given delay time.
    @param delayTime: the delay time (in ms)
    '''
    time.sleep(delayTime / 1000.0)

def draw(*args):
    '''
    Draws a line form current graph cursor position to (x, y).
    Sets the graph cursor position to (x, y).
    Also with one parameter of type complex, list or tuple.
    @param x: the x coordinate of the target point
    @param y: the y coordinate of the target point
    @param target: (alternative) the target point as complex, list or tuple
    '''
    x, y = _getCoords(*args)
    _isGPanelValid()
    _p.draw(x, y)

def drawGrid(*args):
    '''
    Draws a coordinate system with annotated axes.
    (You must increase the user coordinate system at least 10% in both directions.)

    Overloaded variants:

    drawGrid(x, y): Grid with 10 ticks in range 0..x, 0..y. Label text depends if x, y or int or float

    drawGrid(x, y, color): same with given grid color

    drawGrid(x1, x2, y1, y2): same with given span x1..x2, y1..y2

    drawGrid(x1, x2, y1, y2, color): same with given grid color

    drawGrid(x1, x2, y1, y2, x3, y3): same with given number of ticks x3, y3 in x- and y-direction
    '''
    _isGPanelValid()
    _p.drawGrid(*args)

def ellipse(a, b):
    '''
    Draws an ellipse with center at the current graph cursor position
    with given axes.
    @param a: the major ellipse axis
    @param b: the minor ellipse axis
    '''
    _isGPanelValid()
    _p.ellipse(a, b)

def enableRepaint(enable):
    '''
    Enables/Disables automatic repaint in graphics drawing methods.
    @param enable: if True, the automatic repaint is enabled; otherwise disabled
    '''
    _isGPanelValid()
    _p.enableRepaint(enable)

def erase():
    '''
    Same as clear(), but lets the current graph cursor unganged.
    '''
    _isGPanelValid()
    _p.erase()

def fill(x, y, *args):
    '''
    Fills the closed unicolored region with the inner point (x, y) with
    the replacement color (RGB, RGBA or X11 color string).
    The old color is not given, the color of the current (x, y) pixel is taken.
    @param x: the x coordinate of the inner point
    @param y: the y coordinate of the inner point
    @param color: the old color (RGB list/tuple or X11 color string) (may be omitted)
    @param replacementColor: the new color (RGB list/tuple or X11 color string)
    '''
    _isGPanelValid()
    _p.fill(x, y, *args)

def fillArc(radius, startAngle, spanAngle):
    '''
    Draws a filled circle sector with center at the current graph cursor position,
    given radius and given start and span angles (in degrees, positive
    counter-clockwise, zero to east). (fill color = pen color)
    @param radius: the radius of the arc
    @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
    @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
    '''
    _isGPanelValid()
    _p.fillArc(radius, startAngle, spanAngle)

def fillChord(radius, startAngle, spanAngle):
    '''
    Draws a filled circle chord with center at the current graph cursor position,
    given radius and given start and span angles (in degrees, positive
    counter-clockwise, zero to east). (fill color = pen color)
    @param radius: the radius of the arc
    @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
    @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
    '''
    _isGPanelValid()
    _p.fillChord(radius, startAngle, spanAngle)

def fillCircle(radius):
    '''
    Draws a filled circle with center at the current graph cursor position
    with given radius in horizontal window coordinates (fill color = pen color).
    @param radius: the radius of the circle
    '''
    _isGPanelValid()
    _p.fillCircle(radius)

def fillEllipse(a, b):
    '''
    Draws a filled ellipse with center at the current graph cursor position
    with given axes (fill color = pen color).
    @param a: the major ellipse axis
    @param b: the minor ellipse axis
    '''
    _isGPanelValid()
    _p.fillEllipse(a, b)

def fillPath(color):
    '''
    Closes the path started with startPath() and shows a filled polygon from the saved
    draw() positions with given color.
    '''
    _isGPanelValid()
    _p.fillPath(color)

def fillPolygon(*args):
    '''
    Draws a filled polygon with given list of vertexes (list of [x, y])
    (fill color = pen color).
    1 parameter: a list/tuple of the corners [x, y]
    2 parameters: two lists/tuples x, y of corresponding x-y pairs
    '''
    _isGPanelValid()
    _p.fillPolygon(*args)

def fillRectangle(*args):
    '''
    Draws a filled rectangle (fill color = pen color).
    2 parameters: Center at the current graph cursor position
                  and given width and height
    4 parameters: Given diagonal
    '''
    _isGPanelValid()
    _p.fillRectangle(*args)

def fillTriangle(*args):
    '''
    Draws a filled triangle with given corners.
    6 parameters: x1, y1, x2, y2, x3, y3 coordinates of corners
    3 parameters: [x1, y1], [x2, y2], [x3, y3] lists of corners
    '''
    _isGPanelValid()
    _p.fillTriangle(*args)

def getDividingPoint(*args):
    '''
    Returns the tuple of user coordinates of the point on the line through the point pt1 = (x1, y1)
    and the point pt2 = (x2, y2) that is in distance ratio times the length from pt1 to pt2 from
    pt1. For ratio < 0 the point is in the opposite direction.
    3 parameteters: pt1, pt2 (complex/list/tuple), ratio
    5 parameteters: x1, y1, x2, y2, ratio
    '''
    if len(args) == 5:
        x1 = args[0]
        y1 = args[1]
        x2 = args[2]
        y2 = args[3]
        ratio = args[4]
    elif len(args) == 3:
        x1, y1, x2, y2 = _get2Coords(args[0], args[1])
        ratio = args[2]
    else:
        raise ValueError("Illegal number of parameters.")
    _isGPanelValid()
    return _p.getDividingPoint(x1, y1, x2, y2, ratio)

def getBitmap():
    '''
    Returns the QImage of the complete graphics area.
    (For compatiblity with TigerJython.)
    '''
    _isGPanelValid()
    return _p.getFullImage()

def getFullImage():
    '''
    Returns the QImage of the complete graphics area.
    '''
    _isGPanelValid()
    return _p.getFullImage()

def getImage(filename):
    '''
    Same as loadImage(filename)
    (For compatiblity with TigerJython.)
    '''
    return loadImage(filename)

def loadImage(filename, pic_format = None):
    '''
    Returns a QImage of the picture loaded from the given file. For pic_format = None,
    the picture format is guessed from the file data.
    @param: the file path to the picture file
    @param pic_format: format of picture, supported:  "None" (default), "GIF", "JPG",
    "BMP", "PNG", "PBM", "PGM", "PPM", "TIFF", "XBM" "XPM".
    '''
    return GPanel.loadImage(filename, pic_format)

def getPainter():
    '''
    Returns the QPainter reference used to draw into the offscreen buffer.
    '''
    _isGPanelValid()
    return _p.getPainter()

def getPixelColor(*args):
    '''
    Returns the RGBA color tuple of a pixel with given user coordinates.
    No params: Returns color at current graph cursor position.
    '''
    _isGPanelValid()
    return _p.getPixelColor(*args)
    
def getPixelColorStr(*args):
    '''
    Returns the X11 color string of a pixel with given user coordinates.
    No params: Returns color at current graph cursor position.
    '''
    _isGPanelValid()
    return _p.getPixelColorStr(*args)

def getPos():
    '''
    Returns a tuple with current graph cursor position (tuple, user coordinates).
    '''
    _isGPanelValid()
    return _p.getPos()

def getPosX():
    '''
    Returns the current graph cursor x-position (user coordinates).
    @return: x coordinate of graph cursor
    @rtype: float
    '''
    _isGPanelValid()
    return _p.getPosX()

def getPosY():
    '''
    Returns the current graph cursor y-position (user coordinates).
    @return: y coordinate of graph cursor
    @rtype: float
    '''
    _isGPanelValid()
    return _p.getPosY()

def getScreenWidth():
    '''
    Returns the width of the screen (in pixels).
    @return: screen width
    @rtype: int
    '''
    return GPanel.getScreenWidth()

def getScreenHeight():
    '''
    Returns the height of the screen (in pixels).
    @return: screen height
    @rtype: int
    '''
    return GPanel.getScreenHeight()

def imageFromData(data, pic_format, x, y):
    '''
    Draws the picture with given string data in JPEG format at user coordinates of lower left corner.
    @param data: picture data stream in string format
    @param pic_format: format of picture, supported: "GIF", "JPG", "BMP", "PNG",
    "PBM", "PGM", "PPM", "TIFF", "XBM" "XPM"
    @param x: x coordinate of lower left corner
    @param y: y coordinate of lower left corner
    @return: True, if operation is successful; otherwise false
    @rtype: boolean
    '''
    _isGPanelValid()
    img = QImage()
    rc = img.loadFromData(data, pic_format)
    if rc:
        image(img, x, y)
        return True
    return False

def image(*args):
    '''
    Draws the picture with given file path or given image at given upper-left coordinates.
    1st parameter: image path (string) or QImage reference
    2nd, 3rd parameters: llx, lly (lower left corner in user coordinates)
    '''
    _isGPanelValid()
    _p.showImage(*args)

def isLeftMouseButton():
    '''
    Returns True, if the last mouse action was performed with the left mouse button.
    '''
    _isGPanelValid()
    return _p.isLeftMouseButton()

def isRightMouseButton():
    '''
    Returns True, if the last mouse action was performed with the right mouse button.
    '''
    _isGPanelValid()
    return _p.isRightMouseButton()

def keep():
    '''
    Blocks until the title bar's close button is hit. Then cleans up
    the graphics system.
    '''
    _isGPanelValid()
    _p.keep()

def line(*args):
    '''
    Draws a line with given user start and end coordinates
    and sets the graph cursor position to the end point.
    Also with 2 parameters of type complex, list or tuple.
    4 parameters: x1, y1, x2, y2
    2 parameters: pt1, pt2 as complex/list/tuple
    '''
    x1, y1, x2, y2 = _get2Coords(*args)
    _isGPanelValid()
    _p.line(x1, y1, x2, y2)

def lineWidth(width):
    '''
    Sets the current pen size (width) (>=1).
    Returns the previouis pen size.

    Same as setPenSize(). For TigerJython compatiblity.
    @param width: the pen width (>=1)
    '''
    setPenSize(width)

def makeColor(r, g, b):
    '''
    Returns the tuple (r, g,  b). For compatibility with TigerJython.
    '''
    return (r, g, b)

def move(*args):
    '''
    Sets the current graph cursor position to given user coordinates.
    (without drawing anything).
    Also with 1 parameter of type complex, list or tuple.

    Same as pos().
    @param x: the x coordinate of the target point
    @param y: the y coordinate of the target point
    @param target: (alternative) the target point as complex, list or tuple
    '''
    pos(*args)

def point(*args):
    '''
    Draws a single point with current pen size and pen color at given user coordinates.
    No params: draws a current graph cursor position
    @param x: the x coordinate of the target point
    @param y: the y coordinate of the target point
    @param target: (alternative) the target point as complex, list or tuple
    '''
    _isGPanelValid()
    _p.point(*args)

def linePlot(*args):
    '''
    Draws a line plot with given x,y data.
    1 parameter: a list/tuple of subsequent data points [x, y]
    2 parameters: two lists/tuples x, y of corresponding x-y pairs
    The graph cursor position remains unchanged.
    '''
    _isGPanelValid()
    _p.linePlot(*args)

def pos(*args):
    '''
    Sets the current graph cursor position to given user coordinates (x, y).
    (without drawing anything).
    Also with 1 parameter of type complex, list or tuple.

    Same as move().
    @param x: the x coordinate of the target point
    @param y: the y coordinate of the target point
    @param target: (alternative) the target point as complex, list or tuple
    '''
    x, y = _getCoords(*args)
    _isGPanelValid()
    _p.pos(x, y)

def polygon(*args):
    '''
    Draws a filled polygon with given list of vertexes (list of [x, y])
    (fill color = pen color).
    1 parameter: a list/tuple of the corners [x, y]
    2 parameters: two lists/tuples x, y of corresponding x-y pairs
    '''
    _isGPanelValid()
    _p.polygon(*args)

def rectangle(*args):
    '''
    Draws a rectangle.
    2 parameters: Center at the current graph cursor position
                  and given width and height.
    4 parameters: Given diagonal
    '''
    _isGPanelValid()
    _p.rectangle(*args)

def repaint():
    '''
    Renders the offscreen buffer in the graphics window.
    '''
    _isGPanelValid()
    _p.repaint()

def recallGraphics():
    '''
    Restores the saved graphics from the image buffer. Use saveGraphics()
    to save it.

    Same as restoreGraphics() (for TigerJython compatibility).
    '''
    restoreGraphics()


def restoreGraphics():
    '''
    Restores the saved graphics from the image buffer. Use saveGraphics()
    to save it.
    '''
    _isGPanelValid()
    _p.restoreGraphics()

def saveGraphics():
    '''
    Saves the current graphics into a image buffer. Use restoreGraphics()
    to restore it.
    '''
    _isGPanelValid()
    _p.saveGraphics()

def setBgColor(*args):
    '''
    Sets the background color. All drawings are erased and the current
    graph cursor is set to (0, 0).
    1 parameter: value considered as X11 color string
    3 parameters: values considered as RGB (alpha = 255)
    4 parameters: values considered as RGBA
    '''
    _isGPanelValid()
    return _p.setBgColor(*args)

def setColor(*args):
    '''
    Sets the current pen color.
    1 parameter: - string value considered as X11 color string
                 - list considered as [r, b, g] or [r, g, b, a]
                 - tuple considered as (r, b, g) or (r, g, b, a)
    3 parameters: values considered as RGB (alpha = 255)
    4 parameters: values considered as RGBA

    Same as setPenColor(). For TigerJython compatiblity.
    '''
    return setPenColor(*args)

def setPaintMode():
    '''
    Resets the drawing mode to standard (overwriting).
    '''
    _isGPanelValid()
    _p.setPaintMode()

def setPenColor(*args):
    '''
    Sets the current pen color.
    1 parameter: - string value considered as X11 color string
                 - list considered as [r, b, g] or [r, g, b, a]
                 - tuple considered as (r, b, g) or (r, g, b, a)
    3 parameters: values considered as RGB (alpha = 255)
    4 parameters: values considered as RGBA
    '''
    _isGPanelValid()
    return _p.setPenColor(*args)

def setPenSize(size):
    '''
    Sets the current pen size (width) (>=1).
    Returns the previouis pen size.
    Same as lineWidth().
    @param width: the pen width (>=1)
    '''
    _isGPanelValid()
    return _p.setPenSize(size)

def setTitle(title):
    '''
    Sets the title in the window title bar.
    @param title: the title text
    '''
    _isGPanelValid()
    return _p.setTitle(size)

def setUserCoords(xmin, xmax, ymin, ymax):
    '''
    Sets user coordinate system left_x, right_x, bottom_y, top_y (inclusive).
    Same as window().

    @param xmin: the x coordinate (of a visible pixel) at left border
    @param xmax: the x coordinate (of a visible pixel) at right border
    @param ymin: the y coordinate (of a visible pixel) at bottom border
    @param ymax: the y coordinate (of a visible pixel) at top border
    '''
    _isGPanelValid()
    _p.setUserCoords(xmin, xmax, ymin, ymax)

def setWindowCenter():
    '''
    Sets the screen position to the center of the screen.
    '''
    _isGPanelValid()
    _p.setWindowCenter()

def setWindowPos(ulx, uly):
    '''
    Sets the screen position of the graphics window.
    @param ulx: the upper left corner's x-coordinate
    @param ulx: the upper left  corner's y-coordinate
    '''
    _isGPanelValid()
    _p.setWindowPos(ulx, uly)

def setXORMode(*args):
    '''
    Performs pixel color XOR operation with the existing background pixel.
    Be aware that if the background is white, drawing with a white pen shows a black pixel.
    (Parameter not used, for TigerJython compatibility)
    '''
    _isGPanelValid()
    _p.setXORMode()


def startPath():
    '''
    Starts recording the path vertexes. The positions of subsequent draw() operations are saved.
    The path is used to show a filled polygon when fillPath() is called.
    '''
    _isGPanelValid()
    _p.startPath()

def storeGraphics():
     '''
     Saves the current graphics into a image buffer. Use restoreGraphics()
     to restore it.

     Same as saveGraphics() (for TigerJython compatibility).
     '''
     saveGraphics()

def text(*args):
    '''
    Draws a text at given position (user coordinates).
    1 parameter: at current graph cursor position
    2 parameters: target point (comolex/list/tuple), text
    3 parameters: x, y, text
    '''
    _isGPanelValid()
    _p.text(*args)

def title(title):
    '''
    Sets the title in the window title bar.
    Same as setTitle(), for TigerJython compatibility.
    @param title: the title text
    '''
    _isGPanelValid()
    _p.setTitle(title)

def toPixel(user):
    '''
    Returns pixel coordinates (tuple) of given user coordinates (tuple).
    '''
    _isGPanelValid()
    return _p.toPixel(user)

def toPixelHeight(userHeight):
    '''
    Returns pixel y-increment of given user y-increment (always positive).
    '''
    _isGPanelValid()
    return p.toPixelHeight(userHeight)

def toPixelWidth(userWidth):
    '''
    Returns pixel x-increment of given user x-increment (always positive).
    '''
    _isGPanelValid()
    return _p.toPixelWidth(userWidth)

def toPixelX(userX):
    '''
    Returns pixel x-coordinate of given user x-coordinate.
    '''
    _isGPanelValid()
    return _p.toPixelX(userX)

def toPixelY(userY):
    '''
    Returns pixel y-coordinate of given user y-coordinate.
    '''
    _isGPanelValid()
    return _p.toPixelY(userY)

def toUser(pixel):
    '''
    Returns user coordinates (tuple) of given pixel coordinates (tuple).
    '''
    _isGPanelValid()
    return _p.toUser(pixel)

def toUserHeight(pixelHeight):
    '''
    Returns user y-increment of given pixel y-increment (always positive).
    '''
    _isGPanelValid()
    return _p.toUserHeight(pixelHeight)

def toUserWidth(pixelWidth):
    '''
    Returns user x-increment of given pixel x-increment (always positive).
    '''
    _isGPanelValid()
    return _p.toUserWidth(pixelWidth)

def toUserX(pixelX):
    '''
    Returns user x-coordinate of given pixel x-coordinate.
    '''
    _isGPanelValid()
    return _p.toUserX(pixelX)

def toUserY(pixelY):
    '''
    Returns user y-coordinate of given pixel y-coordinate.
    '''
    _isGPanelValid()
    return _p.toUserY(pixelY)

def triangle(*args):
    '''
    Draws a triangle with given corners.
    6 parameters: x1, y1, x2, y2, x3, y3 coordinates of corners
    3 parameters: [x1, y1], [x2, y2], [x3, y3] lists of corners
    '''
    _isGPanelValid()
    _p.triangle(*args)

def window(xmin, xmax, ymin, ymax):
    '''
    Sets user coordinate system left_x, right_x, bottom_y, top_y (inclusive).
    Same as setUserCoords(). For TigerJython compatiblity.

    @param xmin: the x coordinate (of a visible pixel) at left border
    @param xmax: the x coordinate (of a visible pixel) at right border
    @param ymin: the y coordinate (of a visible pixel) at bottom border
    @param ymax: the y coordinate (of a visible pixel) at top border
    '''
    _isGPanelValid()
    _p.setUserCoords(xmin, xmax, ymin, ymax)

def windowPosition(ulx, uly):
    '''
    Sets the screen position (pixel coordinates of upper left corner).
    '''
    _isGPanelValid()
    _p.windowPosition(ulx, uly)

def windowCenter():
    '''
    Sets the window to the center of the screen.
    '''
    _isGPanelValid()
    _p.windowCenter()

def _getCoords(*args):
    if len(args) == 2:
        return args[0], args[1]
    elif len(args) == 1:
        if type(args[0]) == complex:
           return args[0].real, args[0].imag
        elif type(args[0]) == list or type(args[0]) == tuple:
            return args[0][0], args[0][1]
        else:
            raise ValueError("Illegal parameter type.")
    else:
        raise ValueError("Illegal number of parameters.")

def _get2Coords(*args):
    if len(args) == 4:
        return args[0], args[1], args[2], args[3]
    elif len(args) == 2:
        val = []
        for arg in args:
            if type(arg) == complex:
                val.append(arg.real)
                val.append(arg.imag)
            elif type(args) == list or type(args) == tuple:
                val.append(arg[0])
                val.append(arg[1])
            else:
                raise ValueError("Illegal parameter type.")
        return val[0], val[1], val[2], val[3]
    else:
        raise ValueError("Illegal number of parameters.")

# ------------------------ end of GPanel methods -----------

def run(f):
    '''
    Calls f() in a new thread.
    '''
    thread.start_new_thread(f, ())


def getRandomX11Color():
    '''
    Returns a random X11 color string.
    '''
    return GPanel.getRandomX11Color()

# Code from: http://code.activestate.com
def linfit(X, Y):
    '''
    Returns a and b in y = a*x + b for given list X of x values and
    corresponding list Y of values.
    '''
    def mean(Xs):
        return sum(Xs) / len(Xs)
    m_X = mean(X)
    m_Y = mean(Y)

    def std(Xs, m):
        normalizer = len(Xs) - 1
        return math.sqrt(sum((pow(x - m, 2) for x in Xs)) / normalizer)

    def pearson_r(Xs, Ys):
        sum_xy = 0
        sum_sq_v_x = 0
        sum_sq_v_y = 0

        for (x, y) in zip(Xs, Ys):
            var_x = x - m_X
            var_y = y - m_Y
            sum_xy += var_x * var_y
            sum_sq_v_x += pow(var_x, 2)
            sum_sq_v_y += pow(var_y, 2)
        return sum_xy / math.sqrt(sum_sq_v_x * sum_sq_v_y)

    r = pearson_r(X, Y)
    b = r * (std(Y, m_Y) / std(X, m_X))
    A = m_Y - b * m_X
    return b, A




# ----------------------------- Size class -------------------------
class Size():
    '''
    Class that defines the pair width, height of dimension attributes.
    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height



# =====================================================================
# ============================= GPanel class ==========================
# =====================================================================
class GPanel(QtGui.QWidget):
    '''
    Class to create a graphics window of default size 501x501 pixels (client drawing area)
    using a coordinate system with x-axis from left to right, y-axis from bottom to top
    (called user coordinates, default range 0..1, 0..1).

    The drawing methods perform drawing operation in an offscreen buffer (QPixmap)
    and automatically renders it on the screen, so the graphics is shown step-by-step.


    The drawing methods perform drawing operation in an offscreen buffer (pixmap)
    and automatically renders it on the screen, so the graphics is shown step-by-step.

    User coordinates:  (ux, uy)
    Pixel coordinates: (px, py) (screen pixels)
    Transformation: px = px(ux), py = py(uy)
    Pixel coordinate range: 0..winWidth - 1 (inclusive), 0..winHeight - 1 (inclusive); (0,0) upper left corner, x to the right, y downwards
    User coordinate range: xmin..xmax (inclusive), ymin..ymax (inclusive); (0,0) lower left corner, x to the right, y upwards.

    Transformation: user(ux, uy) to pixel(px, py):
    (width = winWidth - 1, height = winHeight - 1)
    px = a * ux + b
    py = c * uy + d
    with a = width / (xmax - xmin)
    b = width * xmin / (xmin - xmax)
    c = height / (ymin - ymax)
    d = height * ymax / (ymax - ymin)

    Inverse:
    ux = (px - b) / a
    uy = (py - d) / c

    Because of the transformation from float to pixel coordinates, some rounding errors
    may happen. If you need pixel accuracy, define a GPanel window with some user defined width x height,
    e.g. GPanal(Size(501, 401)). Define then user coordinates in the range 0..width-1, 0..height-1, e.g.
    setUserCoords(0, 500, 0, 400). Now pixels in the range 0..500 x 0..400 (inclusive) may be addressed with no
    rounding errors. (This is a total of 501 x 401 pixels.)

    If you prefer a coordinate system with the origin at the upper left corner, define the y-range in reverse
    order, e.g. setUserCoords(0, 500, 400, 0).

    WARNING: Because PyQt is not thread-safe, in principle all graphics drawings should be
    executed in the GUI thread (for GPanel the main thread or a GUI callback).

    Typical program:

    from pygpanel import *

    p = GPanel(0, 10, 0, 10)
    for ypt in range(0, 11, 1):
        p.line(0, ypt, 10 - ypt, 0)
        time.sleep(0.1) # to see what happens
    p.keep()

    keep() is blocking and keeps the graphics panel open until the close button is hit or the
    Python process terminates.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructs a GPanel and displays a non-resizable graphics window.
        Defaults with no parameter:
        Window size: 501x501 pixels
        Window title: "GPanel"
        User coordinates: 0, 1, 0, 1
        Background color: white
        Pen color: black
        Pen size: 1

        1 Parameter: Size(window_width, window_height)
        4 Parameters: xmin, xmax, ymin, ymax
        @param Size: a Size refererence that defines the width and height of the graphics window.
        '''
        try:
            self._embedded = kwargs['embedded']
        except:
            self._embedded = False
        else:
            if type(self._embedded) != bool:
                self._embedded = False
        if not self._embedded:
            self._app = QtGui.QApplication(sys.argv)
        super(GPanel, self).__init__()
        self.xmin = 0
        self.xmax = 1
        self.ymin = 0
        self.ymax = 1
        self.winWidth = 501
        self.winHeight = 501
        if not (len(args) == 0 or len(args) == 1 or len(args) == 4):
           raise ValueError("Illegal parameter list")
        if len(args) == 1:
            self.winWidth = args[0].width
            self.winHeight = args[0].height
        elif len(args) == 4:
            self.xmin = args[0]
            self.xmax = args[1]
            self.xmax = args[1]
            self.ymin = args[2]
            self.ymax = args[3]
        self._initUI()

    def _initUI(self):
        self._setDefaults()
        self._label = QLabel()
        self._pixmap = QPixmap(QSize(self.winWidth, self.winHeight))
        self._vbox = QVBoxLayout()
        self._vbox.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self._vbox)
        self._painter = QPainter(self._pixmap)
        self.paintEvent(0)
        self.clear()
        if not self._embedded:
            self.show()
            self.setFixedSize(self.winWidth + 2, self.winHeight + 2)

    def _setDefaults(self):
        self.setWindowTitle('GPanel')
        self._penSize = 1
        self._penColor = QColor(0, 0, 0)
        self._bgColor = QColor(255, 255, 255, 255)

        # default pos of GPanel window
        if not self._embedded:
            ulx = 10
            uly = 10
            super(GPanel, self).move(ulx, uly)  # position

        self._xCurrent = 0
        self._yCurrent = 0
        self._enableRepaint = True
        self._adjust()
        self._onMousePressed = None
        self._onMouseReleased = None
        self._onMouseDragged = None
        self._onKeyPressed = None
        self._onKeyReleased = None
        self._isLeftMouseButton = False
        self._isRightMouseButton = False
        self._inMouseMoveCallback = False
        self._closeListener = None
        self._pathHistory = None
        self._savePixmap = None
        self._doRepaint = False

    def clear(self):
        '''
        Clears the graphics window and the offscreen buffer used by the window
        (fully paint with background color).
        Sets the current graph cursor position to (0, 0).
        If enableRepaint(false) only clears the offscreen buffer.
        '''
        self._painter.setPen(QPen(self._bgColor, 1))
        self._painter.fillRect(QRect(0, 0, self.winWidth, self.winHeight), self._bgColor)
        self._painter.setPen(QPen(self._penColor, self._penSize))
        self._xCurrent = 0
        self._yCurrent = 0
        if self._enableRepaint:
            self.repaint()

    def erase(self):
        '''
        Same as clear(), but lets the current graph cursor unganged.
        '''
        self._painter.setPen(QPen(self._bgColor, 1))
        self._painter.fillRect(QRect(0, 0, self.winWidth, self.winHeight), self._bgColor)
        self._painter.setPen(QPen(self._penColor, self._penSize))
        if self._enableRepaint:
            self.repaint()

    def keep(self):
        '''
        Blocks until the title bar's close button is hit. Then cleans up
        the graphics system.
        '''
        self._app.exec_()  # blocking
#        self._painter.end()
#        sys.exit(0)

    def setTitle(self, title):
        '''
        Sets the title in the window title bar.
        @param title: the title text
        '''
        self.setWindowTitle(title)

    # override
    def paintEvent(self, e):
        if self._doRepaint:
            self._label.setPixmap(self._pixmap)
            self._vbox.addWidget(self._label)
            self._doRepaint = False

    def setColor(self, *args):
        '''
        Same as setPenColor()
        '''
        self.setPenColor(*args)
        
        
    def _toRGBA(self, *args):
        if len(args) == 1:
            if type(args[0]) == str:
                try:
                    color = args[0].lower()
                    rgb = x11ColorDict[color]
                except KeyError:
                    raise ValueError("X11 color", args[0], "not found")
                r = rgb[0]
                g = rgb[1]
                b = rgb[2]
                a = 255
            elif type(args[0]) == list or type(args[0]) == tuple:
                if len(args[0]) == 3:
                    r = args[0][0]
                    g = args[0][1]
                    b = args[0][2]
                    a = 255
                elif len(args[0]) == 4:
                    r = args[0][0]
                    g = args[0][1]
                    b = args[0][2]
                    a = args[0][3]
                else:
                    raise ValueError("Illegal parameter list")
            else:
                raise ValueError("Illegal parameter list")

        elif len(args) == 3:
            r = args[0]
            g = args[1]
            b = args[2]
            a = 255

        elif len(args) == 4:
            r = args[0]
            g = args[1]
            b = args[2]
            a = 255

        else:
            raise ValueError("Illegal number of arguments")        

        return r, g, b, a

    def setPenColor(self, *args):
        '''
        Sets the current pen color.
        1 parameter: - string value considered as X11 color string
                     - list considered as [r, b, g] or [r, g, b, a]
                     - tuple considered as (r, b, g) or (r, g, b, a)
        3 parameters: values considered as RGB (alpha = 255)
        4 parameters: values considered as RGBA
        '''
        r, g, b, a = self._toRGBA(*args) 
        self._penColor = QColor(r, g, b, a)
        self._painter.setPen(QPen(self._penColor, self._penSize))

    def setPenSize(self, size):
        '''
        Sets the current pen size (width) (>=1).
        Returns the previous pen size.
        @param width: the pen width >=1)
        '''
        oldPenSize = self._penSize
        self._penSize = size
        self._painter.setPen(QPen(self._penColor, self._penSize))
        return oldPenSize

    # coordinate transformations
    def toPixel(self, user):
        '''
        Returns pixel coordinates (tuple) of given user coordinates (tupel).
        '''
        return self.toPixelX(user[0]), self.toPixelY(user[1])

    def toPixelX(self, userX):
        '''
        Returns pixel x-coordinate of given user x-coordinate.
        '''
        return (int)(self._a * userX + self._b)

    def toPixelY(self, userY):
        '''
        Returns pixel y-coordinate of given user y-coordinate.
        '''
        return (int)(self._c * userY + self._d)

    def toPixelWidth(self, userWidth):
        '''
        Returns pixel x-increment of given user x-increment (always positive).
        '''
        return int(abs(self._a * userWidth))

    def toPixelHeight(self, userHeight):
        '''
        Returns pixel y-increment of given user y-increment (always positive).
        '''
        return int(abs(self._c * userHeight))

    def toUser(self, pixel):
        '''
        Returns user coordinates (tuple) of given pixel coordinates (tuple).
        '''
        return self.toUserX(pixel[0]), self.toUserY(pixel[1])

    def toUserX(self, pixelX):
        '''
        Returns user x-coordinate of given pixel x-coordinate.
        '''
        a = (self.winWidth - 1) / (self.xmax - self.xmin)
        b = (self.winWidth - 1) * self.xmin / (self.xmin - self.xmax)
        return (pixelX - b) / a

    def toUserY(self, pixelY):
        '''
        Returns user y-coordinate of given pixel y-coordinate.
        '''
        c = (self.winHeight - 1)  / (self.ymin - self.ymax)
        d = (self.winHeight - 1) * self.ymax / (self.ymax - self.ymin)
        return (pixelY - d) / c

    def toUserWidth(self, pixelWidth):
        '''
        Returns user x-increment of given pixel x-increment (always positive).
        '''
        a = (self.winWidth - 1) / (self.xmax - self.xmin)
        return abs(pixelWidth / a)

    def toUserHeight(self, pixelHeight):
        '''
        Returns user y-increment of given pixel y-increment (always positive).
        '''
        c = (self.winWidth - 1) / (self._ymin - self._ymax)
        return abs(pixelHeight / c)

    def setUserCoords(self, xmin, xmax, ymin, ymax):
        '''
        Sets user coordinate system left_x, right_x, bottom_y, top_y (inclusive).
        @param xmin: the x coordinate (of a visible pixel) at left border
        @param xmax: the x coordinate (of a visible pixel) at right border
        @param ymin: the y coordinate (of a visible pixel) at bottom border
        @param ymax: the y coordinate (of a visible pixel) at top border
        '''
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self._adjust()

    def _adjust(self):
        self._a = (self.winWidth - 1) / (self.xmax - self.xmin)
        self._b = (self.winWidth - 1)  * self.xmin / (self.xmin - self.xmax)
        self._c = (self.winHeight - 1) / (self.ymin - self.ymax)
        self._d = (self.winHeight - 1) * self.ymax / (self.ymax - self.ymin)

    # end of coordinate transformations

    def repaint(self):
        '''
        Renders the offscreen buffer in the graphics window.
        '''
        self._doRepaint = True
        self.update()
        QApplication.processEvents()

    def enableRepaint(self, enable):
        '''
        Enables/Disables automatic repaint in graphics drawing methods.
        @param enable: if True, the automatic repaint is enabled; otherwise disabled
        '''
        self._enableRepaint = enable

    def line(self, x1, y1, x2, y2):
        '''
        Draws a line with given user start and end coordinates
        and sets the graph cursor position to the end point.
        Also with 2 parameters of type complex, list or tuple.
        4 parameters: x1, y1, x2, y2
        2 parameters: pt1, pt2 as complex/list/tuple
        '''
        xStart = self.toPixelX(x1)
        yStart = self.toPixelY(y1)
        xEnd = self.toPixelX(x2)
        yEnd = self.toPixelY(y2)
        self._painter.drawLine(xStart, yStart, xEnd, yEnd)
        self._xCurrent = x2
        self._yCurrent = y2
        if self._enableRepaint:
            self.repaint()

    def pos(self, x, y):
        '''
        Sets the current graph cursor position to given user coordinates.
        (without drawing anything, same as move()).
        @param x: the x coordinate of the target point
        @param y: the y coordinate of the target point
        @param target: (alternative) the target point as complex, list or tuple
        '''
        self._xCurrent = x
        self._yCurrent = y

    def move(self, x, y):
        # Overrides super.move()
        '''
        Sets the current graph cursor position to given user coordinates.
        (without drawing anything, same as pos()).
        @param x: the x coordinate of the target point
        @param y: the y coordinate of the target point
        @param target: (alternative) the target point as complex, list or tuple
        '''
        self.pos(x, y)

    def draw(self, x, y):
        '''
        Draws a line form current graph cursor position to (x, y).
        Sets the graph cursor position to (x, y).
        @param x: the x coordinate of the target point
        @param y: the y coordinate of the target point
        @param target: (alternative) the target point as complex, list or tuple
        '''
        self.line(self._xCurrent, self._yCurrent, x, y)
        if self._pathHistory != None:
            self._pathHistory.append([x, y])

    def linePlot(self, *args):
        '''
        Draws a line plot with given x,y data.
        1 parameter: a list/tuple of subsequent data points [x, y]
        2 parameters: two lists/tuples x, y of corresponding x-y pairs
        The graph cursor position remains unchanged.
        '''
        nodes = []
        if len(args) == 1:
            for pt in args[0]:
                node = [pt[0], pt[1]]
                nodes.append(node)
        elif len(args) == 2:
            if len(args[0]) != len(args[1]):
               raise ValueError("x and y list/tuple must have equal size")
            for i in range(len(args[0])):
                node = [args[0][i], args[1][i]]
                nodes.append(node)
        else:
            raise ValueError("Illegal number of parameters.")

        for i in range(len(nodes) - 1):
            x1 = self.toPixelX(nodes[i][0])
            y1 = self.toPixelY(nodes[i][1])
            x2 = self.toPixelX(nodes[i + 1][0])
            y2 = self.toPixelY(nodes[i + 1][1])
            self._painter.drawLine(x1, y1, x2, y2)

        if self._enableRepaint:
            self.repaint()

    def getPos():
        '''
        Returns a tuple with current graph cursor position (tuple, user coordinates).
        '''
        return self._xCurrent, self._yCurrent

    def getPosX(self):
        '''
        Returns the current graph cursor x-position (user coordinates).
        '''
        return self._xCurrent

    def getPosY(self):
        '''
        Returns the current graph cursor y-position (user coordinates).
        '''
        return self._yCurrent

    def text(self, *args):
        '''
        Draws a text at given position (user coordinates).
        1 parameter: at current graph cursor position
        2 parameters: target point (comolex/list/tuple), text
        3 parameters: x, y, text
        '''
        if len(args) == 1:
            xPos = self.toPixelX(self._xCurrent)
            yPos = self.toPixelY(self._yCurrent)
            text = args[0]
        elif len(args) == 2:
            xPos, yPos = _getCoords(args[0][:-1])
            text = args[1]
        elif len(args) == 3:
            xPos = self.toPixelX(args[0])
            yPos = self.toPixelY(args[1])
            text = args[2]
        else:
            raise ValueError("Illegal number of arguments")

        self._painter.drawText(xPos, yPos, text)
        if self._enableRepaint:
            self.repaint()

    def addCloseListener(self, closeListener):
        '''
        Registers the given function that is called when the title bar
        close button is hit. If a listener (!= None) is registered,
        the automatic closing is disabled. To close the window, call
        sys.exit().

        KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
        @param closeListener: a callback function called when the close button is hit
        '''
        self._closeListener = closeListener

    def closeEvent(self, e):
        # Override
        if self._closeListener != None:
            e.ignore()
            self._closeListener()

    def setBgColor(self, *args):
        '''
        Sets the background color. All drawings are erased and the current
        graph cursor is set to (0, 0).

        1 parameter: - string value considered as X11 color string
                     - list considered as [r, b, g] or [r, g, b, a]
                     - tuple considered as (r, b, g) or (r, g, b, a)
        3 parameters: values considered as RGB (alpha = 255)
        4 parameters: values considered as RGBA       
        '''
        r, g, b, a = self._toRGBA(*args)
        self._bgColor = QColor(r, g, b, a)
        self.clear()


    def circle(self, radius):
        '''
        Draws a circle with center at the current graph cursor position
        with given radius in horizontal window coordinates.
        @param radius: the radius of the circle
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(radius)
        self._painter.drawEllipse(QPointF(xPix, yPix), rPix, rPix)
        if self._enableRepaint:
            self.repaint()

    def fillCircle(self, radius):
        '''
        Draws a filled circle with center at the current graph cursor position
        with given radius in horizontal window coordinates (fill color = pen color).
        @param radius: the radius of the circle
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(radius)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self._penColor))
        self._painter.drawEllipse(QPointF(xPix, yPix), rPix, rPix)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self._penColor, self._penSize))
        self._painter.setBrush(Qt.NoBrush)


    def ellipse(self, a, b):
        '''
        Draws an ellipse with center at the current graph cursor position
        with given axes.
        @param a: the major ellipse axis
        @param b: the minor ellipse axis
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        aPix = self.toPixelWidth(a)
        bPix = self.toPixelHeight(b)
        self._painter.drawEllipse(QPointF(xPix, yPix), aPix, bPix)
        if self._enableRepaint:
            self.repaint()

    def fillEllipse(self, a, b):
        '''
        Draws a filled ellipse with center at the current graph cursor position
        with given axes (fill color = pen color).
        @param a: the major ellipse axis
        @param b: the minor ellipse axis
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        aPix = self.toPixelWidth(a)
        bPix = self.toPixelHeight(b)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self._penColor))
        self._painter.drawEllipse(QPointF(xPix, yPix), aPix, bPix)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self._penColor, self._penSize))
        self._painter.setBrush(Qt.NoBrush)

    def rectangle(self, *args):
        '''
        Draws a rectangle.
        2 parameters: Center at the current graph cursor position
                      and given width and height.
        4 parameters: Given diagonal
        '''
        if len(args) == 2:
            wPix = self.toPixelWidth(args[0])
            hPix = self.toPixelHeight(args[1])
            ulx = self.toPixelX(self._xCurrent) - wPix // 2
            uly = self.toPixelY(self._yCurrent) - hPix // 2
        elif len(args) == 4:
            wPix = self.toPixelWidth(args[2] - args[0])
            hPix = self.toPixelHeight(args[3] - args[1])
            ulx = self.toPixelX(args[0])
            uly = self.toPixelY(args[1])
        self._painter.drawRect(ulx, uly, wPix, hPix)
        if self._enableRepaint:
            self.repaint()

    def fillRectangle(self, *args):
        '''
        Draws a filled rectangle (fill color = pen color).
        2 parameters: Center at the current graph cursor position
                      and given width and height.
        4 parameters: Given diagonal
        '''
        if len(args) == 2:
            wPix = self.toPixelWidth(args[0])
            hPix = self.toPixelHeight(args[1])
            ulx = self.toPixelX(self._xCurrent) - wPix // 2
            uly = self.toPixelY(self._yCurrent) - hPix // 2
        elif len(args) == 4:
            wPix = self.toPixelWidth(args[2] - args[0])
            hPix = self.toPixelHeight(args[3] - args[1])
            ulx = self.toPixelX(args[0])
            uly = self.toPixelY(args[1])
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self._penColor))
        self._painter.drawRect(ulx, uly, wPix, hPix)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self._penColor, self._penSize))
        self._painter.setBrush(Qt.NoBrush)

    def polygon(self, *args):
        '''
        Draws a polygon with given list of vertexes (list of [x, y] or (x, y))
        (fill color = pen color).
        1 parameter: a list/tuple of the corners [x, y] or (x, y)
        2 parameters: two lists/tuples x, y of corresponding x-y pairs
        '''
        nodes = []
        if len(args) == 1:
            for pt in args[0]:
                node = QPointF(self.toPixelX(pt[0]), self.toPixelY(pt[1]))
                nodes.append(node)
        elif len(args) == 2:
            if len(args[0]) != len(args[1]):
               raise ValueError("x and y list/tuple must have equal size")
            for i in range(len(args[0])):
                node = QPointF(self.toPixelX(args[0][i]), self.toPixelY(args[1][i]))
                nodes.append(node)
        else:
            raise ValueError("Illegal number of parameters.")
        p = QPolygonF(nodes)
        self._painter.drawPolygon(p)
        if self._enableRepaint:
            self.repaint()

    def fillPolygon(self, *args):
        '''
        Draws a filled polygon with given list of vertexes (list of [x, y] or (x, y))
        (fill color = pen color).
        1 parameter: a list/tuple of the corners [x, y] or (x, y)
        2 parameters: two lists/tuples x, y of corresponding x-y pairs
        '''
        nodes = []
        if len(args) == 1:
            for pt in args[0]:
                node = QPointF(self.toPixelX(pt[0]), self.toPixelY(pt[1]))
                nodes.append(node)
        elif len(args) == 2:
            if len(args[0]) != len(args[1]):
               raise ValueError("x and y list/tuple must have equal size")
            for i in range(len(args[0])):
                node = QPointF(self.toPixelX(args[0][i]), self.toPixelY(args[1][i]))
                nodes.append(node)
        else:
            raise ValueError("Illegal number of parameters.")
        p = QPolygonF(nodes)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self._penColor))
        self._painter.drawPolygon(p)
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self._penColor, self._penSize))
        self._painter.setBrush(Qt.NoBrush)

    def triangle(self, *args):
        '''
        Draws a triangle with given corners.
        6 parameters: x1, y1, x2, y2, x3, y3 coordinates of corners
        3 parameters: [x1, y1], [x2, y2], [x3, y3] lists of corners
        '''
        if len(args) == 6: # triangle(x1, y1, x2, y2, x3, y3)
            corners = [[args[0], args[1]], [args[2], args[3]], [args[4], args[5]]]
            self.polygon(corners)
        elif len(args) == 3: # triangle([x1, y1], [x2, y2], [x3, y3])
            corners = [args[0], args[1], args[2]]
            self.polygon(corners)
        else:
            raise ValueError("Illegal number of parameters.")

    def fillTriangle(self, *args):
        '''
        Draws a filled triangle with given corners.
        6 parameters: x1, y1, x2, y2, x3, y3 coordinates of corners
        3 parameters: [x1, y1], [x2, y2], [x3, y3] lists of corners
        '''
        if len(args) == 6: # triangle(x1, y1, x2, y2, x3, y3)
            corners = [[args[0], args[1]], [args[2], args[3]], [args[4], args[5]]]
            self.fillPolygon(corners)
        elif len(args) == 3: # triangle([x1, y1], [x2, y2], [x3, y3])
            corners = [args[0], args[1], args[2]]
            self.fillPolygon(corners)
        else:
            raise ValueError("Illegal number of parameters.")

    def arc(self, r, startAngle, spanAngle):
        '''
        Draws a circle sector with center at the current graph cursor position,
        given radius and given start and span angles.
        @param radius: the radius of the arc
        @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
        @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight)
        self._painter.drawArc(rect, int(16 * startAngle), int(16 * spanAngle))
        if self._enableRepaint:
            self.repaint()

    def fillArc(self, r, startAngle, spanAngle):
        '''
        Draws a filled circle sector with center at the current graph cursor position,
        given radius and given start and span angles.
        @param radius: the radius of the arc
        @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
        @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self._penColor))
        self._painter.drawChord(rect, int(16 * startAngle), int(16 * spanAngle))

        # Draw sector triangle
        xStart = int(xPix + rPix * math.cos(math.radians(startAngle)))
        yStart = int(yPix - rPix * math.sin(math.radians(startAngle)))
        xEnd = int(xPix + rPix * math.cos(math.radians(startAngle + spanAngle)))
        yEnd = int(yPix - rPix * math.sin(math.radians(startAngle + spanAngle)))
        triangle = [[xPix, yPix], [xStart, yStart], [xEnd, yEnd]]
        nodes = []
        for pt in triangle:
            node = QPointF(pt[0], pt[1])
            nodes.append(node)
        p = QPolygonF(nodes)
        self._painter.drawPolygon(p)

        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self._penColor, self._penSize))
        self._painter.setBrush(Qt.NoBrush)

    def chord(self, r, startAngle, spanAngle):
        '''
        Draws a circle chord with center at the current graph cursor position,
        given radius and given start and span angles (in degrees, positive
        counter-clockwise, zero to east).
        @param radius: the radius of the arc
        @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
        @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight)
        self._painter.drawChord(rect, int(16 * startAngle), int(16 * spanAngle))
        if self._enableRepaint:
            self.repaint()

    def fillChord(self, r, startAngle, spanAngle):
        '''
        Draws a filled circle chord with center at the current graph cursor position,
        given radius and given start and span angles (in degrees, positive
        counter-clockwise, zero to east).
        @param radius: the radius of the arc
        @param startAngle: starting angle in degrees, zero to east, positive counter-clockwise
        @param spanAngle: span angle (sector angle) in degrees, positive counter-clockwise
        '''
        xPix = self.toPixelX(self._xCurrent)
        yPix = self.toPixelY(self._yCurrent)
        rPix = self.toPixelWidth(r)
        topLeft = QPoint(xPix - rPix, yPix - rPix)
        bottomRight = QPoint(xPix + rPix, yPix + rPix)
        rect = QRect(topLeft, bottomRight)
        self._painter.setPen(Qt.NoPen)
        self._painter.setBrush(QBrush(self._penColor))
        self._painter.drawChord(rect, int(16 * startAngle), int(16 * spanAngle))
        if self._enableRepaint:
            self.repaint()
        self._painter.setPen(QPen(self._penColor, self._penSize))
        self._painter.setBrush(Qt.NoBrush)

    def startPath(self):
        '''
        Starts recording the path vertexes. The positions of subsequent draw() operations are saved.
        The path is used to show a filled polygon when fillPath() is called.
        '''
        self._pathHistory = [[self._xCurrent, self._yCurrent]]

    def fillPath(self, color):
        '''
        Closes the path started with startPath() and shows a filled polygon from the saved
        draw() positions with given color.
        '''
        if self._pathHistory == None:
            raise Exception("Must call startPath() before fillPath()")
        oldColor = self._penColor
        oldSize = self._penSize
        self.setPenColor(color)
        self.setPenSize(1)
        self.fillPolygon(self._pathHistory)
        self._painter.setPen(QPen(oldColor, oldSize))
        self.polygon(self._pathHistory) # draw outline again
        self._pathHistory = None

    def showImage(self, *args):
        '''
        Draws the picture with given file path or given image at given upper-left coordinates.
        1st parameter: image path (string) or QImage reference
        2nd, 3rd parameters: llx, lly (lower left corner in user coordinates)
        '''
        if type(args[0])== str:
            img = QImage(args[0])
        else:
            img = args[0]
        xPix = self.toPixelX(args[1])
        yPix = self.toPixelY(args[2]) - img.height() + 1 # 1 pixel border
        self._painter.drawImage(xPix, yPix, img)
        if self._enableRepaint:
            self.repaint()

    def point(self, *args):
        '''
        Draws a single point with current pen size and pen color at given user coordinates.
        No params: draws a current graph cursor position
        @param x: the x coordinate of the target point
        @param y: the y coordinate of the target point
        @param target: (alternative) the target point as complex, list or tuple
         '''
        if len(args) == 0:
            xPix = self.toPixelX(self._xCurrent)
            yPix = self.toPixelY(self._yCurrent)
        elif len(args) == 1:
            pt = _getCoords(*args)
            xPix = self.toPixelX(pt[0])
            yPix = self.toPixelY(pt[1])
        elif len(args) == 2:
            xPix = self.toPixelX(args[0])
            yPix = self.toPixelY(args[1])
        else:
            raise ValueError("Illegal number of arguments")
        self._painter.drawPoint(QPointF(xPix, yPix))
        if self._enableRepaint:
            self.repaint()

    def getPixelColor(self, *args):
        '''
        Returns the RGBA color tuple of a pixel with given user coordinates.
        No params: Returns color at current graph cursor position.
        '''
        if len(args) == 0:
            xPix = self.toPixelX(self._xCurrent)
            yPix = self.toPixelY(self._yCurrent)
        elif len(args) == 2:
            xPix = self.toPixelX(args[0])
            yPix = self.toPixelY(args[1])
        else:
            raise ValueError("Illegal number of parameters.")
        img = self._pixmap.toImage()
        c = img.pixel(xPix, yPix)
        return QColor(c).getRgb()  # RGBA
        
    def getPixelColorStr(self, *args):
        '''
        Returns the X11 color string of a pixel with given user coordinates.
        No params: Returns color at current graph cursor position.
        '''
        r, g, b, a = self.getPixelColor(*args)
        for name, rgb in x11ColorDict.items():
            if name[-1] in [str(i) for i in range(10)]:  # skip names with ending number
                continue
            if " " in name:  # skip names with space
                continue
            if "grey" in name:  # skip British gray
                continue
            if rgb == [r, g, b]:
                return name
        raise ValueError("X11 color", [r, g, b], "not found")

    def _toColor(self, color):
        if type(color) == str:
            try:
                color = color.lower()
                color = x11ColorDict[color]
                return color
            except KeyError:
                raise ValueError("X11 color", color, "not found")
        else:
           return color

    def fill(self, x, y, *args):
        '''
        Fills the closed unicolored region with the inner point (x, y) with
        the replacement color (RGB, RGBA or X11 color string).
        The old color is not given, the color of the current (x, y) pixel is taken.
        @param x: the x coordinate of the inner point
        @param y: the y coordinate of the inner point
        @param color: the old color (RGB list/tuple or X11 color string) (may be omitted)
        @param replacementColor: the new color (RGB list/tuple or X11 color string)
        '''
        xPix = self.toPixelX(x)
        yPix = self.toPixelY(y)

        if len(args) == 2:
            color = self._toColor(args[0])
            replacementColor = self._toColor(args[1])
        elif len(args) == 1:
            im = self._pixmap.toImage()
            col= QColor(im.pixel(xPix, yPix))
            color = [col.red(), col.green(), col.blue()]
            replacementColor = self._toColor(args[0])
        else:
            raise ValueError("Illegal number of parameters.")

        img = GPanel.floodFill(self._pixmap, [self.toPixelX(x), self.toPixelY(y)], color, replacementColor)
        self._painter.drawImage(0, 0, img)
        if self._enableRepaint:
            self.repaint()

    def getPainter(self):
        '''
        Returns the QPainter reference used to draw into the offscreen buffer.
        '''
        return self._painter

    def getFullImage(self):
        '''
        Returns the QImage reference of the whole graphics area.
        '''
        return self._pixmap.toImage()

    def drawGrid(self, *args):
        '''
        Draws a coordinate system with annotated axes.
        (You must increase the user coordinate system at least 10% in both directions.)
        drawGrid(x, y): Grid with 10 ticks in range 0..x, 0..y. Label text depends if x, y or int or float
        drawGrid(x, y, color): same with given grid color
        drawGrid(x1, x2, y1, y2): same with given span x1..x2, y1..y2
        drawGrid(x1, x2, y1, y2, color): same with given grid color
        drawGrid(x1, x2, y1, y2, x3, y3): same with given number of ticks x3, y3 in x- and y-direction
        '''
        if len(args) == 2:
            self._drawGrid(0, args[0], 0, args[1], 10, 10, None)
        if len(args) == 3:
            self._drawGrid(0, args[0], 0, args[1], 10, 10, args[2])
        elif len(args) == 4:
            self._drawGrid(args[0], args[1], args[2], args[3], 10, 10, None)
        elif len(args) == 5:
            self._drawGrid(args[0], args[1], args[2], args[3], 10, 10, args[4])
        elif len(args) == 6:
            self._drawGrid(args[0], args[1], args[2], args[3], args[4], args[5], None)
        elif len(args) == 7:
            self._drawGrid(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        else:
            raise ValueError("Illegal number of parameters.")

    def _drawGrid(self, xmin, xmax, ymin, ymax, xticks, yticks, color):
        # Save current cursor and color
        xPos = self.getPosX()
        yPos = self.getPosY()
        if color != None:
            oldColor = self._penColor
            self.setPenColor(color)
        # Horizontal
        for i in range(yticks + 1):
            y = ymin + (ymax - ymin) / float(yticks) * i
            self.line(xmin, y, xmax, y)
            if isinstance(ymin, float) or isinstance(ymax, float):
                self.text(xmin - 0.09 * (xmax - xmin), y, str(y))
            else:
                self.text(xmin - 0.09 * (xmax - xmin), y, str(int(y)))
        # Vertical
        for k in range(xticks + 1):
            x = xmin + (xmax - xmin) / float(xticks) * k
            self.line(x, ymin, x, ymax)
            if isinstance(xmin, float) or isinstance(xmax, float):
                self.text(x, ymin - 0.05 * (ymax - ymin), str(x))
            else:
                self.text(x, ymin - 0.05 * (ymax - ymin), str(int(x)))
        # Restore cursor and color
        self.pos(xPos, yPos)
        if color != None:
            self._penColor = oldColor
            self._painter.setPen(QPen(self._penColor, self._penSize))

    def addMousePressListener(self, onMousePressed):
        '''
        Registers a callback that is invoked when a mouse button is pressed.
        Use isLeftMouseButton() or isRightMouseButton() to check which button used.

        KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
        @param onMousePressed: a callback function called when a mouse button is pressed
        '''
        self._onMousePressed = onMousePressed

    def addMouseReleaseListener(self, onMouseReleased):
        '''
        Registers a callback that is invoked when a mouse button is releases.
        Use isLeftMouseButton() or isRightMouseButton() to check which button used.

        KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
        @param onMouseReleased: a callback function called when a mouse button is released
        '''
        self._onMouseReleased = onMouseReleased

    def addMouseDragListener(self, onMouseDragged):
        '''
        Registers a callback that is invoked when the mouse is moved while a mouse button is pressed (drag).

        KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
        @param onMouseDragged: a callback function called when the moused is dragged
        '''
        self._onMouseDragged = onMouseDragged

    def isLeftMouseButton(self):
        '''
        Returns True, if the last mouse action was performed with the left mouse button.
        '''
        return self._isLeftMouseButton

    def isRightMouseButton(self):
        '''
        Returns True, if the last mouse action was performed with the right mouse button.
        '''
        return self._isRightMouseButton

    def addKeyPressListener(self, onKeyPressed):
        '''
        Registers a callback that is invoked when a key is pressed (and the graphics window has the focus).

        KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
        @param onKeyPressed: a callback function called when a key is pressed
        '''
        self._onKeyPressed = onKeyPressed

    def addKeyReleaseListener(self, onKeyReleased):
        '''
        Registers a callback that is invoked when a key is released (and the graphics window has the focus).

        KEEP IN MIND: To use GUI callbacks, the main program must block in the keep() function.
        @param onKeyReleased: a callback function called when a key is released
        '''
        self._onKeyReleased = onKeyReleased

    def getScreenWidth(self):
        '''
        Returns the screen width in pixels.
        '''
        screen_resolution = self._app.desktop().screenGeometry()
        return screen_resolution.width()

    def getScreenHeight(self):
        '''
        Returns the screen height in pixels.
        '''
        screen_resolution = self._app.desktop().screenGeometry()
        return screen_resolution.height()


    def setWindowCenter(self):
        '''
        Sets the screen position to the center of the screen.
        '''
        frameGm = self.frameGeometry()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        frameGm.moveCenter(centerPoint)
        super(GPanel, self).move(frameGm.topLeft())

    def setWindowPos(self, ulx, uly):
        '''
        Sets the screen position of the graphics window.
        @param ulx: the upper left corner's x-coordinate
        @param ulx: the upper left  corner's y-coordinate
        '''
        super(GPanel, self).move(ulx, uly)

    def saveGraphics(self):
        '''
        Saves the current graphics into a image buffer. Use restoreGraphics()
        to restore it.
        '''
        self._savePixmap = self._pixmap.copy(QRect())

    def restoreGraphics(self):
        '''
        Restores the saved graphics from the image buffer. Use saveGraphics()
        to save it.
        '''
        if self._savePixmap == None:
            raise Exception("Store graphics buffer is empty.")
        img = self._savePixmap.toImage()
        self._painter.drawImage(0, 0, img)
        if self._enableRepaint:
            self.repaint()

    def setXORMode(self, *args):
        '''
        Performs pixel color XOR operation with the existing background pixel.
        Be aware that if the background is white, drawing with a white pen shows a black pixel.
        (Parameter not used, for TigerJython compatibility)
        '''
        self._painter.setCompositionMode(QPainter.RasterOp_SourceXorDestination)


    def setPaintMode(self):
        '''
        Resets the drawing mode to standard (overwriting).
        '''
        self._painter.setCompositionMode(QPainter.CompositionMode_SourceOver)

    def windowPosition(self, ulx, uly):
        '''
        Sets the screen position (pixel coordinates of upper left corner).
        '''
        super(GPanel, self).move(ulx, uly)
        
    def windowCenter(self):
        '''
        Sets the window to the center of the screen.
        '''
        xc, yc = GPanel.getScreenCenter()
        self.windowPosition(xc - self.winWidth // 2, yc - self.winHeight // 2) 
        

    # ------------- Mouse events ----------------------------
    def mousePressEvent(self, e):
        pos = QPoint(e.pos())
        self._isLeftMouseButton = (e.button() == Qt.LeftButton)
        self._isRightMouseButton = (e.button() == Qt.RightButton)
        if self._onMousePressed != None:
            self._onMousePressed(self.toUserX(pos.x()), self.toUserY(pos.y()))

    def mouseReleaseEvent(self, e):
        pos = QPoint(e.pos())
        self._isLeftMouseButton = (e.button() == Qt.LeftButton)
        self._isRightMouseButton = (e.button() != Qt.RightButton)
        if self._onMouseReleased != None:
            self._onMouseReleased(self.toUserX(pos.x()), self.toUserY(pos.y()))

    def mouseMoveEvent(self, e):
        # reject reentrance
        if self._inMouseMoveCallback:
            return
        self._inMouseMoveCallback = True
        pos = QPoint(e.pos())
        if self._onMouseDragged != None:
            self._onMouseDragged(self.toUserX(pos.x()), self.toUserY(pos.y()))
        self._inMouseMoveCallback = False

    # ------------- Key events ---------------------------
    def keyPressEvent(self, e):
        key = e.key()
        if self._onKeyPressed != None:
            self._onKeyPressed(key)

    def keyReleaseEvent(self, e):
        key = e.key()
        if self._onKeyReleased != None:
            self._onKeyReleased(key)

# ------------- static methods -------------------------------
    @staticmethod
    def loadImage(filename, pic_format = None):
        '''
        Returns a QImage of the picture loaded from the given file. For pic_format = None,
        the picture format is guessed from the file data.
        @param: the file path to the picture file
        @param pic_format: format of picture, supported:  "None" (default), "GIF", "JPG",
        "BMP", "PNG", "PBM", "PGM", "PPM", "TIFF", "XBM" "XPM".
        '''
        img = QImage(filename, pic_format)
        return img

    @staticmethod
    def getPixelColorImg(image, xPix, yPix):
        '''
        Returns a tuple with the RGBA values at given pixel position (pixel coordinates).
        @param image: the QImage reference
        @param xPix: the pixel x-coordinate
        @param yPix: the pixel y-coordinate
        '''
        c = image.pixel(xPix, yPix)
        return QColor(c).getRgb()  # RGBA

    @staticmethod
    def scale(image, scaleFactor):
        '''
        Returns a new QImage of the scaled picture of the given QImage.
        @param image: the original QImage reference
        @param scaleFactor: the scale factor
        '''
        width = int(image.width() * scaleFactor)
        img = image.scaledToWidth(width)
        return img

    @staticmethod
    def crop(image, x1, y1, x2, y2):
        '''
        Returns a QImage of the sub-area of the given QImage.
        @param image: the given QImage reference
        @param xPix: the pixel ulx-coordinate
        @param yPix: the pixel uly-coordinate
        '''
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        img = image.copy(x1, y1, width, height)
        return img

    @staticmethod
    def getDividingPoint(x1, y1, x2, y2, ratio):
        '''
        Returns the tuple of user coordinates of the point on the line through the point pt1 = (x1, y1)
        and the point pt2 = (x2, y2) that is in distance ratio times the length from pt1 to pt2 from
        pt1. For ratio < 0 the point is in the opposite direction.
        3 parameteters: pt1, pt2 (complex/list/tuple), ratio
        5 parameteters: x1, y1, x2, y2, ratio
        '''
        v1 = (x1, y1)
        v2 = (x2, y2)
        dv = (v2[0] - v1[0], v2[1] - v1[1])  # = v2 - v1
        v = (v1[0] + ratio * dv[0], v1[1] + ratio * dv[1]) # v1 + ratio * dv
        return v[0], v[1]

    @staticmethod
    def floodFill(pm, pt, oldColor, newColor):
        # Implementation from Hardik Gajjar of algorithm
        # at http://en.wikipedia.org/wiki/Flood_fill
        '''
        Fills a bounded single-colored region with
        the given color. The given point is part of the region and used
        to specify it.
        @param pm the pixmap containing the connected region
        @param pt a point inside the region
        @param oldColor the old color of the region (RGB list/tuple)
        @param newColor the new color of the region (RGB list/tuple)
        @return a new qImage with the transformed region
        '''
        image = pm.toImage()
        oldColor = QColor(oldColor[0], oldColor[1], oldColor[2]).rgb()
        newColor = QColor(newColor[0], newColor[1], newColor[2]).rgb()
        q = [pt]

        # Perform filling operation
        while len(q) > 0:
            n = q.pop(0)
            if QColor(image.pixel(n[0], n[1])).rgb() != oldColor:
                continue

            w = n
            e = [n[0] + 1, n[1]]
            while w[0] > 0 and QColor(image.pixel(w[0], w[1])).rgb() == oldColor:
                image.setPixel(w[0], w[1], newColor)
                if w[1] > 0 and QColor(image.pixel(w[0], w[1] - 1)).rgb() == oldColor:
                    q.append([w[0], w[1] - 1])
                if w[1] < image.height() - 1 and QColor(image.pixel(w[0], w[1] + 1)).rgb() == oldColor:
                    q.append([w[0], w[1] + 1])
                w[0] -= 1

            while e[0] < image.width() - 1 and QColor(image.pixel(e[0], e[1])).rgb() == oldColor:
                image.setPixel(e[0], e[1], newColor)
                if e[1] > 0 and QColor(image.pixel(e[0], e[1] - 1)).rgb() == oldColor:
                    q.append([e[0], e[1] - 1])
                if e[1] < image.height() - 1 and QColor(image.pixel(e[0], e[1] + 1)).rgb() == oldColor:
                    q.append([e[0], e[1] + 1])
                e[0] += 1
        return image

    @staticmethod
    def getRandomX11Color():
        '''
        Returns a random X11 color string.
        '''
        r = random.randint(0, 540)
        c = x11ColorDict.keys()
        return c[r]

    @staticmethod
    def getScreenCenter():
        '''
        Returns x, y coordinates tuple of the screen's center point.
        '''
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        return centerPoint.x(), centerPoint.y()

# ----------------------------- GPane class -------------------------
'''
Subclass of GPanel to be used as embedded QWidget in a GUI dialog (QDialog).
'''
class GPane(GPanel):

    def __init__(self, *args, **kwargs):
        '''
        Creates a GPanel with no application window.
        '''
        super(GPane, self).__init__(*args, embedded = True)


# ----------------------------- Useful constants -------------------------
'''
X11 to RGB color mapping
'''
x11ColorDict = {
"aqua":[0, 255, 255],
"cornflower":[100, 149, 237],
"crimson":[220, 20, 60],
"fuchsia":[255, 0, 255],
"indigo":[75, 0, 130],
"lime":[50, 205, 50],
"silver":[192, 192, 192],
"ghost white":[248, 248, 255],
"snow":[255, 250, 250],
"ghostwhite":[248, 248, 255],
"white smoke":[245, 245, 245],
"whitesmoke":[245, 245, 245],
"gainsboro":[220, 220, 220],
"floral white":[255, 250, 240],
"floralwhite":[255, 250, 240],
"old lace":[253, 245, 230],
"oldlace":[253, 245, 230],
"linen":[250, 240, 230],
"antique white":[250, 235, 215],
"antiquewhite":[250, 235, 215],
"papaya whip":[255, 239, 213],
"papayawhip":[255, 239, 213],
"blanched almond":[255, 235, 205],
"blanchedalmond":[255, 235, 205],
"bisque":[255, 228, 196],
"peach puff":[255, 218, 185],
"peachpuff":[255, 218, 185],
"navajo white":[255, 222, 173],
"navajowhite":[255, 222, 173],
"moccasin":[255, 228, 181],
"cornsilk":[255, 248, 220],
"ivory":[255, 255, 240],
"lemon chiffon":[255, 250, 205],
"lemonchiffon":[255, 250, 205],
"seashell":[255, 245, 238],
"honeydew":[240, 255, 240],
"mint cream":[245, 255, 250],
"mintcream":[245, 255, 250],
"azure":[240, 255, 255],
"alice blue":[240, 248, 255],
"aliceblue":[240, 248, 255],
"lavender":[230, 230, 250],
"lavender blush":[255, 240, 245],
"lavenderblush":[255, 240, 245],
"misty rose":[255, 228, 225],
"mistyrose":[255, 228, 225],
"white":[255, 255, 255],
"black":[0, 0, 0],
"dark slate gray":[47, 79, 79],
"darkslategray":[47, 79, 79],
"dark slate grey":[47, 79, 79],
"darkslategrey":[47, 79, 79],
"dim gray":[105, 105, 105],
"dimgray":[105, 105, 105],
"dim grey":[105, 105, 105],
"dimgrey":[105, 105, 105],
"slate gray":[112, 128, 144],
"slategray":[112, 128, 144],
"slate grey":[112, 128, 144],
"slategrey":[112, 128, 144],
"light slate gray":[119, 136, 153],
"lightslategray":[119, 136, 153],
"light slate grey":[119, 136, 153],
"lightslategrey":[119, 136, 153],
"gray":[190, 190, 190],
"grey":[190, 190, 190],
"light grey":[211, 211, 211],
"lightgrey":[211, 211, 211],
"light gray":[211, 211, 211],
"lightgray":[211, 211, 211],
"midnight blue":[25, 25, 112],
"midnightblue":[25, 25, 112],
"navy":[0, 0, 128],
"navy blue":[0, 0, 128],
"navyblue":[0, 0, 128],
"cornflower blue":[100, 149, 237],
"cornflowerblue":[100, 149, 237],
"dark slate blue":[72, 61, 139],
"darkslateblue":[72, 61, 139],
"slate blue":[106, 90, 205],
"slateblue":[106, 90, 205],
"medium slate blue":[123, 104, 238],
"mediumslateblue":[123, 104, 238],
"light slate blue":[132, 112, 255],
"lightslateblue":[132, 112, 255],
"medium blue":[0, 0, 205],
"mediumblue":[0, 0, 205],
"royal blue":[65, 105, 225],
"royalblue":[65, 105, 225],
"blue":[0, 0, 255],
"dodger blue":[30, 144, 255],
"dodgerblue":[30, 144, 255],
"deep sky blue":[0, 191, 255],
"deepskyblue":[0, 191, 255],
"sky blue":[135, 206, 235],
"skyblue":[135, 206, 235],
"light sky blue":[135, 206, 250],
"lightskyblue":[135, 206, 250],
"steel blue":[70, 130, 180],
"steelblue":[70, 130, 180],
"light steel blue":[176, 196, 222],
"lightsteelblue":[176, 196, 222],
"light blue":[173, 216, 230],
"lightblue":[173, 216, 230],
"powder blue":[176, 224, 230],
"powderblue":[176, 224, 230],
"pale turquoise":[175, 238, 238],
"paleturquoise":[175, 238, 238],
"dark turquoise":[0, 206, 209],
"darkturquoise":[0, 206, 209],
"medium turquoise":[72, 209, 204],
"mediumturquoise":[72, 209, 204],
"turquoise":[64, 224, 208],
"cyan":[0, 255, 255],
"light cyan":[224, 255, 255],
"lightcyan":[224, 255, 255],
"cadet blue":[95, 158, 160],
"cadetblue":[95, 158, 160],
"medium aquamarine":[102, 205, 170],
"mediumaquamarine":[102, 205, 170],
"aquamarine":[127, 255, 212],
"dark green":[0, 100, 0],
"darkgreen":[0, 100, 0],
"dark olive green":[85, 107, 47],
"darkolivegreen":[85, 107, 47],
"dark sea green":[143, 188, 143],
"darkseagreen":[143, 188, 143],
"sea green":[46, 139, 87],
"seagreen":[46, 139, 87],
"medium sea green":[60, 179, 113],
"mediumseagreen":[60, 179, 113],
"light sea green":[32, 178, 170],
"lightseagreen":[32, 178, 170],
"pale green":[152, 251, 152],
"palegreen":[152, 251, 152],
"spring green":[0, 255, 127],
"springgreen":[0, 255, 127],
"lawn green":[124, 252, 0],
"lawngreen":[124, 252, 0],
"green":[0, 255, 0],
"chartreuse":[127, 255, 0],
"medium spring green":[0, 250, 154],
"mediumspringgreen":[0, 250, 154],
"green yellow":[173, 255, 47],
"greenyellow":[173, 255, 47],
"lime green":[50, 205, 50],
"limegreen":[50, 205, 50],
"yellow green":[154, 205, 50],
"yellowgreen":[154, 205, 50],
"forest green":[34, 139, 34],
"forestgreen":[34, 139, 34],
"olive drab":[107, 142, 35],
"olivedrab":[107, 142, 35],
"dark khaki":[189, 183, 107],
"darkkhaki":[189, 183, 107],
"khaki":[240, 230, 140],
"pale goldenrod":[238, 232, 170],
"palegoldenrod":[238, 232, 170],
"light goldenrod yellow":[250, 250, 210],
"lightgoldenrodyellow":[250, 250, 210],
"light yellow":[255, 255, 224],
"lightyellow":[255, 255, 224],
"yellow":[255, 255, 0],
"gold":[255, 215, 0],
"light goldenrod":[238, 221, 130],
"lightgoldenrod":[238, 221, 130],
"goldenrod":[218, 165, 32],
"dark goldenrod":[184, 134, 11],
"darkgoldenrod":[184, 134, 11],
"rosy brown":[188, 143, 143],
"rosybrown":[188, 143, 143],
"indian red":[205, 92, 92],
"indianred":[205, 92, 92],
"saddle brown":[139, 69, 19],
"saddlebrown":[139, 69, 19],
"sienna":[160, 82, 45],
"peru":[205, 133, 63],
"burlywood":[222, 184, 135],
"beige":[245, 245, 220],
"wheat":[245, 222, 179],
"sandy brown":[244, 164, 96],
"sandybrown":[244, 164, 96],
"tan":[210, 180, 140],
"chocolate":[210, 105, 30],
"firebrick":[178, 34, 34],
"brown":[165, 42, 42],
"dark salmon":[233, 150, 122],
"darksalmon":[233, 150, 122],
"salmon":[250, 128, 114],
"light salmon":[255, 160, 122],
"lightsalmon":[255, 160, 122],
"orange":[255, 165, 0],
"dark orange":[255, 140, 0],
"darkorange":[255, 140, 0],
"coral":[255, 127, 80],
"light coral":[240, 128, 128],
"lightcoral":[240, 128, 128],
"tomato":[255, 99, 71],
"orange red":[255, 69, 0],
"orangered":[255, 69, 0],
"red":[255, 0, 0],
"hot pink":[255, 105, 180],
"hotpink":[255, 105, 180],
"deep pink":[255, 20, 147],
"deeppink":[255, 20, 147],
"pink":[255, 192, 203],
"light pink":[255, 182, 193],
"lightpink":[255, 182, 193],
"pale violet red":[219, 112, 147],
"palevioletred":[219, 112, 147],
"maroon":[176, 48, 96],
"medium violet red":[199, 21, 133],
"mediumvioletred":[199, 21, 133],
"violet red":[208, 32, 144],
"violetred":[208, 32, 144],
"magenta":[255, 0, 255],
"violet":[238, 130, 238],
"plum":[221, 160, 221],
"orchid":[218, 112, 214],
"medium orchid":[186, 85, 211],
"mediumorchid":[186, 85, 211],
"dark orchid":[153, 50, 204],
"darkorchid":[153, 50, 204],
"dark violet":[148, 0, 211],
"darkviolet":[148, 0, 211],
"blue violet":[138, 43, 226],
"blueviolet":[138, 43, 226],
"purple":[160, 32, 240],
"medium purple":[147, 112, 219],
"mediumpurple":[147, 112, 219],
"thistle":[216, 191, 216],
"snow1":[255, 250, 250],
"snow2":[238, 233, 233],
"snow3":[205, 201, 201],
"snow4":[139, 137, 137],
"seashell1":[255, 245, 238],
"seashell2":[238, 229, 222],
"seashell3":[205, 197, 191],
"seashell4":[139, 134, 130],
"antiquewhite1":[255, 239, 219],
"antiquewhite2":[238, 223, 204],
"antiquewhite3":[205, 192, 176],
"antiquewhite4":[139, 131, 120],
"bisque1":[255, 228, 196],
"bisque2":[238, 213, 183],
"bisque3":[205, 183, 158],
"bisque4":[139, 125, 107],
"peachpuff1":[255, 218, 185],
"peachpuff2":[238, 203, 173],
"peachpuff3":[205, 175, 149],
"peachpuff4":[139, 119, 101],
"navajowhite1":[255, 222, 173],
"navajowhite2":[238, 207, 161],
"navajowhite3":[205, 179, 139],
"navajowhite4":[139, 121, 94],
"lemonchiffon1":[255, 250, 205],
"lemonchiffon2":[238, 233, 191],
"lemonchiffon3":[205, 201, 165],
"lemonchiffon4":[139, 137, 112],
"cornsilk1":[255, 248, 220],
"cornsilk2":[238, 232, 205],
"cornsilk3":[205, 200, 177],
"cornsilk4":[139, 136, 120],
"ivory1":[255, 255, 240],
"ivory2":[238, 238, 224],
"ivory3":[205, 205, 193],
"ivory4":[139, 139, 131],
"honeydew1":[240, 255, 240],
"honeydew2":[224, 238, 224],
"honeydew3":[193, 205, 193],
"honeydew4":[131, 139, 131],
"lavenderblush1":[255, 240, 245],
"lavenderblush2":[238, 224, 229],
"lavenderblush3":[205, 193, 197],
"lavenderblush4":[139, 131, 134],
"mistyrose1":[255, 228, 225],
"mistyrose2":[238, 213, 210],
"mistyrose3":[205, 183, 181],
"mistyrose4":[139, 125, 123],
"azure1":[240, 255, 255],
"azure2":[224, 238, 238],
"azure3":[193, 205, 205],
"azure4":[131, 139, 139],
"slateblue1":[131, 111, 255],
"slateblue2":[122, 103, 238],
"slateblue3":[105, 89, 205],
"slateblue4":[71, 60, 139],
"royalblue1":[72, 118, 255],
"royalblue2":[67, 110, 238],
"royalblue3":[58, 95, 205],
"royalblue4":[39, 64, 139],
"blue1":[0, 0, 255],
"blue2":[0, 0, 238],
"blue3":[0, 0, 205],
"blue4":[0, 0, 139],
"dodgerblue1":[30, 144, 255],
"dodgerblue2":[28, 134, 238],
"dodgerblue3":[24, 116, 205],
"dodgerblue4":[16, 78, 139],
"steelblue1":[99, 184, 255],
"steelblue2":[92, 172, 238],
"steelblue3":[79, 148, 205],
"steelblue4":[54, 100, 139],
"deepskyblue1":[0, 191, 255],
"deepskyblue2":[0, 178, 238],
"deepskyblue3":[0, 154, 205],
"deepskyblue4":[0, 104, 139],
"skyblue1":[135, 206, 255],
"skyblue2":[126, 192, 238],
"skyblue3":[108, 166, 205],
"skyblue4":[74, 112, 139],
"lightskyblue1":[176, 226, 255],
"lightskyblue2":[164, 211, 238],
"lightskyblue3":[141, 182, 205],
"lightskyblue4":[96, 123, 139],
"slategray1":[198, 226, 255],
"slategray2":[185, 211, 238],
"slategray3":[159, 182, 205],
"slategray4":[108, 123, 139],
"lightsteelblue1":[202, 225, 255],
"lightsteelblue2":[188, 210, 238],
"lightsteelblue3":[162, 181, 205],
"lightsteelblue4":[110, 123, 139],
"lightblue1":[191, 239, 255],
"lightblue2":[178, 223, 238],
"lightblue3":[154, 192, 205],
"lightblue4":[104, 131, 139],
"lightcyan1":[224, 255, 255],
"lightcyan2":[209, 238, 238],
"lightcyan3":[180, 205, 205],
"lightcyan4":[122, 139, 139],
"paleturquoise1":[187, 255, 255],
"paleturquoise2":[174, 238, 238],
"paleturquoise3":[150, 205, 205],
"paleturquoise4":[102, 139, 139],
"cadetblue1":[152, 245, 255],
"cadetblue2":[142, 229, 238],
"cadetblue3":[122, 197, 205],
"cadetblue4":[83, 134, 139],
"turquoise1":[0, 245, 255],
"turquoise2":[0, 229, 238],
"turquoise3":[0, 197, 205],
"turquoise4":[0, 134, 139],
"cyan1":[0, 255, 255],
"cyan2":[0, 238, 238],
"cyan3":[0, 205, 205],
"cyan4":[0, 139, 139],
"darkslategray1":[151, 255, 255],
"darkslategray2":[141, 238, 238],
"darkslategray3":[121, 205, 205],
"darkslategray4":[82, 139, 139],
"aquamarine1":[127, 255, 212],
"aquamarine2":[118, 238, 198],
"aquamarine3":[102, 205, 170],
"aquamarine4":[69, 139, 116],
"darkseagreen1":[193, 255, 193],
"darkseagreen2":[180, 238, 180],
"darkseagreen3":[155, 205, 155],
"darkseagreen4":[105, 139, 105],
"seagreen1":[84, 255, 159],
"seagreen2":[78, 238, 148],
"seagreen3":[67, 205, 128],
"seagreen4":[46, 139, 87],
"palegreen1":[154, 255, 154],
"palegreen2":[144, 238, 144],
"palegreen3":[124, 205, 124],
"palegreen4":[84, 139, 84],
"springgreen1":[0, 255, 127],
"springgreen2":[0, 238, 118],
"springgreen3":[0, 205, 102],
"springgreen4":[0, 139, 69],
"green1":[0, 255, 0],
"green2":[0, 238, 0],
"green3":[0, 205, 0],
"green4":[0, 139, 0],
"chartreuse1":[127, 255, 0],
"chartreuse2":[118, 238, 0],
"chartreuse3":[102, 205, 0],
"chartreuse4":[69, 139, 0],
"olivedrab1":[192, 255, 62],
"olivedrab2":[179, 238, 58],
"olivedrab3":[154, 205, 50],
"olivedrab4":[105, 139, 34],
"darkolivegreen1":[202, 255, 112],
"darkolivegreen2":[188, 238, 104],
"darkolivegreen3":[162, 205, 90],
"darkolivegreen4":[110, 139, 61],
"khaki1":[255, 246, 143],
"khaki2":[238, 230, 133],
"khaki3":[205, 198, 115],
"khaki4":[139, 134, 78],
"lightgoldenrod1":[255, 236, 139],
"lightgoldenrod2":[238, 220, 130],
"lightgoldenrod3":[205, 190, 112],
"lightgoldenrod4":[139, 129, 76],
"lightyellow1":[255, 255, 224],
"lightyellow2":[238, 238, 209],
"lightyellow3":[205, 205, 180],
"lightyellow4":[139, 139, 122],
"yellow1":[255, 255, 0],
"yellow2":[238, 238, 0],
"yellow3":[205, 205, 0],
"yellow4":[139, 139, 0],
"gold1":[255, 215, 0],
"gold2":[238, 201, 0],
"gold3":[205, 173, 0],
"gold4":[139, 117, 0],
"goldenrod1":[255, 193, 37],
"goldenrod2":[238, 180, 34],
"goldenrod3":[205, 155, 29],
"goldenrod4":[139, 105, 20],
"darkgoldenrod1":[255, 185, 15],
"darkgoldenrod2":[238, 173, 14],
"darkgoldenrod3":[205, 149, 12],
"darkgoldenrod4":[139, 101, 8],
"rosybrown1":[255, 193, 193],
"rosybrown2":[238, 180, 180],
"rosybrown3":[205, 155, 155],
"rosybrown4":[139, 105, 105],
"indianred1":[255, 106, 106],
"indianred2":[238, 99, 99],
"indianred3":[205, 85, 85],
"indianred4":[139, 58, 58],
"sienna1":[255, 130, 71],
"sienna2":[238, 121, 66],
"sienna3":[205, 104, 57],
"sienna4":[139, 71, 38],
"burlywood1":[255, 211, 155],
"burlywood2":[238, 197, 145],
"burlywood3":[205, 170, 125],
"burlywood4":[139, 115, 85],
"wheat1":[255, 231, 186],
"wheat2":[238, 216, 174],
"wheat3":[205, 186, 150],
"wheat4":[139, 126, 102],
"tan1":[255, 165, 79],
"tan2":[238, 154, 73],
"tan3":[205, 133, 63],
"tan4":[139, 90, 43],
"chocolate1":[255, 127, 36],
"chocolate2":[238, 118, 33],
"chocolate3":[205, 102, 29],
"chocolate4":[139, 69, 19],
"firebrick1":[255, 48, 48],
"firebrick2":[238, 44, 44],
"firebrick3":[205, 38, 38],
"firebrick4":[139, 26, 26],
"brown1":[255, 64, 64],
"brown2":[238, 59, 59],
"brown3":[205, 51, 51],
"brown4":[139, 35, 35],
"salmon1":[255, 140, 105],
"salmon2":[238, 130, 98],
"salmon3":[205, 112, 84],
"salmon4":[139, 76, 57],
"lightsalmon1":[255, 160, 122],
"lightsalmon2":[238, 149, 114],
"lightsalmon3":[205, 129, 98],
"lightsalmon4":[139, 87, 66],
"orange1":[255, 165, 0],
"orange2":[238, 154, 0],
"orange3":[205, 133, 0],
"orange4":[139, 90, 0],
"darkorange1":[255, 127, 0],
"darkorange2":[238, 118, 0],
"darkorange3":[205, 102, 0],
"darkorange4":[139, 69, 0],
"coral1":[255, 114, 86],
"coral2":[238, 106, 80],
"coral3":[205, 91, 69],
"coral4":[139, 62, 47],
"tomato1":[255, 99, 71],
"tomato2":[238, 92, 66],
"tomato3":[205, 79, 57],
"tomato4":[139, 54, 38],
"orangered1":[255, 69, 0],
"orangered2":[238, 64, 0],
"orangered3":[205, 55, 0],
"orangered4":[139, 37, 0],
"red1":[255, 0, 0],
"red2":[238, 0, 0],
"red3":[205, 0, 0],
"red4":[139, 0, 0],
"deeppink1":[255, 20, 147],
"deeppink2":[238, 18, 137],
"deeppink3":[205, 16, 118],
"deeppink4":[139, 10, 80],
"hotpink1":[255, 110, 180],
"hotpink2":[238, 106, 167],
"hotpink3":[205, 96, 144],
"hotpink4":[139, 58, 98],
"pink1":[255, 181, 197],
"pink2":[238, 169, 184],
"pink3":[205, 145, 158],
"pink4":[139, 99, 108],
"lightpink1":[255, 174, 185],
"lightpink2":[238, 162, 173],
"lightpink3":[205, 140, 149],
"lightpink4":[139, 95, 101],
"palevioletred1":[255, 130, 171],
"palevioletred2":[238, 121, 159],
"palevioletred3":[205, 104, 137],
"palevioletred4":[139, 71, 93],
"maroon1":[255, 52, 179],
"maroon2":[238, 48, 167],
"maroon3":[205, 41, 144],
"maroon4":[139, 28, 98],
"violetred1":[255, 62, 150],
"violetred2":[238, 58, 140],
"violetred3":[205, 50, 120],
"violetred4":[139, 34, 82],
"magenta1":[255, 0, 255],
"magenta2":[238, 0, 238],
"magenta3":[205, 0, 205],
"magenta4":[139, 0, 139],
"orchid1":[255, 131, 250],
"orchid2":[238, 122, 233],
"orchid3":[205, 105, 201],
"orchid4":[139, 71, 137],
"plum1":[255, 187, 255],
"plum2":[238, 174, 238],
"plum3":[205, 150, 205],
"plum4":[139, 102, 139],
"mediumorchid1":[224, 102, 255],
"mediumorchid2":[209, 95, 238],
"mediumorchid3":[180, 82, 205],
"mediumorchid4":[122, 55, 139],
"darkorchid1":[191, 62, 255],
"darkorchid2":[178, 58, 238],
"darkorchid3":[154, 50, 205],
"darkorchid4":[104, 34, 139],
"purple1":[155, 48, 255],
"purple2":[145, 44, 238],
"purple3":[125, 38, 205],
"purple4":[85, 26, 139],
"mediumpurple1":[171, 130, 255],
"mediumpurple2":[159, 121, 238],
"mediumpurple3":[137, 104, 205],
"mediumpurple4":[93, 71, 139],
"thistle1":[255, 225, 255],
"thistle2":[238, 210, 238],
"thistle3":[205, 181, 205],
"thistle4":[139, 123, 139],
"gray0":[0, 0, 0],
"grey0":[0, 0, 0],
"gray1":[3, 3, 3],
"grey1":[3, 3, 3],
"gray2":[5, 5, 5],
"grey2":[5, 5, 5],
"gray3":[8, 8, 8],
"grey3":[8, 8, 8],
"gray4":[10, 10, 10],
"grey4":[10, 10, 10],
"gray5":[13, 13, 13],
"grey5":[13, 13, 13],
"gray6":[15, 15, 15],
"grey6":[15, 15, 15],
"gray7":[18, 18, 18],
"grey7":[18, 18, 18],
"gray8":[20, 20, 20],
"grey8":[20, 20, 20],
"gray9":[23, 23, 23],
"grey9":[23, 23, 23],
"gray10":[26, 26, 26],
"grey10":[26, 26, 26],
"gray11":[28, 28, 28],
"grey11":[28, 28, 28],
"gray12":[31, 31, 31],
"grey12":[31, 31, 31],
"gray13":[33, 33, 33],
"grey13":[33, 33, 33],
"gray14":[36, 36, 36],
"grey14":[36, 36, 36],
"gray15":[38, 38, 38],
"grey15":[38, 38, 38],
"gray16":[41, 41, 41],
"grey16":[41, 41, 41],
"gray17":[43, 43, 43],
"grey17":[43, 43, 43],
"gray18":[46, 46, 46],
"grey18":[46, 46, 46],
"gray19":[48, 48, 48],
"grey19":[48, 48, 48],
"gray20":[51, 51, 51],
"grey20":[51, 51, 51],
"gray21":[54, 54, 54],
"grey21":[54, 54, 54],
"gray22":[56, 56, 56],
"grey22":[56, 56, 56],
"gray23":[59, 59, 59],
"grey23":[59, 59, 59],
"gray24":[61, 61, 61],
"grey24":[61, 61, 61],
"gray25":[64, 64, 64],
"grey25":[64, 64, 64],
"gray26":[66, 66, 66],
"grey26":[66, 66, 66],
"gray27":[69, 69, 69],
"grey27":[69, 69, 69],
"gray28":[71, 71, 71],
"grey28":[71, 71, 71],
"gray29":[74, 74, 74],
"grey29":[74, 74, 74],
"gray30":[77, 77, 77],
"grey30":[77, 77, 77],
"gray31":[79, 79, 79],
"grey31":[79, 79, 79],
"gray32":[82, 82, 82],
"grey32":[82, 82, 82],
"gray33":[84, 84, 84],
"grey33":[84, 84, 84],
"gray34":[87, 87, 87],
"grey34":[87, 87, 87],
"gray35":[89, 89, 89],
"grey35":[89, 89, 89],
"gray36":[92, 92, 92],
"grey36":[92, 92, 92],
"gray37":[94, 94, 94],
"grey37":[94, 94, 94],
"gray38":[97, 97, 97],
"grey38":[97, 97, 97],
"gray39":[99, 99, 99],
"grey39":[99, 99, 99],
"gray40":[102, 102, 102],
"grey40":[102, 102, 102],
"gray41":[105, 105, 105],
"grey41":[105, 105, 105],
"gray42":[107, 107, 107],
"grey42":[107, 107, 107],
"gray43":[110, 110, 110],
"grey43":[110, 110, 110],
"gray44":[112, 112, 112],
"grey44":[112, 112, 112],
"gray45":[115, 115, 115],
"grey45":[115, 115, 115],
"gray46":[117, 117, 117],
"grey46":[117, 117, 117],
"gray47":[120, 120, 120],
"grey47":[120, 120, 120],
"gray48":[122, 122, 122],
"grey48":[122, 122, 122],
"gray49":[125, 125, 125],
"grey49":[125, 125, 125],
"gray50":[127, 127, 127],
"grey50":[127, 127, 127],
"gray51":[130, 130, 130],
"grey51":[130, 130, 130],
"gray52":[133, 133, 133],
"grey52":[133, 133, 133],
"gray53":[135, 135, 135],
"grey53":[135, 135, 135],
"gray54":[138, 138, 138],
"grey54":[138, 138, 138],
"gray55":[140, 140, 140],
"grey55":[140, 140, 140],
"gray56":[143, 143, 143],
"grey56":[143, 143, 143],
"gray57":[145, 145, 145],
"grey57":[145, 145, 145],
"gray58":[148, 148, 148],
"grey58":[148, 148, 148],
"gray59":[150, 150, 150],
"grey59":[150, 150, 150],
"gray60":[153, 153, 153],
"grey60":[153, 153, 153],
"gray61":[156, 156, 156],
"grey61":[156, 156, 156],
"gray62":[158, 158, 158],
"grey62":[158, 158, 158],
"gray63":[161, 161, 161],
"grey63":[161, 161, 161],
"gray64":[163, 163, 163],
"grey64":[163, 163, 163],
"gray65":[166, 166, 166],
"grey65":[166, 166, 166],
"gray66":[168, 168, 168],
"grey66":[168, 168, 168],
"gray67":[171, 171, 171],
"grey67":[171, 171, 171],
"gray68":[173, 173, 173],
"grey68":[173, 173, 173],
"gray69":[176, 176, 176],
"grey69":[176, 176, 176],
"gray70":[179, 179, 179],
"grey70":[179, 179, 179],
"gray71":[181, 181, 181],
"grey71":[181, 181, 181],
"gray72":[184, 184, 184],
"grey72":[184, 184, 184],
"gray73":[186, 186, 186],
"grey73":[186, 186, 186],
"gray74":[189, 189, 189],
"grey74":[189, 189, 189],
"gray75":[191, 191, 191],
"grey75":[191, 191, 191],
"gray76":[194, 194, 194],
"grey76":[194, 194, 194],
"gray77":[196, 196, 196],
"grey77":[196, 196, 196],
"gray78":[199, 199, 199],
"grey78":[199, 199, 199],
"gray79":[201, 201, 201],
"grey79":[201, 201, 201],
"gray80":[204, 204, 204],
"grey80":[204, 204, 204],
"gray81":[207, 207, 207],
"grey81":[207, 207, 207],
"gray82":[209, 209, 209],
"grey82":[209, 209, 209],
"gray83":[212, 212, 212],
"grey83":[212, 212, 212],
"gray84":[214, 214, 214],
"grey84":[214, 214, 214],
"gray85":[217, 217, 217],
"grey85":[217, 217, 217],
"gray86":[219, 219, 219],
"grey86":[219, 219, 219],
"gray87":[222, 222, 222],
"grey87":[222, 222, 222],
"gray88":[224, 224, 224],
"grey88":[224, 224, 224],
"gray89":[227, 227, 227],
"grey89":[227, 227, 227],
"gray90":[229, 229, 229],
"grey90":[229, 229, 229],
"gray91":[232, 232, 232],
"grey91":[232, 232, 232],
"gray92":[235, 235, 235],
"grey92":[235, 235, 235],
"gray93":[237, 237, 237],
"grey93":[237, 237, 237],
"gray94":[240, 240, 240],
"grey94":[240, 240, 240],
"gray95":[242, 242, 242],
"grey95":[242, 242, 242],
"gray96":[245, 245, 245],
"grey96":[245, 245, 245],
"gray97":[247, 247, 247],
"grey97":[247, 247, 247],
"gray98":[250, 250, 250],
"grey98":[250, 250, 250],
"gray99":[252, 252, 252],
"grey99":[252, 252, 252],
"gray100":[255, 255, 255],
"grey100":[255, 255, 255],
"dark grey":[169, 169, 169],
"darkgrey":[169, 169, 169],
"dark gray":[169, 169, 169],
"darkgray":[169, 169, 169],
"dark blue":[0, 0, 139],
"darkblue":[0, 0, 139],
"dark cyan":[0, 139, 139],
"darkcyan":[0, 139, 139],
"dark magenta":[139, 0, 139],
"darkmagenta":[139, 0, 139],
"dark red":[139, 0, 0],
"darkred":[139, 0, 0],
"light green":[144, 238, 144],
"lightgreen":[144, 238, 144],
"olive":[128, 128, 0],
"teal":[0, 128, 128]}


# ------------- Key constants -------------------------------

'''
The key names used by Qt.
Constant    Value   Description

Qt.Key_Escape   0x01000000

Qt.Key_Tab  0x01000001

Qt.Key_Backtab  0x01000002

Qt.Key_Backspace    0x01000003

Qt.Key_Return   0x01000004

Qt.Key_Enter    0x01000005  Typically located on the keypad.

Qt.Key_Insert   0x01000006

Qt.Key_Delete   0x01000007

Qt.Key_Pause    0x01000008  The Pause/Break key (Note: Not anything to do with pausing media)

Qt.Key_Print    0x01000009

Qt.Key_SysReq   0x0100000a

Qt.Key_Clear    0x0100000b

Qt.Key_Home     0x01000010

Qt.Key_End  0x01000011

Qt.Key_Left     0x01000012

Qt.Key_Up   0x01000013

Qt.Key_Right    0x01000014

Qt.Key_Down     0x01000015

Qt.Key_PageUp   0x01000016

Qt.Key_PageDown     0x01000017

Qt.Key_Shift    0x01000020

Qt.Key_Control  0x01000021  On Mac OS X, this corresponds to the Command keys.

Qt.Key_Meta     0x01000022  On Mac OS X, this corresponds to the Control keys. On Windows keyboards, this key is mapped to the Windows key.

Qt.Key_Alt  0x01000023

Qt.Key_AltGr    0x01001103  On Windows, when the KeyDown event for this key is sent, the Ctrl+Alt modifiers are also set.

Qt.Key_CapsLock     0x01000024

Qt.Key_NumLock  0x01000025

Qt.Key_ScrollLock   0x01000026

Qt.Key_F1   0x01000030

Qt.Key_F2   0x01000031

Qt.Key_F3   0x01000032

Qt.Key_F4   0x01000033

Qt.Key_F5   0x01000034

Qt.Key_F6   0x01000035

Qt.Key_F7   0x01000036

Qt.Key_F8   0x01000037

Qt.Key_F9   0x01000038

Qt.Key_F10  0x01000039

Qt.Key_F11  0x0100003a

Qt.Key_F12  0x0100003b

Qt.Key_F13  0x0100003c

Qt.Key_F14  0x0100003d

Qt.Key_F15  0x0100003e

Qt.Key_F16  0x0100003f

Qt.Key_F17  0x01000040

Qt.Key_F18  0x01000041

Qt.Key_F19  0x01000042

Qt.Key_F20  0x01000043

Qt.Key_F21  0x01000044

Qt.Key_F22  0x01000045

Qt.Key_F23  0x01000046

Qt.Key_F24  0x01000047

Qt.Key_F25  0x01000048

Qt.Key_F26  0x01000049

Qt.Key_F27  0x0100004a

Qt.Key_F28  0x0100004b

Qt.Key_F29  0x0100004c

Qt.Key_F30  0x0100004d

Qt.Key_F31  0x0100004e

Qt.Key_F32  0x0100004f

Qt.Key_F33  0x01000050

Qt.Key_F34  0x01000051

Qt.Key_F35  0x01000052

Qt.Key_Super_L  0x01000053

Qt.Key_Super_R  0x01000054

Qt.Key_Menu     0x01000055

Qt.Key_Hyper_L  0x01000056

Qt.Key_Hyper_R  0x01000057

Qt.Key_Help     0x01000058

Qt.Key_Direction_L  0x01000059

Qt.Key_Direction_R  0x01000060

Qt.Key_Space    0x20

Qt.Key_Any  Key_Space

Qt.Key_Exclam   0x21

Qt.Key_QuoteDbl     0x22

Qt.Key_NumberSign   0x23

Qt.Key_Dollar   0x24

Qt.Key_Percent  0x25

Qt.Key_Ampersand    0x26

Qt.Key_Apostrophe   0x27

Qt.Key_ParenLeft    0x28

Qt.Key_ParenRight   0x29

Qt.Key_Asterisk     0x2a

Qt.Key_Plus     0x2b

Qt.Key_Comma    0x2c

Qt.Key_Minus    0x2d

Qt.Key_Period   0x2e

Qt.Key_Slash    0x2f

Qt.Key_0    0x30

Qt.Key_1    0x31

Qt.Key_2    0x32

Qt.Key_3    0x33

Qt.Key_4    0x34

Qt.Key_5    0x35

Qt.Key_6    0x36

Qt.Key_7    0x37

Qt.Key_8    0x38

Qt.Key_9    0x39

Qt.Key_Colon    0x3a

Qt.Key_Semicolon    0x3b

Qt.Key_Less     0x3c

Qt.Key_Equal    0x3d

Qt.Key_Greater  0x3e

Qt.Key_Question     0x3f

Qt.Key_At   0x40

Qt.Key_A    0x41

Qt.Key_B    0x42

Qt.Key_C    0x43

Qt.Key_D    0x44

Qt.Key_E    0x45

Qt.Key_F    0x46

Qt.Key_G    0x47

Qt.Key_H    0x48

Qt.Key_I    0x49

Qt.Key_J    0x4a

Qt.Key_K    0x4b

Qt.Key_L    0x4c

Qt.Key_M    0x4d

Qt.Key_N    0x4e

Qt.Key_O    0x4f

Qt.Key_P    0x50

Qt.Key_Q    0x51

Qt.Key_R    0x52

Qt.Key_S    0x53

Qt.Key_T    0x54

Qt.Key_U    0x55

Qt.Key_V    0x56

Qt.Key_W    0x57

Qt.Key_X    0x58

Qt.Key_Y    0x59

Qt.Key_Z    0x5a

Qt.Key_BracketLeft  0x5b

Qt.Key_Backslash    0x5c

Qt.Key_BracketRight     0x5d

Qt.Key_AsciiCircum  0x5e

Qt.Key_Underscore   0x5f

Qt.Key_QuoteLeft    0x60

Qt.Key_BraceLeft    0x7b

Qt.Key_Bar  0x7c

Qt.Key_BraceRight   0x7d

Qt.Key_AsciiTilde   0x7e

Qt.Key_nobreakspace     0x0a0

Qt.Key_exclamdown   0x0a1

Qt.Key_cent     0x0a2

Qt.Key_sterling     0x0a3

Qt.Key_currency     0x0a4

Qt.Key_yen  0x0a5

Qt.Key_brokenbar    0x0a6

Qt.Key_section  0x0a7

Qt.Key_diaeresis    0x0a8

Qt.Key_copyright    0x0a9

Qt.Key_ordfeminine  0x0aa

Qt.Key_guillemotleft    0x0ab

Qt.Key_notsign  0x0ac

Qt.Key_hyphen   0x0ad

Qt.Key_registered   0x0ae

Qt.Key_macron   0x0af

Qt.Key_degree   0x0b0

Qt.Key_plusminus    0x0b1

Qt.Key_twosuperior  0x0b2

Qt.Key_threesuperior    0x0b3

Qt.Key_acute    0x0b4

Qt.Key_mu   0x0b5

Qt.Key_paragraph    0x0b6

Qt.Key_periodcentered   0x0b7

Qt.Key_cedilla  0x0b8

Qt.Key_onesuperior  0x0b9

Qt.Key_masculine    0x0ba

Qt.Key_guillemotright   0x0bb

Qt.Key_onequarter   0x0bc

Qt.Key_onehalf  0x0bd

Qt.Key_threequarters    0x0be

Qt.Key_questiondown     0x0bf

Qt.Key_Agrave   0x0c0

Qt.Key_Aacute   0x0c1

Qt.Key_Acircumflex  0x0c2

Qt.Key_Atilde   0x0c3

Qt.Key_Adiaeresis   0x0c4

Qt.Key_Aring    0x0c5

Qt.Key_AE   0x0c6

Qt.Key_Ccedilla     0x0c7

Qt.Key_Egrave   0x0c8

Qt.Key_Eacute   0x0c9

Qt.Key_Ecircumflex  0x0ca

Qt.Key_Ediaeresis   0x0cb

Qt.Key_Igrave   0x0cc

Qt.Key_Iacute   0x0cd

Qt.Key_Icircumflex  0x0ce

Qt.Key_Idiaeresis   0x0cf

Qt.Key_ETH  0x0d0

Qt.Key_Ntilde   0x0d1

Qt.Key_Ograve   0x0d2

Qt.Key_Oacute   0x0d3

Qt.Key_Ocircumflex  0x0d4

Qt.Key_Otilde   0x0d5

Qt.Key_Odiaeresis   0x0d6

Qt.Key_multiply     0x0d7

Qt.Key_Ooblique     0x0d8

Qt.Key_Ugrave   0x0d9

Qt.Key_Uacute   0x0da

Qt.Key_Ucircumflex  0x0db

Qt.Key_Udiaeresis   0x0dc

Qt.Key_Yacute   0x0dd

Qt.Key_THORN    0x0de

Qt.Key_ssharp   0x0df

Qt.Key_division     0x0f7

Qt.Key_ydiaeresis   0x0ff

Qt.Key_Multi_key    0x01001120

Qt.Key_Codeinput    0x01001137

Qt.Key_SingleCandidate  0x0100113c

Qt.Key_MultipleCandidate    0x0100113d

Qt.Key_PreviousCandidate    0x0100113e

Qt.Key_Mode_switch  0x0100117e

Qt.Key_Kanji    0x01001121

Qt.Key_Muhenkan     0x01001122

Qt.Key_Henkan   0x01001123

Qt.Key_Romaji   0x01001124

Qt.Key_Hiragana     0x01001125

Qt.Key_Katakana     0x01001126

Qt.Key_Hiragana_Katakana    0x01001127

Qt.Key_Zenkaku  0x01001128

Qt.Key_Hankaku  0x01001129

Qt.Key_Zenkaku_Hankaku  0x0100112a

Qt.Key_Touroku  0x0100112b

Qt.Key_Massyo   0x0100112c

Qt.Key_Kana_Lock    0x0100112d

Qt.Key_Kana_Shift   0x0100112e

Qt.Key_Eisu_Shift   0x0100112f

Qt.Key_Eisu_toggle  0x01001130

Qt.Key_Hangul   0x01001131

Qt.Key_Hangul_Start     0x01001132

Qt.Key_Hangul_End   0x01001133

Qt.Key_Hangul_Hanja     0x01001134

Qt.Key_Hangul_Jamo  0x01001135

Qt.Key_Hangul_Romaja    0x01001136

Qt.Key_Hangul_Jeonja    0x01001138

Qt.Key_Hangul_Banja     0x01001139

Qt.Key_Hangul_PreHanja  0x0100113a

Qt.Key_Hangul_PostHanja     0x0100113b

Qt.Key_Hangul_Special   0x0100113f

Qt.Key_Dead_Grave   0x01001250

Qt.Key_Dead_Acute   0x01001251

Qt.Key_Dead_Circumflex  0x01001252

Qt.Key_Dead_Tilde   0x01001253

Qt.Key_Dead_Macron  0x01001254

Qt.Key_Dead_Breve   0x01001255

Qt.Key_Dead_Abovedot    0x01001256

Qt.Key_Dead_Diaeresis   0x01001257

Qt.Key_Dead_Abovering   0x01001258

Qt.Key_Dead_Doubleacute     0x01001259

Qt.Key_Dead_Caron   0x0100125a

Qt.Key_Dead_Cedilla     0x0100125b

Qt.Key_Dead_Ogonek  0x0100125c

Qt.Key_Dead_Iota    0x0100125d

Qt.Key_Dead_Voiced_Sound    0x0100125e

Qt.Key_Dead_Semivoiced_Sound    0x0100125f

Qt.Key_Dead_Belowdot    0x01001260

Qt.Key_Dead_Hook    0x01001261

Qt.Key_Dead_Horn    0x01001262

Qt.Key_Back     0x01000061

Qt.Key_Forward  0x01000062

Qt.Key_Stop     0x01000063

Qt.Key_Refresh  0x01000064

Qt.Key_VolumeDown   0x01000070

Qt.Key_VolumeMute   0x01000071

Qt.Key_VolumeUp     0x01000072

Qt.Key_BassBoost    0x01000073

Qt.Key_BassUp   0x01000074

Qt.Key_BassDown     0x01000075

Qt.Key_TrebleUp     0x01000076

Qt.Key_TrebleDown   0x01000077

Qt.Key_MediaPlay    0x01000080  A key setting the state of the media player to play

Qt.Key_MediaStop    0x01000081  A key setting the state of the media player to stop

Qt.Key_MediaPrevious    0x01000082

Qt.Key_MediaNext    0x01000083

Qt.Key_MediaRecord  0x01000084

Qt.Key_MediaPause   0x1000085   A key setting the state of the media player to pause (Note: not the pause/break key)

Qt.Key_MediaTogglePlayPause     0x1000086   A key to toggle the play/pause state in the media player (rather than setting an absolute state)

Qt.Key_HomePage     0x01000090

Qt.Key_Favorites    0x01000091

Qt.Key_Search   0x01000092

Qt.Key_Standby  0x01000093

Qt.Key_OpenUrl  0x01000094

Qt.Key_LaunchMail   0x010000a0

Qt.Key_LaunchMedia  0x010000a1

Qt.Key_Launch0  0x010000a2  On X11 this key is mapped to "My Computer" (XF86XK_MyComputer) key for legacy reasons.

Qt.Key_Launch1  0x010000a3  On X11 this key is mapped to "Calculator" (XF86XK_Calculator) key for legacy reasons.

Qt.Key_Launch2  0x010000a4  On X11 this key is mapped to XF86XK_Launch0 key for legacy reasons.

Qt.Key_Launch3  0x010000a5  On X11 this key is mapped to XF86XK_Launch1 key for legacy reasons.

Qt.Key_Launch4  0x010000a6  On X11 this key is mapped to XF86XK_Launch2 key for legacy reasons.

Qt.Key_Launch5  0x010000a7  On X11 this key is mapped to XF86XK_Launch3 key for legacy reasons.

Qt.Key_Launch6  0x010000a8  On X11 this key is mapped to XF86XK_Launch4 key for legacy reasons.

Qt.Key_Launch7  0x010000a9  On X11 this key is mapped to XF86XK_Launch5 key for legacy reasons.

Qt.Key_Launch8  0x010000aa  On X11 this key is mapped to XF86XK_Launch6 key for legacy reasons.

Qt.Key_Launch9  0x010000ab  On X11 this key is mapped to XF86XK_Launch7 key for legacy reasons.

Qt.Key_LaunchA  0x010000ac  On X11 this key is mapped to XF86XK_Launch8 key for legacy reasons.

Qt.Key_LaunchB  0x010000ad  On X11 this key is mapped to XF86XK_Launch9 key for legacy reasons.

Qt.Key_LaunchC  0x010000ae  On X11 this key is mapped to XF86XK_LaunchA key for legacy reasons.

Qt.Key_LaunchD  0x010000af  On X11 this key is mapped to XF86XK_LaunchB key for legacy reasons.

Qt.Key_LaunchE  0x010000b0  On X11 this key is mapped to XF86XK_LaunchC key for legacy reasons.

Qt.Key_LaunchF  0x010000b1  On X11 this key is mapped to XF86XK_LaunchD key for legacy reasons.

Qt.Key_LaunchG  0x0100010e  On X11 this key is mapped to XF86XK_LaunchE key for legacy reasons.

Qt.Key_LaunchH  0x0100010f  On X11 this key is mapped to XF86XK_LaunchF key for legacy reasons.

Qt.Key_MonBrightnessUp  0x010000b2

Qt.Key_MonBrightnessDown    0x010000b3

Qt.Key_KeyboardLightOnOff   0x010000b4

Qt.Key_KeyboardBrightnessUp     0x010000b5

Qt.Key_KeyboardBrightnessDown   0x010000b6

Qt.Key_PowerOff     0x010000b7

Qt.Key_WakeUp   0x010000b8

Qt.Key_Eject    0x010000b9

Qt.Key_ScreenSaver  0x010000ba

Qt.Key_WWW  0x010000bb

Qt.Key_Memo     0x010000bc

Qt.Key_LightBulb    0x010000bd

Qt.Key_Shop     0x010000be

Qt.Key_History  0x010000bf

Qt.Key_AddFavorite  0x010000c0

Qt.Key_HotLinks     0x010000c1

Qt.Key_BrightnessAdjust     0x010000c2

Qt.Key_Finance  0x010000c3

Qt.Key_Community    0x010000c4

Qt.Key_AudioRewind  0x010000c5

Qt.Key_BackForward  0x010000c6

Qt.Key_ApplicationLeft  0x010000c7

Qt.Key_ApplicationRight     0x010000c8

Qt.Key_Book     0x010000c9

Qt.Key_CD   0x010000ca

Qt.Key_Calculator   0x010000cb  On X11 this key is not mapped for legacy reasons. Use Qt.Key_Launch1 instead.

Qt.Key_ToDoList     0x010000cc

Qt.Key_ClearGrab    0x010000cd

Qt.Key_Close    0x010000ce

Qt.Key_Copy     0x010000cf

Qt.Key_Cut  0x010000d0

Qt.Key_Display  0x010000d1

Qt.Key_DOS  0x010000d2

Qt.Key_Documents    0x010000d3

Qt.Key_Excel    0x010000d4

Qt.Key_Explorer     0x010000d5

Qt.Key_Game     0x010000d6

Qt.Key_Go   0x010000d7

Qt.Key_iTouch   0x010000d8

Qt.Key_LogOff   0x010000d9

Qt.Key_Market   0x010000da

Qt.Key_Meeting  0x010000db

Qt.Key_MenuKB   0x010000dc

Qt.Key_MenuPB   0x010000dd

Qt.Key_MySites  0x010000de

Qt.Key_News     0x010000df

Qt.Key_OfficeHome   0x010000e0

Qt.Key_Option   0x010000e1

Qt.Key_Paste    0x010000e2

Qt.Key_Phone    0x010000e3

Qt.Key_Calendar     0x010000e4

Qt.Key_Reply    0x010000e5

Qt.Key_Reload   0x010000e6

Qt.Key_RotateWindows    0x010000e7

Qt.Key_RotationPB   0x010000e8

Qt.Key_RotationKB   0x010000e9

Qt.Key_Save     0x010000ea

Qt.Key_Send     0x010000eb

Qt.Key_Spell    0x010000ec

Qt.Key_SplitScreen  0x010000ed

Qt.Key_Support  0x010000ee

Qt.Key_TaskPane     0x010000ef

Qt.Key_Terminal     0x010000f0

Qt.Key_Tools    0x010000f1

Qt.Key_Travel   0x010000f2

Qt.Key_Video    0x010000f3

Qt.Key_Word     0x010000f4

Qt.Key_Xfer     0x010000f5

Qt.Key_ZoomIn   0x010000f6

Qt.Key_ZoomOut  0x010000f7

Qt.Key_Away     0x010000f8

Qt.Key_Messenger    0x010000f9

Qt.Key_WebCam   0x010000fa

Qt.Key_MailForward  0x010000fb

Qt.Key_Pictures     0x010000fc

Qt.Key_Music    0x010000fd

Qt.Key_Battery  0x010000fe

Qt.Key_Bluetooth    0x010000ff

Qt.Key_WLAN     0x01000100

Qt.Key_UWB  0x01000101

Qt.Key_AudioForward     0x01000102

Qt.Key_AudioRepeat  0x01000103

Qt.Key_AudioRandomPlay  0x01000104

Qt.Key_Subtitle     0x01000105

Qt.Key_AudioCycleTrack  0x01000106

Qt.Key_Time     0x01000107

Qt.Key_Hibernate    0x01000108

Qt.Key_View     0x01000109

Qt.Key_TopMenu  0x0100010a

Qt.Key_PowerDown    0x0100010b

Qt.Key_Suspend  0x0100010c

Qt.Key_ContrastAdjust   0x0100010d

Qt.Key_MediaLast    0x0100ffff

Qt.Key_unknown  0x01ffffff

Qt.Key_Call     0x01100004  A key to answer or initiate a call (see Qt.Key_ToggleCallHangup for a key to toggle current call state)

Qt.Key_Camera   0x01100020  A key to activate the camera shutter

Qt.Key_CameraFocus  0x01100021  A key to focus the camera

Qt.Key_Context1     0x01100000

Qt.Key_Context2     0x01100001

Qt.Key_Context3     0x01100002

Qt.Key_Context4     0x01100003

Qt.Key_Flip     0x01100006

Qt.Key_Hangup   0x01100005  A key to end an ongoing call (see Qt.Key_ToggleCallHangup for a key to toggle current call state)

Qt.Key_No   0x01010002

Qt.Key_Select   0x01010000

Qt.Key_Yes  0x01010001

Qt.Key_ToggleCallHangup     0x01100007  A key to toggle the current call state (ie. either answer, or hangup) depending on current call state

Qt.Key_VoiceDial    0x01100008

Qt.Key_LastNumberRedial     0x01100009

Qt.Key_Execute  0x01020003

Qt.Key_Printer  0x01020002

Qt.Key_Play     0x01020005

Qt.Key_Sleep    0x01020004

Qt.Key_Zoom     0x01020006

Qt.Key_Cancel   0x01020001
'''


