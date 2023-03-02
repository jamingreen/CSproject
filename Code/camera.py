import pygame

from constants import *

vec = pygame.math.Vector2

class Camera:

    def __init__(self,player, vertices: list):
        # The edges of the camera
        self.vertices = vertices
        
        self.player = player
        
        # The position of the camera
        self.position = vec(0,0)
        self.screenW, self.screenH = SIZE
        self.left_padding = PLAYER_LEFT_PADDING
        self.right_padding = PLAYER_RIGHT_PADDING

        self.position.x = self.player.rect.x - self.left_padding
        self.position.x = max(self.vertices[0], self.position.x)
        self.position.x = min(self.vertices[1] - self.screenW, self.position.x)
        self.position.x = int(self.position.x)

    def scroll(self):
        # If the player coordinate is smaller than the left padding relative to the camera
        if self.player.rect.x < self.position.x + self.left_padding:
            # Set the position fo the camera so that the player is on the left padding unless the camera reaches the edge of the level
            self.position.x = self.player.rect.x - self.left_padding
            self.position.x = max(self.vertices[0], self.position.x) 
            
        # If the player coordinate is larger than the right padding relative to the camera
        elif self.player.rect.x > self.position.x + self.screenW - self.right_padding:
            # Set the position fo the camera so that the player is on the right padding unless the camera reaches the edge of the level
            self.position.x = self.player.rect.x + self.right_padding - self.screenW
            self.position.x = min(self.vertices[1] - self.screenW, self.position.x)
