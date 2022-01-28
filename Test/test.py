import pygame,math
import helper_test as ht


RED = (255,0,0)
BLACK = (0,0,0)
SIZE = width, height = (600, 400)
angle = 1

pygame.init()

screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()
img = pygame.transform.scale(pygame.image.load("invader2.png"), (50,50))
imgPos = (300,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    screen.fill(BLACK)
    rImg, origin = ht.rotateImg(screen,img,imgPos,(0,0),1)
    pygame.draw.circle(screen,RED,(300,200),10)

    pygame.display.flip()

    clock.tick(60)

    