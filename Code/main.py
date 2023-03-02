import sys

import pygame

from constants import *
from helper import *
from mario import Game

import sqlite3

con = sqlite3.connect("data.db", check_same_thread=False)
db = con.cursor()

class Main:

    def __init__(self):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Mario")
        self.clock = pygame.time.Clock()
        self.all_sprites_list = []
        self.currentScreen = MENU
        self.player_name = ""

        # Objects
        self.menu = Menu(self.screen)
        self.setting = MenuSettingScreen()
        self.instructionScreen = InstructionScreen(SCREENTOGAMEMENU)
        self.rankingScreen = RankingScreen(SCREENTOGAMEMENU)
        
        self.all_sprites_list.extend([self.menu, self.setting])

        # Sprite Groups
        self.status = []
        

    def keyResponse(self,event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.status.append(create_level_status_code(1))
            elif event.key == pygame.K_2:
                self.status.append(create_level_status_code(2))

    # Change status (Task pending to do)
    def mouseResponse(self, position: tuple, click):
        if self.currentScreen == MENU:
            self.status = self.menu.mouseInteraction(position, self.status, click)
        elif self.currentScreen == SETTINGSCREEN:
            self.status = self.setting.mouseInteraction(position, self.status, click)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.status = self.instructionScreen.mouseInteraction(position, self.status, click)
        elif self.currentScreen == RANKINGSCREEN:
            self.status = self.rankingScreen.mouseInteraction(position, self.status, click)
    
    
    def setCurrentScreen(self, newScreen: str):
        self.currentScreen = newScreen

    def initialiseGame(self, level: int):
        game = Game(level)
        restart, respawn_checkpoint, check_point, death_count, time_count, record = game.play()
        if record:
            db.execute(f"INSERT INTO Entries (name, time, deaths, level) VALUES ('{self.player_name}', {time_count}, {death_count}, {level});")
            con.commit()
            death_count = 0
            time_count = 0
        elif not respawn_checkpoint:
            death_count = 0
            time_count = 0
        while restart:
            game = Game(level, respawn = respawn_checkpoint, check_point = check_point, death_count = death_count, time_count = time_count)
            restart, respawn_checkpoint, check_point, death_count, time_count, record = game.play()
            if record:
                db.execute(f"INSERT INTO Entries (name, time, deaths, level) VALUES ('{self.player_name}', {time_count}, {death_count}, {level});")
                con.commit()
                death_count = 0
                time_count = 0
            elif not respawn_checkpoint:
                death_count = 0
                time_count = 0  
            


    def readStatus(self):
        for stat in self.status:
            # Change to menu screen
            if stat == SCREENTOSETTING:
                self.setCurrentScreen(SETTINGSCREEN)

            # Change to setting screen
            elif stat == SCREENTOGAMEMENU:
                self.setCurrentScreen(MENU)

            # Initialise game
            elif check_status_init_level(stat):
                level = extract_level_from_status_code(stat)
                self.initialiseGame(level)

            # Exit game
            elif stat == EXITGAME:
                sys.exit()

            # Change to instruction screen
            elif stat == SCREENTOINSTRUCTION:
                self.setCurrentScreen(INSTRUCTIONSCREEN)
            
            elif stat == SCREENTORANKING:
                self.rankingScreen.refresh()
                self.setCurrentScreen(RANKINGSCREEN)

        self.status = []

    def logic(self):    
        pass

    def drawScreen(self):
        self.screen.fill(BROWN)
        if self.currentScreen == MENU:
            self.menu.drawScreen(self.screen)
        elif self.currentScreen == SETTINGSCREEN:
            self.setting.drawScreen(self.screen)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.instructionScreen.drawScreen(self.screen)
        elif self.currentScreen == RANKINGSCREEN:
            self.rankingScreen.drawScreen(self.screen)
        
        pygame.display.flip()

    def gameplay(self):
        self.inputName()
        
        done = False
        while not done:


            # -- User input and controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.keyResponse(event)
                
            click,_,_ = pygame.mouse.get_pressed()
            mouse = pygame.mouse.get_pos()
            self.mouseResponse(mouse,click)

            self.readStatus()
            
            #--Game logic goes after this comment
            self.logic()


            # -- Screen background is BLACK
            self.drawScreen()


            self.clock.tick(60)

        #Endwhile
        self.finishScreen()

    def inputName(self):
        self.font = pygame.font.Font("freesansbold.ttf",100)
        self.nameStr = self.font.render("Name: ", True, WHITE)
        self.nameStr_pos = (182, 80)
        self.name_pos = (182, 80 + self.nameStr.get_size()[1])
        temp_name = ""
        done = False
        while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN and temp_name != "":
                            self.player_name = temp_name
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            temp_name = temp_name[:-1]
                        elif event.unicode.isalpha():
                            temp_name += event.unicode
                        
            self.screen.fill(BROWN)
            self.screen.blit(self.nameStr, self.nameStr_pos)
            self.screen.blit(self.font.render(temp_name, True, WHITE), self.name_pos)
            pygame.display.flip()

#Menu Screen
class Menu():

    def __init__(self, screen: pygame.Surface):
        self.size = SIZE
        self.screen = screen
        self.menuSpriteGroup = []
        self.levelButtonGroup = []

        self.settingButton = SettingButton(*SETTINGS_BUTTON_SIZE, (SIZE[0] - 132, 20))
        self.menuSpriteGroup.append(self.settingButton)
        
        startY = 120 + LEVEL_IMAGE_SIZE[1] + LEVEL_IMAGE_BUTTON_PADDING
        startX = (SIZE[0] - NUM_OF_LEVELS * LEVEL_IMAGE_SIZE[0] + (NUM_OF_LEVELS - 1) * LEVEL_IMAGE_BUTTON_PADDING)/2
        self.img1 = pygame.transform.scale(pygame.image.load(os.path.join("images", "Level1.png")), (240, 168))
        self.img2 = pygame.transform.scale(pygame.image.load(os.path.join("images", "Level2.png")), (240, 168))
        self.img1_pos = ((SIZE[0] - NUM_OF_LEVELS * LEVEL_IMAGE_SIZE[0] + (NUM_OF_LEVELS - 1) * LEVEL_IMAGE_BUTTON_PADDING)/2 - 46,120)
        self.img2_pos = (self.img1_pos[0] + LEVEL_2_LEVEL_PADDING + LEVEL_IMAGE_SIZE[0],120)


        for lvlNum in range(NUM_OF_LEVELS):
            levelBut = LevelButton(lvlNum+1, f"Level {lvlNum + 1}",*LEVEL_BUTTON_SIZE,(startX,startY))
            self.levelButtonGroup.append(levelBut)
            startX += LEVEL_2_LEVEL_PADDING + LEVEL_IMAGE_SIZE[0]

    # Return new status
    def mouseInteraction(self, position: tuple, status: list, click: bool):
        for sprite in self.menuSpriteGroup:
            status = sprite.mouseInteraction(position, status, click)
        for but in self.levelButtonGroup:
            status = but.mouseInteraction(position, status, click)
        return status

    def drawScreen(self,screen: pygame.Surface):
        self.settingButton.draw(screen)
        for sprite in self.menuSpriteGroup:
            sprite.draw(screen)
        for but in self.levelButtonGroup:
            but.draw(screen)
        screen.blit(self.img1, self.img1_pos)
        screen.blit(self.img2, self.img2_pos)

class LevelButton(WordButton):

    def __init__(self,level: int, name: str, width: int, height: int, position: tuple[int]):
        super().__init__(width, height, position, WHITE, BLACK, "Level "+str(level), create_level_status_code(level))
        self.name = name
        self.level = level


# Setting Screen
class MenuSettingScreen:

    def __init__(self):
        self.background = Background(648,336,(76, 64), SETTINGSCREENCOLOR)
        self.closeButton = CloseButton(24,24, (712, 52), SCREENTOGAMEMENU)
        self.exitButton = QuitGameButton((331, 306))
        self.controlButton = InstructionButton((331,118))
        self.rankingButton = RankScreenButton((331,218))
        self.gameMenu_sprite_group = [self.background, self.closeButton, self.exitButton,self.controlButton, self.rankingButton]

    def drawScreen(self, screen: pygame.Surface):
        for sprite in self.gameMenu_sprite_group:
            sprite.draw(screen)

    def mouseInteraction(self,position: tuple, status: list[str], click):
        for sprite in self.gameMenu_sprite_group:
            status = sprite.mouseInteraction(position, status, click)
        return status

    def keyResponse(self,event: pygame.event, status: list[str]):
        for sprite in self.gameMenu_sprite_group:
            status = sprite.keyResponse(event, status)
        return status

class RankingScreen:
    
    def __init__(self, closeStatusCode: str):
        self.font = pygame.font.Font("freesansbold.ttf", FONTSIZE)
        self.background = Background(648,336,(76, 64), SETTINGSCREENCOLOR)
        self.closeButton = CloseButton(24,24, (712, 52), closeStatusCode)
        self.instruction_sprite_group = [self.background, self.closeButton]
        self.background = pygame.Rect(134,114,532,237)
        self.refresh()
        
    def mouseInteraction(self, position: tuple, status: list, click):
        return self.closeButton.mouseInteraction(position, status, click)

    def keyResponse(self,event: pygame.event, status: list):
        return status

    def refresh(self):
        res1 = db.execute("SELECT Name, Time, Deaths, level FROM Entries WHERE level = 1 ORDER BY Time, Deaths ASC").fetchall()[0:3]
        res2 = db.execute("SELECT Name, Time, Deaths, level FROM Entries WHERE level = 2 ORDER BY Time, Deaths ASC").fetchall()[0:3]
        self.whitebox = []
        for i in range(7):
            self.whitebox.extend([pygame.Rect(139, 119 + i * 33, 267, 28), pygame.Rect(411, 119 + i * 33, 80, 28), pygame.Rect(496, 119 + i * 33, 80, 28), pygame.Rect(581, 119  + i * 33, 80, 28)])
        self.txt = [self.font.render("Name",True, BLACK), self.font.render("Time",True, BLACK), self.font.render("Deaths",True, BLACK), self.font.render("level",True, BLACK)]
        self.txt.extend([self.font.render(str(item), True, BLACK) for sub in res1 for item in sub])
        self.txt.extend([self.font.render(str(item), True, BLACK) for sub in res2 for item in sub])
    def drawScreen(self, screen: pygame.Surface):
        for sprite in self.instruction_sprite_group:
            sprite.draw(screen)
        for txt, rect in zip(self.txt, self.whitebox):
            pygame.draw.rect(screen, WHITE, rect, 0)
            screen.blit(txt, (rect.left + 5, rect.top + 4))

if __name__ == "__main__":
    pygame.init()
    main = Main()
    main.gameplay()
    pygame.quit()
    
