from re import L
from jinja2 import pass_context
import pygame, math, sys
from helper import *
from mario import Game

#Global constant
SIZE = (800,500)
SKYBLUE = (91, 148, 251)
EXIT = "exit"
SETTINGS = (80,80)
LEVELBUTTONSIZE = (148, 40)
LEVELIMAGESIZE = (240, 168)
LEVELIMAGEBUTTONPADDING = EDGELEVELIMAGEPADDING = 16
LEVEL2LEVELPADDING = 24
NUMOFLEVELS = 3


class Main():

    def __init__(self):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.surface = pygame.display.set_caption("Mario")
        self.clock = pygame.time.Clock()
        self.all_sprites_group = pygame.sprite.Group()
        self.menu = Menu(self.screen)
        self.setting = Setting()
        self.settingButton = SettingButton()
        self.levelButtonGroup = pygame.sprite.Group()
        self.menuSpriteGroup = pygame.sprite.Group()
        self.status = ["start"]
        
        startY = self.size[1] / 2 + LEVELIMAGESIZE[1]/2 + LEVELIMAGEBUTTONPADDING
        startX = self.size[0] / 2 - LEVELIMAGESIZE[0] * 1.5 - LEVEL2LEVELPADDING + (LEVELIMAGESIZE[0] - LEVELBUTTONSIZE[0])/2

        for lvlNum in range(NUMOFLEVELS):
            levelBut = LevelButton(f"Level {lvlNum + 1}",*LEVELBUTTONSIZE,(startX,startY), "tempLevelImg.png")
            self.levelButtonGroup.add(levelBut)
            self.menuSpriteGroup.add(levelBut)
            self.all_sprites_group.add(levelBut)

    def keyResponse(self,event):
        pass

    def mouseResponse(self, position):
        pass
    
    def logic(self):
        pass

    def drawScreen(self):
        pass

    def gameplay(self):
        done = False
        while not done:


            # -- User input and controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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

        #Endwhile
        self.finishScreen()


#Menu Screen
class Menu():

    def __init__(self, screen):
        pass


# Setting Screen
class Setting():

    def __init__(self):
        pass

# Ranking Screen
class RankingScreen():

    def __init__(self):
        pass

if __name__ == "__main__":
    pygame.init()
    main = Main()
    main.gameplay()
    pygame.quit()
    
