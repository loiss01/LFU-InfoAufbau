from gpanel import *

GPANEL_WINDOW_WIDTH = GPANEL_WINDOW_HEIGHT = 550
BIT_MAP_WIDTH = BIT_MAP_HEIGHT = 500

DISC_RADIUS = 125

RED_DISC_CENTER = (200, 200)
GREEN_DISC_CENTER = (300, 200)
BLUE_DISC_CENTER = (250,300)

makeGPanel(Size(GPANEL_WINDOW_WIDTH, GPANEL_WINDOW_HEIGHT))
window(0, GPANEL_WINDOW_WIDTH-1, 0, GPANEL_WINDOW_HEIGHT-1)

bit_map = GBitmap(BIT_MAP_WIDTH, BIT_MAP_HEIGHT)


for y_coordinate in range(BIT_MAP_WIDTH):
    for x_coordinate in range(BIT_MAP_HEIGHT):
        red_intensity = green_intensity = blue_intensity = 0

        if (x_coordinate - RED_DISC_CENTER[0])**2 + (y_coordinate - RED_DISC_CENTER[1])**2 < DISC_RADIUS**2:
            red_intensity = 255
        if (x_coordinate - GREEN_DISC_CENTER[0])**2 + (y_coordinate - GREEN_DISC_CENTER[1])**2 < DISC_RADIUS**2:
            green_intensity = 255
        if (x_coordinate - BLUE_DISC_CENTER[0])**2 + (y_coordinate - BLUE_DISC_CENTER[1])**2 < DISC_RADIUS**2:
            blue_intensity = 255

        # print(GPANEL_WINDOW_WIDTH - y_coordinate)
        bit_map.setPixelColor(x_coordinate, (BIT_MAP_WIDTH - 1) - y_coordinate, makeColor(red_intensity, green_intensity, blue_intensity))

image(bit_map, (GPANEL_WINDOW_WIDTH-BIT_MAP_WIDTH)//2, (GPANEL_WINDOW_HEIGHT-BIT_MAP_HEIGHT)//2)