import csv
import os
import sys

import pygame

from camera import *
from constants import *
from helper import *


class Game:
    
    def __init__(self, level = 1, respawn = False, check_point = None, death_count = 0):
        
        # Pygame setups
        self.size = SIZE # (810,540)
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.done = False
        
        # Load Map
        self.map = Map(os.path.join("files","map" +str(level) +".csv"))
        
        # Level of this game
        self.level = level
        
        # Menu Buttons
        self.menu_button = MenuButton()
        
        # Game Menu Screen
        self.menuScreen = GameMenuScreen()
        
        # Status Codes
        self.status = []
        
        # Cursor Buffer (Prevent Multiple detection from one click)
        self.mouseBuffer = MouseBuffer()
        
        # Instruction Screen (from menu screen)
        self.instruction_screen = InstructionScreen(RETURNTOGAME)
        
        # Game Board
        self.game_board = GameBoard(death_count = death_count)
        
        # Set Current Screen Code
        self.currentScreen = GAME
        
        # Let the main know if the game is restarting or quiting
        self.restart = False
        
        # Text Shown when death
        self.death_text = DeathText()
        self.win_text = WinText()
        
        # Time count until automatic restart from checkpoint
        self.death_count = 0
        self.death_count_start = False
        
        # Time count until automatic exit
        self.win_count = 0
        self.win_count_start = False
        
        # Sprite Group that contains everything
        self.gameSpriteGroup = []
        
        # Check if it is restarting from checkpoint
        self.respawn_checkpoint = True
        if respawn:
            self.check_point = check_point
        else:
            self.check_point = self.map.player_start_pos

        # Create Player object
        self.player = Player(HORIZONAL_MAX_SPEED, self.map.vertices, self.check_point)
        
        # Create Camera (containing the position of the camera)
        self.camera = Camera(self.player, self.map.vertices)
        
        # Enemy sprites group
        self.enemy_sprite_group = pygame.sprite.Group()

        self.gameSpriteGroup.extend([self.menu_button])

        # Parse in the enemy from flat file
        self.parseEntities(os.path.join("files","entity"+str(level)+".csv"))
        
        # Create all traps
        self.trap_group = TrapGroup(os.path.join("files","trap"+str(level)+".csv"))
        
        
        self.gameSpriteGroup.extend([self.trap_group, self.game_board])

    def parseEntities(self, filename: str):
        """
        Parse different enemies to add into game sprite group

        Args:
            filename (str): name of the file
        """
        with open(filename, 'r') as f:
            reader =  csv.reader(f)
            next(reader)

            for row in reader:
                self.create_enemies(row)
        self.gameSpriteGroup.extend(self.enemy_sprite_group)


    def create_enemies(self, row: list):
        """
        Create Enemy object from each line and add into enemy sprite group

        Args:
            row (list): row in the csv file
        """
        
        # Change relative position to pygame coordinates
        position = relativeCoor2DeCoor((int(row[1]), int(row[2])))
        
        # Interprete the boundaries
        x_boundary = tuple(apply(row[3].split("|"), xReToDe))
        y_boundary = tuple(apply(row[4].split("|"), yReToDe))
        
        # Create different enemies
        if row[0] == "goomba":
            temp = Goomba(position, x_boundary, y_boundary)
            self.enemy_sprite_group.add(temp)

    def gameResponse(self, event: pygame.event):
        """
        The game response to different events

        Args:
            event (pygame.event): pygame event
        """
        if event.type == pygame.KEYDOWN:
            
            # When it is inside the death screen + enter is pressed, the game restart instantly 
            if event.key in [pygame.K_RETURN, pygame.K_SPACE] and self.death_count_start:
                self.done = True
                self.restart = True
            elif event.key == pygame.K_ESCAPE:
                if self.currentScreen == GAME:
                    self.currentScreen = GAMEMENU
                else:
                    self.currentScreen = GAME

    def keyResponse(self, event: pygame.event):
        """
        Response to different keys being pressed

        Args:
            event (pygame.event): pygame event
        """
        
        # Different response with respect to the screen mode
        if self.currentScreen == GAMEMENU:
            self.status = self.menuScreen.keyResponse(event,self.status)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.status = self.instruction_screen.keyResponse(event, self.status)
        elif self.currentScreen == GAME:
            self.status = self.player.keyResponse(event, self.status)
        self.gameResponse(event)

    def mouseResponse(self, position: tuple):
        """
        Response to mouse cursor clicks

        Args:
            position (tuple): position of the mouse pointer
        """
        self.status = self.menu_button.mouseInteraction(position, self.status)
        
        # Different response according to the screen mode
        if self.currentScreen == GAMEMENU:
            self.status = self.menuScreen.mouseInteraction(position, self.status)
        elif self.currentScreen == INSTRUCTIONSCREEN:
            self.status = self.instruction_screen.mouseInteraction(position, self.status)

    def readStatus(self):
        """
        Read the status code of the game
        """
        for stat in self.status:
            
            # Turn screen mode to game menu
            if stat == SCREENTOGAMEMENU:
                self.currentScreen = GAMEMENU
                
            # Exit the current game
            elif stat == CLOSEGAME:
                self.done = True
            
            # Turn screen mode to game mode
            elif stat == RETURNTOGAME:
                self.currentScreen = GAME
                
            # Turn screen mode to instruction screen
            elif stat == SCREENTOINSTRUCTION:
                self.currentScreen = INSTRUCTIONSCREEN
                
            # Restart the current game
            elif stat == RESTARTGAME:
                self.done = True
                self.restart = True
                self.respawn_checkpoint = False
                
            # Turn the screen mode to death screen
            elif stat == PLAYERDEATH:
                self.currentScreen = DEATHSCREEN
                self.death_count_start = True
                self.game_board.death_count += 1
                
            elif stat == PLAYERWIN:
                self.currentScreen = WINSCREEN
                self.win_count_start = True
        # Reset the screen status for next iteration
        self.status = []

    def logic(self):
        """
        The main logic of the game
        """
        
        # Read status code from last iteration
        self.readStatus()
        
        # Check the cursor buffer
        self.mouseBuffer.logic()
        
        # Player death screen count down
        self.playerdeath()
        self.playerwin()
        
        # Only run if the player is playing the game (All game object logic will not work if the menu is opened)
        if self.currentScreen == GAME:
            
            # Player and bullet interactions with dead zone, tiles and enemies
            temp = self.player.update(self.map.tileGroup, self.map.dead_zone, self.status,self.enemy_sprite_group, self.trap_group)
            
            # Add new status code to status (if there is one)
            if temp != None:
                self.status.append(temp)
                
            # Change the camera position according to the player's position
            self.camera.scroll()
            
            # Check if the player touches a checkpoint block (and set new checkpoint if yes)
            for tile in self.map.checkpoint_group:
                res = tile.player_interaction(player_rect = self.player.rect)
                if res != None:
                    self.check_point = res
            
            if self.player.rect.colliderect(self.map.finish_point.rect):
                self.status.append(PLAYERWIN)
            
            # Player and tiles interaction (Nothing for now)
            for tile in self.map.tileGroup:
                tile.player_interaction(player_rect = self.player.rect)

            # Traps logic
            self.trap_group.logic()

            # Update enemies
            for enemy in self.enemy_sprite_group:
                enemy.update()
                if enemy.hp <= 0:
                    enemy.kill()
                    self.gameSpriteGroup.remove(enemy)
                    
            # Update game board (Nothing for now)
            self.game_board.logic()

    def drawScreen(self):
        """
        Draw Screen
        """
        
        # fill background as sky blue
        self.screen.fill(SKYBLUE)

        # Draw everything
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
        elif self.currentScreen == WINSCREEN:
            self.win_text.draw(self.screen)

        pygame.display.flip()

    def playerdeath(self):
        """
        Count down for the death screen to disappear
        """
        if self.death_count_start:
            self.death_count +=1
        if self.death_count >= 200:
            self.done = True
            self.restart = True
            self.respawn_checkpoint  = True
            
    def playerwin(self):
        """
        Count down for the win screen to disappear and exit the game
        """
        if self.win_count_start:
            self.win_count += 1
        if self.win_count >= 200:
            self.done = True
            self.restart = False
            self.respawn_checkpoint = False

    def play(self) -> tuple[bool, bool, tuple, int] :
        """
        Main Game loop

        Returns:
            Restart (bool): If the game should restart or not 
            Respawn Checkpoint (bool): If the player should respawn in the check point
            Checkpoint (tuple): tuple for the coordinate of the checkpoint
            Death count: the death count of the player if he / she respawn in checkpoint instead of restarting
        """
        self.done = False
        while not self.done:
            
            # Loop throught events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    sys.exit()
                self.keyResponse(event)
                
            # Cursor interactions
            click,_,_ = pygame.mouse.get_pressed()
            if click == True and not self.mouseBuffer.flag:
                self.mouseBuffer.tFlag()
                mouse = pygame.mouse.get_pos()
                self.mouseResponse(mouse)

            # Game logics
            self.logic()

            # Draw Screen
            self.drawScreen()
            
            # 60 ticks per second
            self.clock.tick(60)
        return self.restart, self.respawn_checkpoint, self.check_point, 0 if not self.respawn_checkpoint else self.game_board.death_count


# Player object
class Player(pygame.sprite.Sprite):
    """
    Player object
    """
    
    
    def __init__(self, horizonal_max_speed: int, vertices: list, start_pos: list):
        super().__init__()
        
        # Import image for the player 
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("images", "redRect.png")), PLAYER_SIZE)
        
        # Create rectangle object for the player
        self.rect = self.image.get_rect()
        
        # Intialise it in the setted starting position
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        
        # Set initial speed as 0
        self.xSpeed = 0
        self.ySpeed = 0
        
        # Set the boarder of the player
        self.left_border = vertices[0]
        self.right_border = vertices[1] - PLAYER_SIZE[0] # right most of the map
        
        # Set the maximum horizonal speed the player can travel
        self.horizonal_max_speed = horizonal_max_speed
        
        # Set the player status to be on the ground
        self.on_ground = True
        
        # Set the health of the player
        self.health = 100
        
        # Set the direction the player is facing (for animation and shooting of the bullets)
        self.face_direction = 1
        
        # Bullet group and timer for shooting the next bullet
        self.bullet_group = pygame.sprite.Group()
        self.bullet_timer = 0
        self.bullet_available = True
    
    def draw(self, screen, cam_position):
        """
        Draw the player

        Args:
            screen (_type_): screen to draw on
            cam_position (_type_): the position of the camera
        """
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))
        
        # Draw bullets
        for bullet in self.bullet_group:
            bullet.draw(screen, cam_position)

    def set_speed_x(self, speed: int):
        """
        Set the horizontal speed of the player
        """
        self.xSpeed = speed

    def shoot_bullet(self):
        """
        Shoot bullet
        """
        
        # Check if the player is allow to shoot bullets
        if self.bullet_available:
            bullet = Bullet(self.face_direction, self.rect.center)
            self.bullet_group.add(bullet)
            self.bullet_available = False

    # Timer for time between each bullet 
    def shoot_timer(self):
        if not self.bullet_available:
            self.bullet_timer += 1
        if self.bullet_timer >= BULLET_TIMER:
            self.bullet_available = True
            self.bullet_timer = 0

    # Interactions between bullets and enemies
    def bullet_enemy_interaction(self, enemies: list):
        
        for enemy in enemies:
            hits = pygame.sprite.spritecollide(enemy, self.bullet_group, False)
            enemy.change_hp(-len(hits) * BULLET_DAMAGE)
            for bu in hits:
                bu.kill()

    def jump(self):
        """
        Control the logic of jumping
        """
        
        # If the player is on the ground, the player jump 
        if self.on_ground:
            self.jump_num = 1
            self.on_ground = False
            self.ySpeed = -JUMP_SPEED
            
        # If the player is on air and there is jumps available, the player jump and reduce the number of jumps available
        elif self.jump_num > 0:
            self.jump_num -= 1
            self.on_ground = False
            self.ySpeed = -JUMP_SPEED

    def movementX(self):
        """
        Horizonal movement logic
        """
        self.rect.x += self.xSpeed 

        # boarder collision
        self.rect.x = min(self.rect.x, self.right_border)
        self.rect.x = max(self.rect.x, self.left_border)
    
    def movementY(self):
        """
        Vertical movement logic
        """
        self.rect.y += self.ySpeed
        self.ySpeed += GRAVITY
        
    def collisionX(self, tiles: list):
        """
        Horizonal interaction wiht tiles it collided with

        Args:
            tiles (list): The ground tiles
        """

        # For moving right
        if self.xSpeed > 0:
            # If there is collision, change x coordinate to the lef to the block it collide with
            for tile in tiles:
                self.rect.x = min(tile.rect.x - PLAYER_SIZE[0], self.rect.x)
                
        # For moving left
        elif self.xSpeed < 0:
            
            # IF there are collisions, change x coordinate to the right of the block it collide with
            for tile in tiles:
                self.rect.x = max(tile.rect.right, self.rect.x)

    def collisionY(self, tiles: list):
        """
        Veritical interaction with tiles it collided with

        Args:
            tiles (list): Ground tiles
        """
        
        # Moving down
        if self.ySpeed > 0:
            self.on_ground = True
            
            # Set the y coordinate to the top of the collide blocks
            for tile in tiles:
                self.rect.y = min(tile.rect.top - PLAYER_SIZE[1], self.rect.y)
            self.ySpeed = 5

        # Moving up
        elif self.ySpeed < 0:
            
            # Set the y coordinate to the top of the collide blocks
            for tile in tiles:
                self.rect.y = max(tile.rect.bottom, self.rect.y)
        
        # Taking away any vertical velocity if collision
            self.ySpeed = 0

    def enemy_interaction(self,enemy_sprite_group: list, trap_group: TrapGroup) -> str:
        """
        Interaction between enemy, traps and player

        Args:
            enemy_sprite_group (list): Group of enemy sprite
            trap_group (TrapGroup): Traps

        Returns:
            str: Status Code
        """
        
        # Player dies if it touches with any enemy
        for enemy in enemy_sprite_group:
            if type(enemy) == Goomba:
                if pygame.sprite.collide_rect(self, enemy):
                    return PLAYERDEATH
                
        # Player dies if it touches traps
        for trap in trap_group.all_trap_group:
            if type(trap) in [Spike, SpikeUp,GrowSpike, HorizontalSpike,MoveableHoriSpike]:
                for rect in trap.rect_group:
                    if self.rect.colliderect(rect):
                        return PLAYERDEATH
                    
        # Return None if the player hasn't died
        return None

    # Logic and updates
    def update(self, tiles: list, dead_zone: list, status: str, enemy_sprite_group: pygame.sprite.Group, trap_group: TrapGroup) -> bool:
        """
        Update the Player including the interaction with environment

        Args:
            tiles (list): List of tiles
            dead_zone (list): list of the dead zones
            status (str): status code
            enemy_sprite_group (pygame.sprite.Group): Enemy sprite group
            trap_group (TrapGroup): Traps

        Returns:
            (bool): If the player is dead
        """
        death = False
        
        # Horizonal movements and collisions
        self.movementX()
        collided_tiles = pygame.sprite.spritecollide(self, tiles, False)
        if len(collided_tiles) != 0:
            self.collisionX(collided_tiles)
        
        # Vertical movements and collisions
        self.movementY()
        collided_tiles = pygame.sprite.spritecollide(self, tiles, False)
        if len(collided_tiles) != 0:
            self.collisionY(collided_tiles)

        # Shoot logics
        self.shoot_timer()
        self.bullet_group.update(tiles)

        # Traps activaltion
        trap_group.player_interaction(self.rect)

        # Check if the player touches dead zone
        self.check_dead_zone(dead_zone)
        
        # Check the player HP
        death = self.checkdeath()

        # Bullet-enemy interaction
        self.bullet_enemy_interaction(enemy_sprite_group)
        
        # Player-enemy interaction
        temp = self.enemy_interaction(enemy_sprite_group, trap_group)
        if temp != None:
            death = temp

        return death
        
    def check_dead_zone(self,dead_zone: list):
        """
        Check if the player touches the deathzone

        Args:
            dead_zone (list): dead zones
        """
        for dead in dead_zone:
            if self.rect.x >= dead[0] and self.rect.x <= dead[0] + dead[2] and self.rect.y >= dead[1] and self.rect.y <= dead[1] + dead[3]:
                self.health -= 1000

    def checkdeath(self) -> str:
        """
        Check if the player has any health left

        Returns:
            (str): if the player is death, it will return a status code indicating the player is dead
        """
        if self.health <= 0:
            return PLAYERDEATH

    # Key response
    def keyResponse(self,event: pygame.event, status: list) -> list:
        """
        Key response

        Args:
            event (pygame.event): event happening in pygame (key inputs)
            status (list): status code list

        Returns:
            status(list): status codes list
        """
        if event.type == pygame.KEYDOWN:
            
            # If W is pressed, jump
            if event.key == pygame.K_w:
                self.jump()
                
            # If space is pressed, shoot bullet
            elif event.key == pygame.K_SPACE:
                self.shoot_bullet()

        # get the key being pressed
        key_p = pygame.key.get_pressed()
        
        # If the A is pressed down, set speed as left
        if key_p[pygame.K_a]:
            self.set_speed_x(-self.horizonal_max_speed)
            self.face_direction = -1
        
        # If the D is pressed down, set speed as right
        elif key_p[pygame.K_d]:
            self.set_speed_x(self.horizonal_max_speed)
            self.face_direction = 1
            
        # If None of A or D is pressed, set speed to 0
        else:
            self.set_speed_x(0)
            
        return status

# 27 x 18 block per map
class Map:
    
    # Initialise Map object
    def __init__(self, map_file_name: str):
        
        # Ground Tiles
        self.groundSpriteGroup = pygame.sprite.Group()
        
        # All tiles
        self.tileGroup = pygame.sprite.Group()
        
        # Checkpoint blocks
        self.checkpoint_group = []
        
        # Deadzones
        self.dead_zone = []
        
        self.finish_point = NULL

        # Parse the csv map file
        with open(map_file_name, 'r') as f:
            reader =  csv.reader(f)
            
            # Skip the header
            next(reader)
            
            # Set the first row as vertices of the map
            self.vertices = apply(next(reader), int) # min x, max x, min y, max y
            
            # Get the starting position of the player
            self.player_start_pos = apply(next(reader), int)[0:2] #Left x, top y

            # Loop through the remaining row
            for row in reader:
                self.parseMap(row)
        
    def parseMap(self,row: list):
        """Create objects according to the information of that row

        Args:
            row (list): a row in the csv file
        """
        
        # Get the relative position
        relPos = (int(row[1]), int(row[2]))
        
        # Turn relative position into coordinate in the Pygame
        dePos = relativeCoor2DeCoor(relPos)
        
        # Number of block extending horizontally and vertically
        width = int(row[3])
        height = int(row[4])
        
        # Ground block
        if row[0] == "ground":
            for i in range(width):
                for j in range(height):
                    groundTile = Ground((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.groundSpriteGroup.add(groundTile)
                    self.tileGroup.add(groundTile)
                    
        # Air Block
        elif row[0] == "airTile":
            for i in range(width):
                for j in range(height):
                    airTile = AirTile((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.tileGroup.add(airTile)
        
        # Deadzone ("barrier")
        elif row[0] == "barrier":
            self.dead_zone.append((*dePos, width*BLOCKSIZE[0], height*BLOCKSIZE[1]))
            
        # Hidden block (only appear if the player is close)
        elif row[0] == "appear_block":
            for i in range(width):
                for j in range(height):
                    tile = Appear_block((dePos[0]+ BLOCKSIZE[0] * i, dePos[1]+ BLOCKSIZE[1] * j))
                    self.tileGroup.add(tile)
        
        # Checkpoints
        elif row[0] == "check_point":
            tile = Check_point(dePos)
            self.checkpoint_group.append(tile)
            
        elif row[0] == "finish_point":
            self.finish_point = FinishPoint(dePos)

    # Draw objects on screen
    def draw(self,screen: pygame.Surface, cam_pos: pygame.math.Vector2):
        """Draw objects

        Args:
            screen (pygame.Surface): pygame display surface
            cam_pos (pygame.math.Vector2): position of the camera
        """
        
        # Draw all tiles
        for sprite in self.tileGroup:
            sprite.draw(screen, cam_pos)
            
        # Draw deadzone (can be removed later)
        for dz in self.dead_zone:
            pygame.draw.rect(screen,YELLOW, pygame.Rect(dz[0], dz[1], dz[2]-cam_pos.x,dz[3] - cam_pos.y))
        
        # Draw checkpoints
        for respawn in self.checkpoint_group:
            respawn.draw(screen, cam_pos)

        self.finish_point.draw(screen, cam_pos)

class MenuButton(Button):
    """
    Menu Button
    """

    # Initialise the button
    def __init__(self):
        super().__init__(40,40,(SIZE[0]- MENU_BUTTON_PADDING - 40, MENU_BUTTON_PADDING),"images/settingButton.png")

    def mouseInteraction(self, position: tuple, status: list) -> list:
        """Interaction with mouse pointer

        Args:
            position (tuple): Position of the pointer
            status (list): status codes

        Returns:
            status: status codes
        """
        if self.rect.collidepoint(position):
            status.extend([SCREENTOGAMEMENU])
        return status

class GameMenuScreen():
    """
    Game Menu Screen
    """

    def __init__(self):
        self.background = Background(706, 381, (47, 48), YELLOW)
        self.closeButton = CloseButton(24,24, (741, 36), RETURNTOGAME)
        self.quitButton = QuitButton((331, 306))
        self.controlButton = InstructionButton((331,118))
        self.restartButton = RestartButton((331, 212))
        self.gameMenu_sprite_group = [self.background, self.closeButton, self.quitButton,self.controlButton, self.controlButton, self.restartButton]

    def drawScreen(self, screen: pygame.Surface):
        """
        Draw Screen

        Args:
            screen (pygame.Surface): pygame display surface
        """
        for sprite in self.gameMenu_sprite_group:
            sprite.draw(screen)

    def mouseInteraction(self,position: tuple, status: list) -> list:
        """
        Interaction with mouse pointer

        Args:
            position (tuple): position of the pointer
            status (list): status code

        Returns:
            list: status code
        """
        for sprite in self.gameMenu_sprite_group:
            status = sprite.mouseInteraction(position, status)
        return status

    def keyResponse(self,event: pygame.event, status: list) -> list:
        """
        Response to keys

        Args:
            event (pygame.event): pygame event
            status (list): status codes

        Returns:
            list: status codes
        """
        for sprite in self.gameMenu_sprite_group:
            status = sprite.keyResponse(event, status)
        return status

class Enemy(pygame.sprite.Sprite):

    def __init__(self, position: list, x_boundary: int, y_boundary: int, imgName: str, size: tuple, hp: int):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(imgName), size)
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x_speed = 1
        self.hp = hp
        self.max_hp = self.hp
        self.h_bar_height = round(self.rect.height*0.1)
        
    def change_hp(self, value: int):
        """
        Change the HP of the enemy

        Args:
            value (int): the amount of change in HP
        """
        self.hp += value

    def update(self):
        """
        Update the position and speed of the enemy
        """
        self.rect.x += self.x_speed
        if self.x_speed >0 and self.rect.x > self.x_boundary[1]-self.size[0]:
            self.x_speed *= -1
        elif self.x_speed < 0 and self.rect.x < self.x_boundary[0]:
            self.x_speed *= -1
            
        


    def draw(self, screen: pygame.Surface, cam_position: pygame.math.Vector2):
        """
        Draw the enemy on the screen

        Args:
            screen (pygame.Surface): pygame display surface
            cam_position (pygame.math.Vector2): the position of the camera
        """
        screen.blit(self.image, (self.rect.x - cam_position.x, self.rect.y))
        pygame.draw.rect(screen, RED, (self.rect.left - cam_position.x, round(self.rect.bottom - self.rect.height*0.1), self.rect.width, self.h_bar_height))
        pygame.draw.rect(screen, LIGHTGREEN, (self.rect.left - cam_position.x, round(self.rect.bottom - self.rect.height*0.1), (self.rect.width * self.hp/self.max_hp), self.h_bar_height))

class Goomba(Enemy):

    def __init__(self, position, x_boundary, y_boundary):
        super().__init__(position, x_boundary, y_boundary, os.path.join("images","goomba.png"), GOOMBA_SIZE, 30)

class DeathText():

    def __init__(self):
        big_font = pygame.font.Font("freesansbold.ttf",100)
        self.txt = big_font.render("Defeated", True, DARKBLUE)
        fontSize = self.txt.get_size()
        self.txt_pos = (182, 130)

    def draw(self,screen: pygame.Surface):
        screen.blit(self.txt, self.txt_pos)


class GameBoard():
    
    def __init__(self, death_count=0):
        self.time = 0
        self.death_count = 0
        self.death_image = pygame.transform.scale(pygame.image.load(os.path.join("images", "death.png")), (40,40))
        self.death_image_coor = (498,20)
        self.death_count = death_count
        self.small_font = pygame.font.Font("freesansbold.ttf", 30)
    
    def logic(self):
        self.time += 1

    def draw(self, screen: pygame.Surface, cam_pos: pygame.math.Vector2):
        screen.blit(self.death_image, self.death_image_coor)
        txt = self.small_font.render(str(self.death_count), True, BLACK)
        screen.blit(txt, (558, 30))

class WinText():
    
    def __init__(self):
        big_font = pygame.font.Font("freesansbold.ttf",100)
        self.txt = big_font.render("Victory", True, DARKBLUE)
        self.txt_pos = (182, 130)
        
    def draw(self,screen: pygame.Surface):
        screen.blit(self.txt, self.txt_pos)