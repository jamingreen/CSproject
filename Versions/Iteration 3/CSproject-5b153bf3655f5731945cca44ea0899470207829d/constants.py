import re

# Color
BROWN = (135, 52, 35)
SKYBLUE = (91, 148, 251)
LIGHTGREY = (213, 216, 220)
BLACK = (0, 0, 0)
YELLOW = (251,208,0)
WHITE = (255,255,255)
SETTINGSCREENCOLOR = (144, 212, 204)

#Size
SIZE = (800,500)
BLOCKSIZE = (30,30)
SETTINGS_BUTTON_SIZE = (105, 40)
LEVEL_BUTTON_SIZE = (148, 40)
LEVEL_IMAGE_SIZE = (240, 168)
PLAYER_SIZE = (BLOCKSIZE[0], BLOCKSIZE[1]*2)

# Padding
LEVEL_IMAGE_BUTTON_PADDING = EDGE_LEVEL_IMAGE_PADDING = 16
LEVEL_2_LEVEL_PADDING = 24

#Misc
EXIT = "exit"
NUM_OF_LEVELS = 3

#Screens
MENU = "menu"
SETTINGSCREEN = "setting screen"
GAMEMENU = "game menu"
GAMESCREEN = "game screen"

#Status Code
SCREENTOSETTING = "change to setting screen"
SCREENTOGAMEMENU = "change to game menu screen"
CLOSEGAMEMENU = "close game menu screen"
CLOSEGAME = "close game"
EXITGAME = "exit game"

# Camera
PLAYER_LEFT_PADDING =  50
PLAYER_RIGHT_PADDING = SIZE[1] - 100

# Player
HORIZONAL_MAX_SPEED = 10
JUMP_SPEED = 50
GRAVITY = 5

# Game
MENU_BUTTON_PADDING = 20





# Level status code
def create_level_status_code(level):
    return f"Initialise Level {level}"

def check_status_init_level(string):
    return bool(re.match("^Initialise Level.+[0-9]+$", string))

def extract_level_from_status_code(status_code):
    if not create_level_status_code(status_code):
        return None
    try:
        return int(status_code.split(" ")[-1])

    except ValueError:
        return None