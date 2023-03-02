status = []
status1, status2, status3, status4, status5 = 1,1,1,1,1


for stat in status:

	if stat == status1:
		# Action 1
		pass

	elif stat == status2:
		# Action 2
		pass

	elif stat == status3:
		# Action 3
		pass

	elif stat == status4:
		# Action 4
		pass

	elif stat == status5:
		# Action 5
		pass

	# endif

# next stat
import pygame
from Code.constants import *
from Code.mario import *
from Code.helper import *
from Code.main import *
screen1 , screen2 = 1

def keyResponse(self: Game, event: pygame.event):
        # Different response with respect to the screen mode
        if self.currentScreen == screen1:
            self.status = self.screen1.keyResponse(event,self.status)
        elif self.currentScreen == screen2:
            self.status = self.screen2.keyResponse(event, self.status)
        elif self.currentScreen == GAME:
            self.status = self.player.keyResponse(event, self.status)
        self.gameResponse(event)
        
def keyResponse(self: Player,event: pygame.event, status: list) -> list:
        if event.type == pygame.KEYDOWN:
            
            # If W is pressed, jump
            if event.key == pygame.K_w:
                self.jump()
                
            # If space is pressed, shoot bullet
            elif event.key == pygame.K_SPACE:
                self.shoot_bullet()

        # get the key being pressed
        key_p = pygame.key.get_pressed()
        
        # If the A is pressed down, set speed as left
        if key_p[pygame.K_a]:
            self.set_speed_x(-self.horizonal_max_speed)
            self.face_direction = -1
        
        # If the D is pressed down, set speed as right
        elif key_p[pygame.K_d]:
            self.set_speed_x(self.horizonal_max_speed)
            self.face_direction = 1
            
        # If None of A or D is pressed, set speed to 0
        else:
            self.set_speed_x(0)
            
        return status

def shoot_bullet(self: Player):
    
	# Check if the player is allow to shoot bullets
	if self.bullet_available:
		bullet = Bullet(self.face_direction, self.rect.center)
		self.bullet_group.add(bullet)
		self.bullet_available = False
  
def enemy_interaction(self: Player,enemy_sprite_group: list, trap_group: TrapGroup, trapClasses: tuple) -> str:   
        # Player dies if it touches with any enemy
        for enemy in enemy_sprite_group:
            if type(enemy) == Goomba:
                if pygame.sprite.collide_rect(self, enemy):
                    return PLAYERDEATH
                
        # Player dies if it touches traps
        for trap in trap_group.all_trap_group:
            if isinstance(trap, trapClasses):
                for rect in trap.rect_group:
                    if self.rect.colliderect(rect):
                        return PLAYERDEATH
                    
        # Return None if the player hasn't died
        return None
def relativeCoor2DeCoor():
    pass
BLOCKSIZE = ()

letter1 = 1
class Tile1:
	pass

def parseMap(self: Map, map: list, barrier_list: list):
    self.dead_zone.append((*barrier_list[0:2], barrier_list[2]*BLOCKSIZE[0], barrier_list[3]*BLOCKSIZE[1]))
    for r_num, row in enumerate(map):
        for c_num, col in enumerate(row):
            if col == letter1:
                ground = Tile1()
                self.tileGroup.add(ground)
            elif col == "F":
                self.finish_point = FinishPoint(r_num, c_num)
            elif col == "C":
                tile = Check_point(r_num, c_num)
                self.checkpoint_group.append(tile)

class Setting:
    pass

class Main():

    def __init__(self):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Mario")
        self.clock = pygame.time.Clock()
        self.all_sprites_list = []
        self.mouseBuffer = MouseBuffer()
        self.currentScreen = MENU

        # Objects
        self.menu = Menu(self.screen)
        self.setting = Setting()
        
        self.all_sprites_list.extend([self.menu, self.setting])

        # Sprite Groups
        self.status = []
        

    def keyResponse(self,event):
        pass

    # Change status (Task pending to do)
    def mouseResponse(self, position):
        if self.currentScreen == MENU:
            self.status = self.menu.mouseInteraction(position, self.status)
        elif self.currentScreen == SETTINGSCREEN:
            self.status = self.setting.mouseInteraction(position, self.status)
    
    def setCurrentScreen(self, newScreen):
        self.currentScreen = newScreen

    def readStatus(self):
        i = 0
        while i < len(self.status):
            stat = self.status[i]
            if stat == SCREENTOSETTING:
                self.setCurrentScreen(SETTINGSCREEN)
            del self.status[i]

    def logic(self):
        self.mouseBuffer.logic()
        pass

    def drawScreen(self):
        self.screen.fill(BROWN)
        if self.currentScreen == MENU:
            self.menu.drawScreen(self.screen)
        elif self.currentScreen == SETTINGSCREEN:
            self.setting.drawScreen(self.screen)
        
        pygame.display.flip()

    def gameplay(self):
        done = False
        while not done:


            # -- User input and controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.keyResponse(event)
            
            # Mouse pointer interaction   
            click,_,_ = pygame.mouse.get_pressed()
            # only runs if it is left-clicked
            if click == True and not self.mouseBuffer.flag:
                self.mouseBuffer.tFlag()
                print("Left click")
                mouse = pygame.mouse.get_pos()
                self.mouseResponse(mouse)

            
            #--Game logic goes after this comment
            self.logic()


            # -- Screen background is BLACK
            self.drawScreen()


            self.clock.tick(60)

        #Endwhile
        self.finishScreen()
        
from dataclasses import dataclass

@dataclass
class Main:
    size: tuple = SIZE
    screen: pygame.Surface = pygame.display.set_mode(size)
    clock: pygame.time.Clock = pygame.time.Clock()
    all_sprite_list: list = []
    mouseBuffer: MouseBuffer = MouseBuffer()
    currentScreen: str = MENU
    menu: Menu = Menu()
    setting: Setting = Setting()
    all_sprite_list.extend([menu, setting])

    status: list = []
    
main = Main()
print(main)



class Menu():

    def __init__(self, screen):
        self.size = SIZE
        self.screen = screen
        self.menuSpriteGroup = pygame.sprite.Group()
        self.levelButtonGroup = pygame.sprite.Group()

        self.settingButton = SettingButton(*SETTINGS_BUTTON_SIZE, (SIZE[0] - 132, 20))
        self.menuSpriteGroup.add(self.settingButton)
        
        startY = 120 + LEVEL_IMAGE_SIZE[1] + LEVEL_IMAGE_BUTTON_PADDING
        startX = EDGE_LEVEL_IMAGE_PADDING + (LEVEL_IMAGE_SIZE[0]-LEVEL_BUTTON_SIZE[0])/2


        for lvlNum in range(NUM_OF_LEVELS):
            levelBut = LevelButton(lvlNum+1, f"Level {lvlNum + 1}",*LEVEL_BUTTON_SIZE,(startX,startY), "images/tempLevelImg.png")
            self.levelButtonGroup.add(levelBut)
            self.menuSpriteGroup.add(levelBut)
            startX += 264

    # Return new status
    def mouseInteraction(self, position, status):
        for sprite in self.menuSpriteGroup:
            status = sprite.mouseInteraction(position, status)
        return status

    def drawScreen(self,screen):
        self.settingButton.draw(screen)
        for sprite in self.menuSpriteGroup:
            sprite.draw(screen)
            
class Game():
    
    def __init__(self, level = 1):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.map = Map("map" +str(level) +".csv")
        self.level = level

        self.gameSpriteGroup = []

        self.player = Player()

        self.gameSpriteGroup.extend([self.player, self.map])

    def __init__(self, ):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/redRect.png"), PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYERSTARTPOS[0]
        self.rect.y = PLAYERSTARTPOS[1]
        self.xSpeed = 0
        self.ySpeed = 0
    def __init__(self, filename):
        temp = []
        with open(filename, 'r') as f:
            reader =  csv.reader(f)
            next(reader)
            
            for row in reader:
                temp.append(tuple(row))
        self.groundSpriteGroup = pygame.sprite.Group()
        self.tileGroup = pygame.sprite.Group()
        self.parseMap(temp)

def parseMap(self: Map,tiles):
    for row in tiles:
        relPos = (int(row[1]), int(row[2]))
        dePos = relativeCoor2DeCoor(relPos)
        width = int(row[3])
        height = int(row[4])
        if row[0] == "ground":
            for i in range(width):
                for j in range(height):
                    groundTile = Ground((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.groundSpriteGroup.add(groundTile)
                    self.tileGroup.add(groundTile)
        elif row[0] == "airTile":
            for i in range(width):
                for j in range(height):
                    airTile = AirTile((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.tileGroup.add(airTile)
                    

class Tile(pygame.sprite.Sprite):

    def __init__(self,position, imgFileName):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imgFileName),BLOCKSIZE)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    

class Ground(Tile):

    def __init__(self,position):
        super().__init__(position,"images/groundTile.png")

class AirTile(Tile):
    
    def __init__(self,position):
        super().__init__(position, "images/airTile.png")