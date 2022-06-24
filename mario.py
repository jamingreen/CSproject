import pygame, math, sys, csv
from pygame import math
from constants import *
from camera import *
from helper import *

PLAYERSTARTPOS = (BLOCKSIZE[0],BLOCKSIZE[1] * 7 )

class Game:
    
    def __init__(self, level = 1):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.map = Map("map" +str(level) +".csv")
        self.level = level
        self.menu_button = MenuButton()
        self.status = []
        self.openMenu = False
        self.menuScreen = GameMenuScreen()
        self.done = False
        self.mouseBuffer = MouseBuffer()

        self.gameSpriteGroup = []

        self.player = Player(HORIZONAL_MAX_SPEED, self.map.vertices)
        self.camera = Camera(self.player, self.map.vertices)

        self.gameSpriteGroup.extend([self.player, self.map, self.menu_button])

    def keyResponse(self, event):
        if self.openMenu:
            self.status = self.menuScreen.keyResponse(event,self.status)
        else:
            self.status = self.player.keyResponse(event, self.status)

    def mouseResponse(self, position):
        self.status = self.menu_button.mouseInteraction(position, self.status)
        if self.openMenu:
            self.status = self.menuScreen.mouseInteraction(position, self.status)

    def readStatus(self):
        for stat in self.status:
            if stat == SCREENTOGAMEMENU:
                self.openMenu = True
            elif stat == CLOSEGAME:
                self.done = True
            elif stat == CLOSEGAMEMENU:
                self.openMenu = False
        self.status = []

            
    def logic(self):
        self.readStatus()
        self.mouseBuffer.logic()
        self.player.update()
        self.camera.scroll()

    def drawScreen(self):
        self.screen.fill(SKYBLUE)

        # -- Draw here
        for sprite in self.gameSpriteGroup:
            sprite.draw(self.screen, self.camera.position)
        
        # Draw menu screen on top
        if self.openMenu:
            self.menuScreen.drawScreen(self.screen)

        pygame.display.flip()


    def play(self):
        self.done = False
        print("Start Game cycle")
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    sys.exit()
                self.keyResponse(event)
            click,_,_ = pygame.mouse.get_pressed()
            if click == True and not self.mouseBuffer.flag:
                self.mouseBuffer.tFlag()
                mouse = pygame.mouse.get_pos()
                self.mouseResponse(mouse)

            #--Game logic goes after this comment
            self.logic()

            # -- Screen background is BLACK
            self.drawScreen()

            self.clock.tick(60)



class Player(pygame.sprite.Sprite):
    
    def __init__(self, horizonal_max_speed, vertices):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/redRect.png"), PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYERSTARTPOS[0]
        self.rect.y = PLAYERSTARTPOS[1]
        self.xSpeed = 0
        self.ySpeed = 0
        self.left_border = vertices[0]
        self.right_border = vertices[1] - PLAYER_SIZE[0] # right most of the map
        self.horizonal_max_speed = horizonal_max_speed
    
    def draw(self, screen, cam_position):
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))

    def set_speed_x(self, speed):
        self.xSpeed = speed

    def start_shooting(self):
        pass

    def stop_shooting(self):
        pass

    def jump(self): 
        self.ySpeed = -JUMP_SPEED

    def jumpBuffer(self):
        pass

    def update(self):
        self.rect.x += self.xSpeed
        self.rect.x = min(self.rect.x, self.right_border)
        self.rect.x = max(self.rect.x, self.left_border)
        self.rect.y += self.ySpeed
        self.ySpeed += GRAVITY
        # Require change to tile based
        self.rect.y = min(self.rect.y, 350)

    def keyResponse(self,event, status):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.set_speed_x(-self.horizonal_max_speed)
            elif event.key == pygame.K_d:
                self.set_speed_x(self.horizonal_max_speed)
            elif event.key == pygame.K_w:
                self.jump()
            elif event.key == pygame.K_SPACE:
                self.start_shooting()
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                self.set_speed_x(0)
            elif event.key == pygame.K_SPACE:
                self.stop_shooting()
        return status
# 16 x 10 block per map
class Map:
    
    def __init__(self, filename):
        temp = []
        with open(filename, 'r') as f:
            reader =  csv.reader(f)
            next(reader)
            
            self.vertices = apply(next(reader), "int") # min x, max x, min y, max y

            for row in reader:
                temp.append(tuple(row))
        
        self.groundSpriteGroup = pygame.sprite.Group()
        self.tileGroup = pygame.sprite.Group()
        self.parseMap(temp)
        

    def parseMap(self,tiles):
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

    def draw(self,screen, cam_pos):
        for sprite in self.tileGroup:
            sprite.draw(screen, cam_pos)


class Tile(pygame.sprite.Sprite):

    def __init__(self,position, imgFile):
        super().__init__()
        self.x = position[0]
        self.y = position[1]
        self.image = pygame.transform.scale(pygame.image.load(imgFile), BLOCKSIZE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, screen, cam_pos):
        screen.blit(self.image, (self.rect.x - cam_pos.x, self.rect.y))
    

class Ground(Tile):

    def __init__(self,position):
        super().__init__(position, "images/groundTile.png")

class AirTile(Tile):
    
    def __init__(self,position):
        super().__init__(position,"images/airTile.png")

class MenuButton(Button):

    def __init__(self,):
        super().__init__(40,40,(SIZE[0]- MENU_BUTTON_PADDING - 40, MENU_BUTTON_PADDING),"images/settingButton.png")

    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([SCREENTOGAMEMENU])
        return status

class GameMenuScreen():

    def __init__(self):
        self.background = Background(706, 381, (47, 48), YELLOW)
        self.closeButton = CloseButton(24,24, (741, 36))
        self.quitButton = QuitButton((331, 278))
        self.controlButton = ControlButton((331,158))
        self.gameMenu_sprite_group = [self.background, self.closeButton, self.quitButton,self.controlButton]

    def drawScreen(self, screen):
        for sprite in self.gameMenu_sprite_group:
            sprite.draw(screen)

    def mouseInteraction(self,position, status):
        for sprite in self.gameMenu_sprite_group:
            status = sprite.mouseInteraction(position, status)
        return status

    def keyResponse(self,event, status):
        for sprite in self.gameMenu_sprite_group:
            status = sprite.keyResponse(event, status)
        return status

class CloseButton(Button):

    def __init__(self,width, height, position):
        super().__init__(width, height, position, "images/closeButton.jpg")

    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([CLOSEGAMEMENU])
        return status

class QuitButton(WordButton):

    def __init__(self, position):
        super().__init__(140,40, position, (51, 51, 204), WHITE, "Exit Game")
    
    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([CLOSEGAME])
        return status
    
class ControlButton(WordButton):

    def __init__(self, position):
        super().__init__(140,40, position, (51, 51, 204), WHITE, "Controls")
    
    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            pass
        return status