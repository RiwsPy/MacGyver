MAP_SIZE = 15
CASE_SIZE = 32
WINDOW_SIZE = MAP_SIZE * CASE_SIZE
WINDOW_TITLE = "MacGyver Escape"
MAP_FILENAME = "data/map_01.txt"

PATH = "resource/"
PATH_CHAR = "O"
STAIR_CHAR = "S"
START_CHAR = "D"
GUARD_CHAR = "G"
WALL_CHAR = "W"

IMAGE_WALL = PATH + "wall.png"
IMAGE_GROUND = PATH + "ground.png"

letter_to_icon = {
    STAIR_CHAR: PATH + "stair.png",
    START_CHAR: PATH + "player.png",
    PATH_CHAR: IMAGE_GROUND,
    GUARD_CHAR: PATH + "guard.png"
}

ITEMS_NUMBER = 3

items_icon = [
    PATH + "ether.png",
    PATH + "tube.png",
    PATH + "needle.png",
    None]

FPS_MAX = 30

STATE_OVER = MAP_SIZE * MAP_SIZE + 1
