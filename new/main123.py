import pygame, sys
from constants123 import *
from helper123 import *

class Main:

    def __init__(self):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.surface = pygame.display.set_caption("Mario")
        self.clock = pygame.time.Clock()
        self.done = False
        self.status = []
        self.currentScreen = MENU

        self.menu_screen = MenuScreen()
        self.setting_screen = SettingScreen()
        self.ranking_screen = RankingBoardScreen()

    def setCurrentScreen(self, screenName):
        self.currentScreen = screenName

    def keyResponse(self,event):
        if self.currentScreen == MENU:
            self.menu_screen.keyResponse(event)
        elif self.currentScreen == RANKBOARDSCREEN:
            self.ranking_screen.keyResponse(event)
        elif self.currentScreen == SETTINGSCREEN:
            self.setting_screen.keyResponse(event)
    
    def mouseResponse(self,position):
        if self.currentScreen == MENU:
            self.menu_screen.mouseResponse(position)
        elif self.currentScreen == RANKBOARDSCREEN:
            self.ranking_screen.mouseResponse(position)
        elif self.currentScreen == SETTINGSCREEN:
            self.setting_screen.mouseResponse(position)
    
    def logic(self):
        pass

    def drawScreen(self):
        if self.currentScreen == MENU:
            self.menu_screen.drawScreen(self.screen)
        elif self.currentScreen == RANKBOARDSCREEN:
            self.ranking_screen.drawScreen(self.screen)
        elif self.currentScreen == SETTINGSCREEN:
            self.setting_screen.drawScreen(self.screen)

    def gameplay(self):
        while not self.done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.keyResponse(event)

            left_click, _, _ = pygame.mouse.get_pressed()
            if left_click:
                position = pygame.mouse.get_pos()
                self.mouseResponse(position)

            self.logic()

            self.drawScreen()

class MenuScreen():

    def __init__(self):
        self.level_button_list = []
        self.menuScreen_sprite_list = []
        for i in range(3):
            levelButton = LevelButton()
            self.level_button_list.append(levelButton)
            self.menuScreen_sprite_list.append(levelButton)

    def keyResponse(self,event):
        pass

    def mouseResponse(self, position):
        pass

    def drawScreen(self, screen):
        pass

class SettingScreen():

    def __init__(self):
        pass

    def keyResponse(self,event):
        pass

    def mouseResponse(self, position):
        pass

    def drawScreen(self, screen):
        pass

class RankingBoardScreen():

    def __init__(self):
        pass

    def keyResponse(self,event):
        pass

    def mouseResponse(self, position):
        pass

    def drawScreen(self, screen):
        pass

if __name__ == '__main__':
    pygame.init()
    main = Main()
    main.gameplay()
    pygame.quit()
