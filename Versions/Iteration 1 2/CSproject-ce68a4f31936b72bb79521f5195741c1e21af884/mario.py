import pygame, math, sys, csv
from pygame import math
from constants import *
from helper import Button, relativeCoor2DeCoor, deCoor2RelativeCoor

PLAYERSTARTPOS = (BLOCKSIZE[0],BLOCKSIZE[1] * 7 )

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

    def keyResponse(self, event):
        pass

    def mouseResponse(self, position):
        pass

    def logic(self):
        pass

    def drawScreen(self):
        self.screen.fill(SKYBLUE)

        # -- Draw here
        for sprite in self.gameSpriteGroup:
            sprite.draw(self.screen)
        pygame.display.flip()


    def play(self):
        done = False
        print("Start Game cycle")
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    sys.exit()
                self.keyResponse(event)
            
            click,_,_ = pygame.mouse.get_pressed()
            if click == True:
                mouse = pygame.mouse.get_pos()
                self.mouseResponse(mouse)

            #--Game logic goes after this comment
            self.logic()

            # -- Screen background is BLACK
            self.drawScreen()

            self.clock.tick(60)




class Player(pygame.sprite.Sprite):
    
    def __init__(self, ):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("images/redRect.png"), PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = PLAYERSTARTPOS[0]
        self.rect.y = PLAYERSTARTPOS[1]
        self.xSpeed = 0
        self.ySpeed = 0
        pass
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        pass


# 16 x 10 block per map
class Map():
    
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

    def draw(self,screen):
        self.tileGroup.draw(screen)


class Tile(pygame.sprite.Sprite):

    def __init__(self,position):
        super().__init__()
        self.x = position[0]
        self.y = position[1]
    

class Ground(Tile):

    def __init__(self,position):
        super().__init__(position)
        self.image = pygame.transform.scale(pygame.image.load("images/groundTile.png"),BLOCKSIZE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class AirTile(Tile):
    
    def __init__(self,position):
        super().__init__(position)
        self.image = pygame.transform.scale(pygame.image.load("images/airTile.png"),BLOCKSIZE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y