MAP_SIZE = 15
CASE_SIZE = 32
WINDOW_SIZE = MAP_SIZE * CASE_SIZE
WINDOW_TITLE = "MacGyver Escape"
MAP_FILENAME = "map"

PATH = "ressource/"
PATH_CHAR = "O"
STAIR_CHAR = "S"
DEPARTURE_CHAR = "D"
GUARD_CHAR = "G"
WALL_CHAR = "W"

IMAGE_WALL = PATH + "wall.png"
IMAGE_GROUND = PATH + "ground.png"

letter_to_icon = {
    STAIR_CHAR: PATH + "stair.png",
    DEPARTURE_CHAR: PATH + "PJ.png",
    PATH_CHAR: IMAGE_GROUND,
    GUARD_CHAR: PATH + "guard.png"
}

ITEMS_NUMBER = 3
IMAGE_ITEM_1 = PATH + "ether.png"
IMAGE_ITEM_2 = PATH + "tube.png"
IMAGE_ITEM_3 = PATH + "needle.png"
IMAGE_ITEM_4 = None
IMAGE_ITEM_5 = None
IMAGE_ITEM_6 = None

FPS_MAX = 30

STATE_DEAD = 9
STATE_OVER = 8
