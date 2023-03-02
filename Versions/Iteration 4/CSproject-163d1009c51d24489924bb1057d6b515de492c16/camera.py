import pygame
from constants import * 
vec = pygame.math.Vector2

class Camera:

    def __init__(self,player, vertices):
        self.vertices = vertices
        self.player = player
        self.position = vec(0,0)
        self.position_float = vec(0,0)
        self.screenW, self.screenH = SIZE
        self.left_padding = PLAYER_LEFT_PADDING
        self.right_padding = PLAYER_RIGHT_PADDING

    def scroll(self):
        self.position.x = self.player.rect.x - self.left_padding
        self.position.x = max(self.vertices[0], self.position.x)
        self.position.x = min(self.vertices[1] - self.screenW, self.position.x)
        self.position.x = int(self.position.x)
