import re

# Color
BROWN = (135, 52, 35)
SKYBLUE = (91, 148, 251)
LIGHTGREY = (213, 216, 220)
BLACK = (0, 0, 0)
YELLOW = (251,208,0)
WHITE = (255,255,255)
GOLD = (212, 175, 55)
DARKBLUE = (0, 0, 139)
SETTINGSCREENCOLOR = (144, 212, 204)
SILVER = (192, 192, 192)
RED = (255,0,0)

#Size
SIZE = (810,540)
BLOCKSIZE = (30,30)
SETTINGS_BUTTON_SIZE = (105, 40)
LEVEL_BUTTON_SIZE = (148, 40)
LEVEL_IMAGE_SIZE = (240, 168)
PLAYER_SIZE = (int(BLOCKSIZE[0]*0.4), int(BLOCKSIZE[1]*0.4))
FONTSIZE = 20

# Padding
LEVEL_IMAGE_BUTTON_PADDING = EDGE_LEVEL_IMAGE_PADDING = 16
LEVEL_2_LEVEL_PADDING = 24
INSTRUCTION_MENU_PADDING = 10

#Misc
EXIT = "exit"
NUM_OF_LEVELS = 3

#Screens
MENU = "menu"
SETTINGSCREEN = "setting screen"
GAMESCREEN = "game screen"
INSTRUCTIONSCREEN = "instruction screen"
GAMEMENU = "game menu"
GAME = "game"
DEATHSCREEN = "death screen"

#Status Code
SCREENTOSETTING = "change to setting screen"
SCREENTOGAMEMENU = "change to game menu screen"
RETURNTOGAME = "close game menu screen"
CLOSEGAME = "close game"
EXITGAME = "exit game"
SCREENTOINSTRUCTION = "change to instruction screen"
RESTARTGAME = "restart game"
PLAYERDEATH = "player death"

# Camera
PLAYER_LEFT_PADDING =  150
PLAYER_RIGHT_PADDING = SIZE[1] - 100

# Player
PLAYERSTARTPOS = (PLAYER_LEFT_PADDING,BLOCKSIZE[1] * 7 )
HORIZONAL_MAX_SPEED = BLOCKSIZE[1] * 0.15
JUMP_SPEED = BLOCKSIZE[1] / 2
GRAVITY = BLOCKSIZE[1] /25

#Player statusCode
MOVING_LEFT = "moving left"
MOVING_RIGHT = "moving right"

# Game
MENU_BUTTON_PADDING = 20

#Enemy
GOOMBA_SIZE = (BLOCKSIZE[0], BLOCKSIZE[1])

# Spike
UP_SPEED = 10
GROW_SPEED = 10
HORI_SPEED = 10
