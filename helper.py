import csv, pygame
from os import read
from mario import Game

#Global Variables / Constants
BROWN = (135, 52, 35)
SKYBLUE = (91, 148, 251)
LIGHTGREY = (213, 216, 220)
SIZE = (800,500)
BLOCKSIZE = (50,50)

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
            if row[0] == "ground":
                groundTile = Ground((row[1], row[2]))
                self.groundSpriteGroup.add(groundTile)
                self.tileGroup.add(groundTile)
            elif row[0] == "airTile":
                airTile = airTile((row[1], row[2]))
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

class Button(pygame.sprite.Sprite):

    def __init__(self,width, height, position, imageName):
        self.image = pygame.transform.scale(pygame.image.load(imageName), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def mouseInteraction(self,position):
        if position[0] >= self.position[0] and position[0] <= self.position[0] + self.width and position[1] >= self.position[1] and position[1] <= self.position[1] + self.height:
            return True
        else:
            return False

class SettingButton(Button):

    def __init__(self, width, height, position):
        super().__init__(width, height,position,"image/settingButton.png")
    
class LevelButton(Button):

    def __init__(self,name, width, height, position, imageName):
        super().__init__(width, height, position, imageName)
        self.name = name

    def mouseInteraction(self,position):
        if super().mouseInteraction(position):
            self.initialiseGame()

    def initialiseGame(self):
        pass

