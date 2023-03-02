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

    def draw(self,screen):
        screen.blit(self.image, (self.rect.x,self.rect.y))


class SettingButton(Button):

    def __init__(self, width, height, position):
        super().__init__(width, height,position,"images/settingButton.png")

    def mouseInteraction(self,position: tuple, status: list):
        """

        Args:
            position (tuple): The position 
            status (list): _description_

        Returns:
            _type_: _description_
        """
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