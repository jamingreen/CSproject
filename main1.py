from re import L
from jinja2 import pass_context
import pygame, math, sys, re
from helper import *
from mario import Game
from constants import *


class Main():

    def __init__(self):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.surface = pygame.display.set_caption("Mario")
        self.clock = pygame.time.Clock()
        self.all_sprites_list = []
        self.mouseBuffer = MouseBuffer()
        self.currentScreen = MENU
        #self.settingScreen = MenuSettingScreen()

        # Objects
        self.menu = Menu(self.screen)
        self.setting = MenuSettingScreen()
        
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

    def initialiseGame(self, level):
        game = Game(level)
        game.play()

    def readStatus(self):
        for stat in self.status:
            if stat == SCREENTOSETTING:
                self.setCurrentScreen(SETTINGSCREEN)
            elif stat == SCREENTOGAMEMENU:
                self.setCurrentScreen(MENU)
            elif check_status_init_level(stat):
                level = extract_level_from_status_code(stat)
                self.initialiseGame(level)
            elif stat == EXITGAME:
                sys.exit()
        self.status = []

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
                
            click,_,_ = pygame.mouse.get_pressed()
            if click == True and not self.mouseBuffer.flag:
                self.mouseBuffer.tFlag()
                print("Left click")
                mouse = pygame.mouse.get_pos()
                self.mouseResponse(mouse)

            print(self.status)
            self.readStatus()
            
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

class LevelButton(Button):

    def __init__(self,level, name, width, height, position, imageName):
        super().__init__(width, height, position, imageName)
        self.name = name
        self.level = level

    def mouseInteraction(self,position, status):
        if self.rect.collidepoint(position):
            print("Level button mouse collide")
            status.extend([create_level_status_code(self.level)])
        return status

# Ranking Screen
class RankingScreen():

    def __init__(self):
        pass

    def mouseInteraction(self,position, status):
        pass

    def drawScreen(self, screen):
        pass

# Setting Screen
class MenuSettingScreen:

    def __init__(self):
        self.background = Background(648,336,(76, 64), SETTINGSCREENCOLOR)
        self.closeButton = CloseButton(24,24, (712, 52), SCREENTOGAMEMENU)
        self.exitButton = QuitGameButton((331, 278))
        self.controlButton = ControlButton((331,158))
        self.gameMenu_sprite_group = [self.background, self.closeButton, self.exitButton,self.controlButton]

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

class InstructionScreen():

    def __init__(self):
        pass

    def mouseInteraction(self, position, status):
        return status

    def keyResponse(self,event,status):
        return status

if __name__ == "__main__":
    pygame.init()
    main = Main()
    main.gameplay()
    pygame.quit()
    
