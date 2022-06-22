from re import L
import pygame, math
from helper import *
from mario import Game

#Global constant
SIZE = (800,500)
SKYBLUE = (91, 148, 251)
EXIT = "exit"
SETTINGS = (80,80)
NUMOFLEVELS = 3


class Main():

    def __init__(self):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.surface = pygame.display.set_caption("Mario")
        self.clock = pygame.time.Clock()
        self.all_sprites_group = pygame.sprite.Group()
        self.menu = Menu(self.screen)
        self.scoreBoard = Scoreboard()
        player = Player(YELLOW, 10, 10)
        self.player_group.add(player)
        self.all_sprites_group.add(player)
        self.generate(NUMOFINVADERS)
        self.victory = False
        self.invader_group_hspeed = 1
        self.invader_changeDirection = False

class Level():
    
    def __init__(self,mapFile):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.surface = pygame.display.set_caption("Game 1")
        self.clock = pygame.time.Clock()
        self.allSpriteGroup = pygame.sprite.Group()
        self.map = Map(mapFile) 
        self.events = []
        self.progress = 0


    def play(self):
        done =False
        while not done:
            self.

class Game():

    def __init__(self,screen, clock, level = 1):
        self.size = SIZE
        self.screen = screen
        self.clock = clock
        self.menu = Menu(self.screen,NUMOFLEVELS)
        self.map = Map("map" +level +".csv")

    def rungame(self):
        done = False
        while not done:

            #self.menu.interaction()
            self.draw()
    
    def draw(self):
        self.map.draw()
        #self.menu.draw()



class Menu():

    def __init__(self,screen,numOfLvl):
        self.screen = screen
        self.menuSpriteGroup = pygame.sprite.SpriteGroup()
        self.settingButton = SettingButton(*SETTINGS)
        self.menuSpriteGroup.add(self.settingButton)
        self.levels = []
        self.parseLevels(numOfLvl)
        
    def parseLevels(self,numOfLvl):
        if numOfLvl == 0:
            raise ValueError
        width = SIZE[0]-SETTINGS[0] / 3
        height = SIZE[1]/(math.ceil(numOfLvl/3))
        for i in range(numOfLvl):
            tempLevel = LevelButton(f"Level {i+1}", width, height,(i%3*width,i//3*height))
            self.levels.append(tempLevel)
            self.menuSpriteGroup.add(tempLevel)
        


    def interaction(self):

        click,_,_ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
    
    def draw(self):
        self.menuSpriteGroup.draw()



def rungame():
    pygame.init()

    game = Game()
    game.rungame()

def main():
    rungame()

if __name__ == "__main__":
    #main()
    pygame.init()
    
