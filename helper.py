from asyncio.windows_events import NULL
import pygame
from constants import *
from abc import ABC, abstractmethod
import os

class Button(pygame.sprite.Sprite, ABC):

    # Initialise Button as a sprite object
    def __init__(self,width, height, position, imageName):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(imageName), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    @abstractmethod
    def mouseInteraction(self,position, status):
        if self.rect.collidepoint(position):
            pass
        return status
    
    def keyResponse(self,event,status):
        return status

    def draw(self,screen, cam_pos = pygame.math.Vector2(0,0)):
        screen.blit(self.image, (self.rect.x,self.rect.y))

    def update(self):
        pass

class SettingButton(Button):

    def __init__(self, width, height, position):
        super().__init__(width, height,position,os.path.join("images","settingButton.png"))

    def mouseInteraction(self,position, status):
        if self.rect.collidepoint(position):
            print("Setting Button mouse collide")
            status.extend([SCREENTOSETTING])
        return status
    
class GameObject(pygame.sprite.Sprite, ABC):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self):
        pass


class MouseBuffer():

    def __init__(self):
        self.timer = 0
        self.flag = False
        self.frameNum = 8

    def tFlag(self):
        self.flag = True

    def logic(self):
        if self.flag:
            self.count()
        if self.timer >= self.frameNum:
            self.flag = False
            self.reset()
    
    def reset(self):
        self.timer = 0
    
    def count(self):
        self.timer +=1

class WordButton(ABC):

    def __init__(self,width, height, position, color, textColor, txt):
        super().__init__()
        self.rect = pygame.Rect(*position, width, height)
        self.color = color
        font = pygame.font.Font("freesansbold.ttf", FONTSIZE)
        self.txt = font.render(txt, True, textColor)
        fontSize = self.txt.get_size()
        self.txt_pos = (position[0] + (width - fontSize[0])/2, position[1] + (height - fontSize[1])/2)

    @abstractmethod
    def mouseInteraction(self,position, status):
        return status

    def keyResponse(self,event,status):
        return status

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        screen.blit(self.txt, self.txt_pos)

class Background(pygame.sprite.Sprite):

    def __init__(self, width, height, position, color):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(position[0], position[1], width, height)
    
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def mouseInteraction(self, position, status):
        return status

    def keyResponse(self,event,status):
        return status

class CloseButton(Button):

    def __init__(self,width, height, position, statusCode):
        super().__init__(width, height, position, os.path.join("images","closeButton.jpg"))
        self.statusCode = statusCode

    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([self.statusCode])
        return status

class QuitButton(WordButton):

    def __init__(self, position):
        super().__init__(140,40, position, (51, 51, 204), WHITE, "Exit Game")
    
    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([CLOSEGAME])
        return status
    
class InstructionButton(WordButton):

    def __init__(self, position):
        super().__init__(140,40, position, (51, 51, 204), WHITE, "Instructions")
    
    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            print("Instruction clicked")
            status.append(SCREENTOINSTRUCTION)
        return status

class QuitGameButton(WordButton):

    def __init__(self, position):
        super().__init__(140, 40, position, (51, 51, 204), WHITE, "Quit Game") 

    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([EXITGAME])
        return status

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
    
    def player_interaction(self, **args):
        pass
    

class Ground(Tile):

    def __init__(self,position):
        super().__init__(position, os.path.join("images","groundTile.png"))

class AirTile(Tile):
    
    def __init__(self,position):
        super().__init__(position,os.path.join("images","airTile.png"))

class InstructionScreen():

    def __init__(self, closeStatusCode):
        self.instructions = [
            " 'A' key for going to the left ",
            " 'D' key for going to the right",
            " 'W' key for jumping",
            " 'SPACE' key for shooting"
        ]
        self.fonts = []
        font = pygame.font.Font("freesansbold.ttf", FONTSIZE)
        start_y = 108
        for instruction in self.instructions:
            txt = font.render(instruction, True, BLACK)
            fontSize = txt.get_size()
            txt_pos = (76 + (648 - fontSize[0])/2, start_y + INSTRUCTION_MENU_PADDING)
            start_y += fontSize[1] + INSTRUCTION_MENU_PADDING * 2
            self.fonts.append((txt,txt_pos))
        self.background = Background(648,336,(76, 64), SETTINGSCREENCOLOR)
        self.closeButton = CloseButton(24,24, (712, 52), closeStatusCode)
        self.instruction_sprite_group = [self.background, self.closeButton]

    def mouseInteraction(self, position, status):
        return self.closeButton.mouseInteraction(position, status)

    def keyResponse(self,event,status):
        return status
    
    def drawScreen(self, screen):
        for sprite in self.instruction_sprite_group:
            sprite.draw(screen)
        for txt, txt_pos in self.fonts:
            screen.blit(txt, txt_pos)

class RestartButton(WordButton):

    def __init__(self, position):
        super().__init__(140,40, position, (51, 51, 204), WHITE, "Restart")
    
    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([RESTARTGAME])
        return status

def xReToDe(x_pos):
    return int(x_pos)*BLOCKSIZE[0]

def yReToDe(y_pos):
    return int(y_pos)*BLOCKSIZE[1]

def relativeCoor2DeCoor(relativePosition):
    return (xReToDe(relativePosition[0]), yReToDe(relativePosition[1]))

def deCoor2RelativeCoor(dePosition):
    return (dePosition[0]/BLOCKSIZE[0], dePosition[1]/BLOCKSIZE[1])
            

#Apply a function to items in a list with optional arguments
def apply(list, func, **args):
    result = []
    argument = ""
    for key, value in args.items():
        argument = argument + ", " + str(key) +"="+str(value)
    argument = argument + ")"
    for i in list:
        com = f"x = {func.__name__}({ i }" + argument
        loc = {}
        exec(f"{com}",globals(),loc)
        x = loc["x"]
        result.append(x)
    return result

# Level status code
def create_level_status_code(level):
    return f"Initialise Level {level}"

def check_status_init_level(string):
    return bool(re.match("^(Initialise Level)\s\-?[0-9]+$", string))

def extract_level_from_status_code(status_code):
    if not check_status_init_level(status_code):
        return None
    try:
        return int(status_code.split(" ")[-1])

    except ValueError:
        return None

class Spike:
    def __init__(self, position, base, height):
        self.x = position[0]
        self.y = position[1]
        self.base = base
        self.height = height
        self.rect_group = []
        self.createRect()

    def createRect(self):
        base_change = self.base / 40
        height_change = self.height / 20
        base_length = self.base - base_change*2
        left = self.x + base_change
        top = self.y + self.height-height_change
        for i in range(19):
            rect = pygame.Rect(left, top, base_length, height_change)
            self.rect_group.append(rect)
            base_length -= base_change*2
            left += base_change
            top -= height_change

    def draw(self,screen, cam_position):
        for rect in self.rect_group:
            pygame.draw.rect(screen,SILVER, pygame.Rect(rect.left - cam_position.x, rect.top - cam_position.y, rect.width, rect.height))

    def logic(self):
        pass

    def player_interaction(self,player_rect):
        pass

class ActivateObjects(ABC):

    def __init__(self,zone):
        self.zone = pygame.Rect(*zone)
        self.activate = False

    def detect(self, player_rect):
        if player_rect.colliderect(self.zone):
            self.activate = True

    def logic(self):
        pass

    @abstractmethod
    def player_interaction(self,player_rect):
        pass

class SpikeUp(Spike, ActivateObjects):

    def __init__(self, position, base, height, zone, up, hori_dir = 0): #zone = (leftx, rightx, width, height)
        temp_pos = (position[0], position[1])
        Spike.__init__(self, temp_pos, base, height)
        ActivateObjects.__init__(self,zone)
        self.tar_y = position[1] - up*BLOCKSIZE[1]
        self.up = up
        self.hori_dir = hori_dir
        self.tar_x = position[0] + hori_dir * BLOCKSIZE[0]

    def player_interaction(self, player_rect):
        if not self.activate:
            self.detect(player_rect)
        if self.activate and player_rect.collidelist(self.rect_group) != -1:
            return True
        return False

    def logic(self):
        if self.activate and self.y > self.tar_y and self.up > 0:
            self.y -= UP_SPEED
            for rect in self.rect_group:
                rect.y -= UP_SPEED
        elif self.activate and self.y < self.tar_y and self.up < 0:
            self.y += UP_SPEED
            for rect in self.rect_group:
                rect.y += UP_SPEED
        if self.activate and self.x < self.tar_x and self.hori_dir > 0:
            self.x += HORI_SPEED
            for rect in self.rect_group:
                rect.x += HORI_SPEED
        elif self.activate and self.x > self.tar_x and self.hori_dir < 0:
            self.x -= HORI_SPEED
            for rect in self.rect_group:
                rect.x -= HORI_SPEED

    def draw(self,screen, cam_position):
        #pygame.draw.rect(screen, YELLOW, pygame.Rect(self.zone.left - cam_position.x, self.zone.top-cam_position.y, self.zone.width, self.zone.height))
        super().draw(screen, cam_position)

class Appear_block(ActivateObjects, Ground):

    def __init__(self,position):
        ActivateObjects.__init__(self, (position[0]-10, position[1]-10, BLOCKSIZE[0]+20, BLOCKSIZE[1]+20))
        Ground.__init__(self,position)
    
    def draw(self, screen, cam_pos):
        if self.activate:
            screen.blit(self.image, (self.rect.x - cam_pos.x, self.rect.y))
        
    def player_interaction(self,player_rect):
        if not self.activate:
            self.detect(player_rect)

class DisappearBlock(ActivateObjects, Ground):

    def __init__(self,position):
        ActivateObjects.__init__(self, (position[0]- 3, position[1]- 3, BLOCKSIZE[0] + 6, BLOCKSIZE[1] + 6))
        Ground.__init__(self,position)
        self.rect = NULL
        self.position = position
    
    def draw(self, screen, cam_pos):
        if not self.activate:
            screen.blit(self.image, (self.position[0] - cam_pos.x, self.position[1]))

    def player_interaction(self,player_rect):
        if not self.activate:
            self.detect(player_rect)

class GrowSpike(Spike, ActivateObjects):

    def __init__(self, position, base, height, zone, up, hori):
        Spike.__init__(self, position, base, height)
        ActivateObjects.__init__(self,zone)
        self.tar_height = height*up
        self.tar_base = hori * base

    def player_interaction(self, player_rect):
        if not self.activate:
            self.detect(player_rect)
        if self.activate and player_rect.collidelist(self.rect_group) != -1:
            return True
        return False
    
    def logic(self):
        flag = False
        if self.activate and self.height < self.tar_height:
            self.height += GROW_SPEED
            self.y -= GROW_SPEED
            flag = True
        if self.activate and self.base < self.tar_base:
            self.base += GROW_SPEED
            self.x -= GROW_SPEED /2
            flag = True
        if flag:
            self.rect_group = []
            base_change = self.base / 40
            height_change = self.height / 20
            base_length = self.base - base_change*2
            left = self.x + base_change
            top = self.y + self.height-height_change
            for i in range(19):
                rect = pygame.Rect(left, top, base_length, height_change)
                self.rect_group.append(rect)
                base_length -= base_change*2
                left += base_change
                top -= height_change
    
    def draw(self,screen, cam_position):
        #pygame.draw.rect(screen, YELLOW, pygame.Rect(self.zone.left - cam_position.x, self.zone.top-cam_position.y, self.zone.width, self.zone.height))
        super().draw(screen, cam_position)

class Check_point(Tile, ActivateObjects):

    def __init__(self, position):
        Tile.__init__(self, position, os.path.join("images","respawn_before.png"))
        ActivateObjects.__init__(self, (position[0]-10, position[1]-10, BLOCKSIZE[0] + 20, BLOCKSIZE[1] + 20))

    def player_interaction(self,player_rect):
        if player_rect.colliderect(self.zone):
            self.image = pygame.transform.scale(pygame.image.load(os.path.join("images","respawn.png")), BLOCKSIZE)
            return [self.x, self.y +18]

class HorizontalSpike():
    def __init__(self, position, base, height):
        self.x = position[0]
        self.y = position[1]
        self.base = base
        self.height = height
        self.rect_group = []
        self.createRect()

    def createRect(self):
        base_change = self.base / 40
        height_change = self.height / 20
        base_length = self.base - base_change*2
        left = self.x 
        top = self.y + height_change
        for i in range(19):
            rect = pygame.Rect(left, top, height_change, base_length)
            self.rect_group.append(rect)
            base_length -= base_change*2
            left += height_change
            top += base_change

    def draw(self,screen, cam_position):
        for rect in self.rect_group:
            pygame.draw.rect(screen,SILVER, pygame.Rect(rect.left - cam_position.x, rect.top - cam_position.y, rect.width, rect.height))

    def logic(self):
        pass

    def player_interaction(self,player_rect):
        pass

class MoveableHoriSpike(HorizontalSpike, SpikeUp):

    def __init__(self, position, base, height, zone, up, hori_dir = 0):
        print( position, base, height, zone, up, hori_dir)
        SpikeUp.__init__(self, position, base, height, zone, up, hori_dir)
        HorizontalSpike.__init__(self,position, base, height)

    def draw(self,screen, cam_position):
        #pygame.draw.rect(screen, YELLOW, pygame.Rect(self.zone.left - cam_position.x, self.zone.top-cam_position.y, self.zone.width, self.zone.height))
        HorizontalSpike.draw(self,screen, cam_position)

    def player_interaction(self,player_rect):
        SpikeUp.player_interaction(self,player_rect)
    
    def logic(self):
        SpikeUp.logic(self)

class Bullet(GameObject):
    
    def __init__(self, direction, position):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "redRect.png")), BULLET_SIZE)
        self.rect = self.image.get_rect()
        self.direction = direction
        self.rect.x = position[0]
        self.rect.y = position[1]
    
    def update(self, tiles):
        self.rect.x += self.direction * BULLET_SPEED
        if len(pygame.sprite.spritecollide(self, tiles, False)) != 0:
            self.kill()
    
    def draw(self, screen, cam_position):
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))

