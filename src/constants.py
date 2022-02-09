import sys

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
RADIUS = 15
if "--debug" or "-d" in sys.argv:
    flag_debug = True
if "--silent" or "-s" in sys.argv:
    flag_silent = True
