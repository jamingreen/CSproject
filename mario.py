import pygame, math, sys, csv, os
from pygame import math
from constants import *
from camera import *
from helper import *
import numpy as np

class Game:
    
    def __init__(self, level = 1, respawn = False, check_point = None):
        self.size = SIZE
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.map = Map(os.path.join("files","map" +str(level) +".csv"))
        self.level = level
        self.menu_button = MenuButton()
        self.status = []
        self.menuScreen = GameMenuScreen()
        self.done = False
        self.mouseBuffer = MouseBuffer()
        self.instruction_screen = InstructionScreen(RETURNTOGAME)
        self.game_board = GameBoard()
        self.currentScreen = GAME
        self.restart = False
        self.death_text = DeathText()
        self.death_count = 0
        self.death_count_start = False
        

        self.gameSpriteGroup = []
        self.respawn_checkpoint = True
        if respawn:
            self.check_point = check_point
        else:
            self.check_point = self.map.player_start_pos

        self.player = Player(HORIZONAL_MAX_SPEED, self.map.vertices, self.check_point)
        self.camera = Camera(self.player, self.map.vertices)
        self.enemy_sprite_group = pygame.sprite.Group()

        self.gameSpriteGroup.extend([self.menu_button])

        self.parseEntities(os.path.join("files","entity"+str(level)+".csv"))
        self.trap_group = TrapGroup(os.path.join("files","trap"+str(level)+".csv"))
        self.gameSpriteGroup.extend([self.trap_group, self.game_board])
        print(globals())

    def parseEntities(self, filename):
        with open(filename, 'r') as f:
            reader =  csv.reader(f)
            next(reader)

            for row in reader:
                self.create_enemies(row)
        self.gameSpriteGroup.extend(self.enemy_sprite_group)

    def create_enemies(self, row):
        position = relativeCoor2DeCoor((int(row[1]), int(row[2])))
        x_boundary = tuple(apply(row[3].split("|"), xReToDe))
        y_boundary = tuple(apply(row[4].split("|"), yReToDe))
        if row[0] == "goomba":
            temp = Goomba(position, x_boundary, y_boundary)
            self.enemy_sprite_group.add(temp)

    def gameResponse(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.death_count_start:
                self.done = True
                self.restart = True

    def keyResponse(self, event):
        if self.currentScreen == GAMEMENU:
            self.status = self.menuScreen.keyResponse(event,self.status)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.status = self.instruction_screen.keyResponse(event, self.status)
        elif self.currentScreen == GAME:
            self.status = self.player.keyResponse(event, self.status)
        self.gameResponse(event)

    def mouseResponse(self, position):
        self.status = self.menu_button.mouseInteraction(position, self.status)
        if self.currentScreen == GAMEMENU:
            self.status = self.menuScreen.mouseInteraction(position, self.status)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.status = self.instruction_screen.mouseInteraction(position, self.status)

    def readStatus(self):
        for stat in self.status:
            if stat == SCREENTOGAMEMENU:
                self.currentScreen = GAMEMENU
            elif stat == CLOSEGAME:
                self.done = True
            elif stat == RETURNTOGAME:
                self.currentScreen = GAME
            elif stat == SCREENTOINSTRUCTION:
                self.currentScreen = INSTRUCTIONSCREEN
            elif stat == RESTARTGAME:
                self.done = True
                self.restart = True
                self.respawn_checkpoint = False
            elif stat == PLAYERDEATH:
                self.currentScreen = DEATHSCREEN
                self.death_count_start = True
        self.status = []

            
    def logic(self):
        self.readStatus()
        self.mouseBuffer.logic()
        self.playerdeath()
        if self.currentScreen == GAME:
            temp = self.player.update(self.map.tileGroup, self.map.dead_zone, self.status,self.enemy_sprite_group, self.trap_group)
            if temp != None:
                self.status.append(temp)
            self.camera.scroll()
            for tile in self.map.respawn_group:
                res = tile.player_interaction(player_rect = self.player.rect)
                if res != None:
                    self.check_point = res
            
            for tile in self.map.tileGroup:
                tile.player_interaction(player_rect = self.player.rect)

            self.trap_group.logic()

            for enemy in self.enemy_sprite_group:
                enemy.update()
                if enemy.hp <= 0:
                    enemy.kill()
                    self.gameSpriteGroup.remove(enemy)
                    
                
            self.game_board.logic()

    def drawScreen(self):
        self.screen.fill(SKYBLUE)

        # -- Draw here
        for sprite in self.gameSpriteGroup:
            sprite.draw(self.screen, self.camera.position)
        self.map.draw(self.screen, self.camera.position)
        self.player.draw(self.screen, self.camera.position)
        
        # Draw menu screen on top
        if self.currentScreen == GAMEMENU:
            self.menuScreen.drawScreen(self.screen)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.instruction_screen.drawScreen(self.screen)
        elif self.currentScreen == DEATHSCREEN:
            self.death_text.draw(self.screen)

        pygame.display.flip()

    def playerdeath(self):
        if self.death_count_start:
            self.death_count +=1
        if self.death_count >= 200:
            self.done = True
            self.restart = True
            self.respawn_checkpoint  = True

    def play(self):
        self.done = False
        print("Start Game cycle")
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    sys.exit()
                self.keyResponse(event)
            click,_,_ = pygame.mouse.get_pressed()
            if click == True and not self.mouseBuffer.flag:
                self.mouseBuffer.tFlag()
                mouse = pygame.mouse.get_pos()
                self.mouseResponse(mouse)

            #--Game logic goes after this comment
            self.logic()

            self.drawScreen()
            print("_____________")
            self.clock.tick(60)
        return self.restart, self.respawn_checkpoint, self.check_point

class Player(pygame.sprite.Sprite):
    
    def __init__(self, horizonal_max_speed, vertices, start_pos):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "redRect.png")), PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.xSpeed = 0
        self.ySpeed = 0
        self.left_border = vertices[0]
        self.right_border = vertices[1] - PLAYER_SIZE[0] # right most of the map
        self.horizonal_max_speed = horizonal_max_speed
        self.on_ground = True
        self.health = 100
        self.face_direction = 1
        
        
        self.bullet_group = pygame.sprite.Group()
        self.bullet_timer = 0
        self.bullet_available = True
    
    def draw(self, screen, cam_position):
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))
        for bullet in self.bullet_group:
            bullet.draw(screen, cam_position)

    def set_speed_x(self, speed):
        self.xSpeed = speed

    def shoot_bullet(self):
        if self.bullet_available:
            bullet = Bullet(self.face_direction, self.rect.center)
            self.bullet_group.add(bullet)
            self.bullet_available = False

    def shoot_timer(self):
        if not self.bullet_available:
            self.bullet_timer += 1
        if self.bullet_timer >= BULLET_TIMER:
            self.bullet_available = True
            self.bullet_timer = 0

    def bullet_enemy_interaction(self, enemies):
        for enemy in enemies:
            hits = pygame.sprite.spritecollide(enemy, self.bullet_group, False)
            enemy.change_hp(-len(hits) * BULLET_DAMAGE)
            for bu in hits:
                bu.kill()

    def jump(self): 
        if self.on_ground:
            self.jump_num = 1
            self.on_ground = False
            self.ySpeed = -JUMP_SPEED
        elif self.jump_num > 0:
            self.jump_num -= 1
            self.on_ground = False
            self.ySpeed = -JUMP_SPEED

    def jumpBuffer(self):
        pass

    def movementX(self):
        self.rect.x += self.xSpeed 

        # boarder collision
        self.rect.x = min(self.rect.x, self.right_border)
        self.rect.x = max(self.rect.x, self.left_border)
    
    def movementY(self):
        self.rect.y += self.ySpeed
        self.ySpeed += GRAVITY
        
    def collisionX(self, tiles):

        # move right
        if self.xSpeed > 0:
            for tile in tiles:
                self.rect.x = min(tile.rect.x - PLAYER_SIZE[0], self.rect.x)
        elif self.xSpeed < 0:
            for tile in tiles:
                self.rect.x = max(tile.rect.right, self.rect.x)

    def collisionY(self, tiles):
        if self.ySpeed > 0:
            self.on_ground = True
            for tile in tiles:
                self.rect.y = min(tile.rect.top - PLAYER_SIZE[1], self.rect.y)

        elif self.ySpeed < 0:
            for tile in tiles:
                self.rect.y = max(tile.rect.bottom, self.rect.y)
        self.ySpeed = 0

    def enemy_interaction(self,enemy_sprite_group, trap_group):
        for enemy in enemy_sprite_group:
            if type(enemy) == Goomba:
                if pygame.sprite.collide_rect(self, enemy):
                    return PLAYERDEATH
        for trap in trap_group.all_trap_group:
            if type(trap) in [Spike, SpikeUp,GrowSpike, HorizontalSpike,MoveableHoriSpike]:
                for rect in trap.rect_group:
                    if self.rect.colliderect(rect):
                        return PLAYERDEATH
        return None

    def update(self, tiles, dead_zone, status, enemy_sprite_group, trap_group):
        death = False
        self.movementX()
        collided_tiles = pygame.sprite.spritecollide(self, tiles, False)
        if len(collided_tiles) != 0:
            self.collisionX(collided_tiles)
        
        self.movementY()
        collided_tiles = pygame.sprite.spritecollide(self, tiles, False)
        if len(collided_tiles) != 0:
            self.collisionY(collided_tiles)

        self.shoot_timer()
        self.bullet_group.update(tiles)

        trap_group.player_interaction(self.rect)

        self.check_dead_zone(dead_zone)
        death = self.checkdeath()

        self.bullet_enemy_interaction(enemy_sprite_group)
        temp = self.enemy_interaction(enemy_sprite_group, trap_group)
        if temp != None:
            death = temp

        return death
        

    def check_dead_zone(self,dead_zone):
        for dead in dead_zone:
            if self.rect.x >= dead[0] and self.rect.x <= dead[0] + dead[2] and self.rect.y >= dead[1] and self.rect.y <= dead[1] + dead[3]:
                self.health -= 1000

    def checkdeath(self):
        if self.health <= 0:
            self.respawn()
            return PLAYERDEATH

    def respawn(self):
        pass

    def keyResponse(self,event, status):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.jump()
            elif event.key == pygame.K_SPACE:
                self.shoot_bullet()

        key_p = pygame.key.get_pressed()
        if key_p[pygame.K_a]:
            self.set_speed_x(-self.horizonal_max_speed)
            self.face_direction = -1
        elif key_p[pygame.K_d]:
            self.set_speed_x(self.horizonal_max_speed)
            self.face_direction = 1
        else:
            self.set_speed_x(0)
        return status

# 16 x 10 block per map
class Map:
    
    def __init__(self, map_file_name):
        self.groundSpriteGroup = pygame.sprite.Group()
        self.tileGroup = pygame.sprite.Group()
        self.respawn_group = []
        self.dead_zone = []

        with open(map_file_name, 'r') as f:
            reader =  csv.reader(f)
            next(reader)
            self.vertices = apply(next(reader), int) # min x, max x, min y, max y
            self.player_start_pos = apply(next(reader), int)[0:2] #Left x, top y

            for row in reader:
                self.parseMap(row)
        

    def parseMap(self,row):
        relPos = (int(row[1]), int(row[2]))
        dePos = relativeCoor2DeCoor(relPos)
        width = int(row[3])
        height = int(row[4])
        if row[0] == "ground":
            for i in range(width):
                for j in range(height):
                    groundTile = Ground((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.groundSpriteGroup.add(groundTile)
                    self.tileGroup.add(groundTile)
        elif row[0] == "airTile":
            for i in range(width):
                for j in range(height):
                    airTile = AirTile((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.tileGroup.add(airTile)
        elif row[0] == "barrier":
            self.dead_zone.append((*dePos, width*BLOCKSIZE[0], height*BLOCKSIZE[1]))
        elif row[0] == "appear_block":
            for i in range(width):
                for j in range(height):
                    tile = Appear_block((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.tileGroup.add(tile)
        elif row[0] == "check_point":
            tile = Check_point(dePos)
            self.respawn_group.append(tile)

    def draw(self,screen, cam_pos):
        for sprite in self.tileGroup:
            sprite.draw(screen, cam_pos)
        for dz in self.dead_zone:
            pygame.draw.rect(screen,YELLOW, pygame.Rect(dz[0], dz[1], dz[2]-cam_pos.x,dz[3] - cam_pos.y))
        for respawn in self.respawn_group:
            respawn.draw(screen, cam_pos)

    def update(self):
        pass


class MenuButton(Button):

    def __init__(self,):
        super().__init__(40,40,(SIZE[0]- MENU_BUTTON_PADDING - 40, MENU_BUTTON_PADDING),"images/settingButton.png")

    def mouseInteraction(self, position, status):
        if self.rect.collidepoint(position):
            status.extend([SCREENTOGAMEMENU])
        return status

class GameMenuScreen():

    def __init__(self):
        self.background = Background(706, 381, (47, 48), YELLOW)
        self.closeButton = CloseButton(24,24, (741, 36), RETURNTOGAME)
        self.quitButton = QuitButton((331, 306))
        self.controlButton = InstructionButton((331,118))
        self.restartButton = RestartButton((331, 212))
        self.gameMenu_sprite_group = [self.background, self.closeButton, self.quitButton,self.controlButton, self.controlButton, self.restartButton]

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

class Enemy(pygame.sprite.Sprite):

    def __init__(self,position, x_boundary, y_boundary, imgName, size):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imgName), size)
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x_speed = 1.8
        self.hp = 10
        
    def change_hp(self, value):
        self.hp += value

    def update(self):
        self.rect.x += self.x_speed
        if self.x_speed >0 and self.rect.x > self.x_boundary[1]-self.size[0]:
            self.rect.x = self.x_boundary[1]-self.size[0]
            self.x_speed *= -1
        elif self.x_speed < 0 and self.rect.x < self.x_boundary[0]:
            self.rect.x = self.x_boundary[0]
            self.x_speed *= -1
            
        


    def draw(self, screen, cam_position):
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))

class Goomba(Enemy):

    def __init__(self, position, x_boundary, y_boundary):
        super().__init__(position, x_boundary, y_boundary, "images/goomba.png", GOOMBA_SIZE)
        self.hp = 30

class DeathText():

    def __init__(self):
        font = pygame.font.Font("freesansbold.ttf", 100)
        self.txt = font.render("Defeated", True, DARKBLUE)
        fontSize = self.txt.get_size()
        self.txt_pos = (182, 130)

    def draw(self,screen):
        screen.blit(self.txt, self.txt_pos)

class TrapGroup():

    def __init__(self, filename):
        self.all_trap_group = []
        self.parseFile(filename)

    def parseFile(self,filename):
        # Maybe not use standard csv file but determine how to read the content by the first column
        
        with open(filename, 'r') as f:
            reader =  csv.reader(f)
            next(reader)

            for row in reader:
                relPos = (int(row[1]), int(row[2]))
                dePos = relativeCoor2DeCoor(relPos)
                if row[0] == "normal_spike":
                    trap = Spike(dePos, int(row[3]), int(row[4]))
                    self.all_trap_group.append(trap)
                elif row[0] == "up_spike":
                    trap = SpikeUp(dePos, int(row[3]), int(row[4]),apply(row[5:9], int), int(row[11]), int(row[12]))
                    self.all_trap_group.append(trap)
                elif row[0] == "disappear_block":
                    for i in range(int(row[9])):
                        for j in range(int(row[10])):
                            trap = DisappearBlock((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                            self.all_trap_group.append(trap)
                elif row[0] == "grow_spike":
                    trap = GrowSpike(dePos, int(row[3]), int(row[4]),apply(row[5:9], int), int(row[11]), int(row[12]))
                    self.all_trap_group.append(trap)
                elif row[0] == "hori_spike":
                    trap = HorizontalSpike(dePos, int(row[3]), int(row[4]))
                    self.all_trap_group.append(trap)
                elif row[0] == "hori_move_spike":
                    trap = MoveableHoriSpike(dePos, int(row[3]), int(row[4]),apply(row[5:9], int), int(row[11]), int(row[12]))
                    self.all_trap_group.append(trap)


                

    def draw(self,screen, cam_position):
        for trap in self.all_trap_group:
            trap.draw(screen, cam_position)

    def logic(self):
        for trap in self.all_trap_group:
            trap.logic()

    def player_interaction(self, player_rect):
        for trap in self.all_trap_group:
            trap.player_interaction(player_rect = player_rect)

class GameBoard():
    
    def __init__(self):
        self.time = 0
    
    def logic(self):
        self.time += 1

    def draw(self, screen, cam_pos):
        pass
