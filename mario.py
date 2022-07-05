import pygame, math, sys, csv
from pygame import math
from constants import *
from camera import *
from helper import *

class Game:
    
    def __init__(self, level = 1):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.map = Map("map" +str(level) +".csv")
        self.level = level
        self.menu_button = MenuButton()
        self.status = []
        self.menuScreen = GameMenuScreen()
        self.done = False
        self.mouseBuffer = MouseBuffer()
        self.instruction_screen = InstructionScreen(RETURNTOGAME)
        self.currentScreen = GAME
        self.restart = False

        self.gameSpriteGroup = []

        self.player = Player(HORIZONAL_MAX_SPEED, self.map.vertices)
        self.camera = Camera(self.player, self.map.vertices)
        self.enemy_sprite_group = []

        self.gameSpriteGroup.extend([self.player, self.map, self.menu_button])

        self.parseEntities("entity"+str(level)+".csv")

    def parseEntities(self, filename):
        with open(filename, 'r') as f:
            reader =  csv.reader(f)
            next(reader)

            for row in reader:
                self.create_enemies(row)
        self.gameSpriteGroup.extend(self.enemy_sprite_group)

    def create_enemies(self, row):
        position = relativeCoor2DeCoor((int(row[1]), int(row[2])))
        x_boundary = tuple(apply(row[3].split("|"), "xReToDe"))
        y_boundary = tuple(apply(row[4].split("|"), "yReToDe"))
        if row[0] == "goomba":
            temp = Goomba(position, x_boundary, y_boundary)
            self.enemy_sprite_group.append(temp)

    def keyResponse(self, event):
        if self.currentScreen == GAMEMENU:
            self.status = self.menuScreen.keyResponse(event,self.status)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.status = self.instruction_screen.keyResponse(event, self.status)
        elif self.currentScreen == GAME:
            self.status = self.player.keyResponse(event, self.status)

    def mouseResponse(self, position):
        self.status = self.menu_button.mouseInteraction(position, self.status)
        if self.currentScreen == GAMEMENU:
            self.status = self.menuScreen.mouseInteraction(position, self.status)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.status = self.instruction_screen.mouseInteraction(position, self.status)

    def readStatus(self):
        for stat in self.status:
            if stat == SCREENTOGAMEMENU:
                self.currentScreen = GAMEMENU
            elif stat == CLOSEGAME:
                self.done = True
            elif stat == RETURNTOGAME:
                self.currentScreen = GAME
            elif stat == SCREENTOINSTRUCTION:
                self.currentScreen = INSTRUCTIONSCREEN
            elif stat == RESTARTGAME:
                self.done = True
                self.restart = True
        self.status = []

            
    def logic(self):
        self.readStatus()
        self.mouseBuffer.logic()
        if self.currentScreen == GAME:
            temp = self.player.update(self.map.tileGroup, self.map.dead_zone, self.status)
            if temp != None:
                self.status.append(temp)
            self.camera.scroll()

            for enemy in self.enemy_sprite_group:
                enemy.update()

    def drawScreen(self):
        self.screen.fill(SKYBLUE)

        # -- Draw here
        for sprite in self.gameSpriteGroup:
            sprite.draw(self.screen, self.camera.position)
        
        # Draw menu screen on top
        if self.currentScreen == GAMEMENU:
            self.menuScreen.drawScreen(self.screen)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.instruction_screen.drawScreen(self.screen)

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

            self.drawScreen()
            print("_____________")
            self.clock.tick(60)
        return self.restart

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
        self.on_ground = True
        self.health = 100
    
    def draw(self, screen, cam_position):
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))

    def set_speed_x(self, speed):
        self.xSpeed = speed

    def start_shooting(self):
        pass

    def stop_shooting(self):
        pass

    def jump(self): 
        if self.on_ground:
            self.jump_num = 1
            self.on_ground = False
            self.ySpeed = -JUMP_SPEED
        """elif self.jump_num > 0:
            self.jump_num -= 1
            self.on_ground = False
            self.ySpeed = -JUMP_SPEED"""

    def jumpBuffer(self):
        pass

    def movementX(self):
        self.rect.x += self.xSpeed

        # boarder collision
        self.rect.x = min(self.rect.x, self.right_border)
        self.rect.x = max(self.rect.x, self.left_border)
    
    def movementY(self):
        self.rect.y += self.ySpeed
        self.ySpeed += GRAVITY
        
    def collisionX(self, tiles):

        # move right
        if self.xSpeed > 0:
            for tile in tiles:
                self.rect.x = min(tile.rect.x - PLAYER_SIZE[0], self.rect.x)
        elif self.xSpeed < 0:
            for tile in tiles:
                self.rect.x = max(tile.rect.right, self.rect.x)

    def collisionY(self, tiles):
        if self.ySpeed > 0:
            self.on_ground = True
            for tile in tiles:
                self.rect.y = min(tile.rect.top - PLAYER_SIZE[1], self.rect.y)

        elif self.ySpeed < 0:
            for tile in tiles:
                self.rect.y = max(tile.rect.bottom, self.rect.y)
        self.ySpeed = 0


    def update(self, tiles, dead_zone, status):
        self.movementX()
        collided_tiles = pygame.sprite.spritecollide(self, tiles, False)
        if len(collided_tiles) != 0:
            self.collisionX(collided_tiles)
        
        self.movementY()
        collided_tiles = pygame.sprite.spritecollide(self, tiles, False)
        if len(collided_tiles) != 0:
            self.collisionY(collided_tiles)

        self.check_dead_zone(dead_zone)
        return self.checkdeath()
        

    def check_dead_zone(self,dead_zone):
        for dead in dead_zone:
            if self.rect.x >= dead[0] and self.rect.x <= dead[0] + dead[2] and self.rect.y >= dead[1] and self.rect.y <= dead[1] + dead[3]:
                self.health -= 1000
                print("death")

    def checkdeath(self):
        if self.health <= 0:
            self.respawn()
            return SCREENTOGAMEMENU

    def respawn(self):
        pass

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
    
    def __init__(self, map_file_name):
        self.groundSpriteGroup = pygame.sprite.Group()
        self.tileGroup = pygame.sprite.Group()
        self.dead_zone = []

        with open(map_file_name, 'r') as f:
            reader =  csv.reader(f)
            next(reader)
            
            self.vertices = apply(next(reader), "int") # min x, max x, min y, max y

            for row in reader:
                self.parseMap(row)
        

    def parseMap(self,row):
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
        elif row[0] == "barrier":
            self.dead_zone.append((*dePos, width*BLOCKSIZE[0], height*BLOCKSIZE[1]))

    def draw(self,screen, cam_pos):
        for sprite in self.tileGroup:
            sprite.draw(screen, cam_pos)

    def update(self):
        pass


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
        self.closeButton = CloseButton(24,24, (741, 36), RETURNTOGAME)
        self.quitButton = QuitButton((331, 306))
        self.controlButton = InstructionButton((331,118))
        self.restartButton = RestartButton((331, 212))
        self.gameMenu_sprite_group = [self.background, self.closeButton, self.quitButton,self.controlButton, self.controlButton, self.restartButton]

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

class Enemy(pygame.sprite.Sprite):

    def __init__(self,position, x_boundary, y_boundary, imgName, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imgName), size)
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x_speed = 3
        

    def update(self):
        self.rect.x += self.x_speed
        if self.x_speed >0 and self.rect.x > self.x_boundary[1]-self.size[0]:
            self.rect.x = self.x_boundary[1]-self.size[0]
            self.x_speed *= -1
        elif self.x_speed < 0 and self.rect.x < self.x_boundary[0]:
            self.rect.x = self.x_boundary[0]
            self.x_speed *= -1


    def draw(self, screen, cam_position):
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))

class Goomba(Enemy):

    def __init__(self, position, x_boundary, y_boundary):
        super().__init__(position, x_boundary, y_boundary, "images/goomba.png", GOOMBA_SIZE)