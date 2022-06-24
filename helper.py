import csv, pygame
from os import read
from constants import *

class Button(pygame.sprite.Sprite):

    def __init__(self,width, height, position, imageName):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(imageName), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]

    def mouseInteraction(self,position, status):
        if self.rect.collidepoint(position):
            pass
        return status
    
    def keyResponse(self,event,status):
        return status

    def draw(self,screen, cam_pos = pygame.math.Vector2(0,0)):
        screen.blit(self.image, (self.rect.x,self.rect.y))


class SettingButton(Button):

    def __init__(self, width, height, position):
        super().__init__(width, height,position,"images/settingButton.png")

    def mouseInteraction(self,position, status):
        if self.rect.collidepoint(position):
            print("Setting Button mouse collide")
            status.extend(SCREENTOSETTING)
        return status
    

def relativeCoor2DeCoor(relativePosition):
    return (relativePosition[0]*BLOCKSIZE[0], relativePosition[1]*BLOCKSIZE[1])

def deCoor2RelativeCoor(dePosition):
    return (dePosition[0]/BLOCKSIZE[0], dePosition[1]/BLOCKSIZE[1])


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

#Apply a function to items in a list with optional arguments
def apply(list, func, **args):
    result = []
    argument = ""
    for key, value in args.items():
        argument = argument + ", " + str(key) +"="+str(value)
    argument = argument + ")"
    for i in list:
        com = f"x = {func}({ i }" + argument
        loc = {}
        exec(f"{com}",globals(),loc)
        x = loc["x"]
        result.append(x)
    return result

class WordButton():

    def __init__(self,width, height, position, color, textColor, txt):
        super().__init__()
        self.rect = pygame.Rect(*position, width, height)
        self.color = color
        font = pygame.font.Font("freesansbold.ttf", 20)
        self.txt = font.render(txt, True, textColor)
        self.txt_pos = position

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