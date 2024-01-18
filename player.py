import pygame
import time
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load('level_graphics/graphics/test/player.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(-10, -26)

        #graphic setup
        self.import_player_assets()
        self.status = 'down'

        self.direction = pygame.math.Vector2() # have [x: and y: ]
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        self.dodge_cooldown = 2.0  # Set the initial cooldown time (in seconds)
        self.last_dodge_time = 0.0

    def import_player_assets(self):
        character_path = 'level_graphics/graphics/player/'
        self.animations = {
            'up' : [],
            'down' : [],
            'left' : [],
            'right' : [],
            'right_idle' : [],
            'left_idle' : [],
            'up_idle' : [],
            'down_idle' : [],
            'right_attack' : [],
            'left_attack' : [],
            'up_attack' : [],
            'down_attack' : [],
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(character_path + animation)

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0


        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0


        #dodge or sprint
        if keys[pygame.K_LSHIFT]:
            self.speed = 8
        else:
            self.speed = 5

        #attack input
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')

        # magic attack
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('magic attack')

    def get_status(self):

        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and not 'attack' in self.status:
                self.status += '_idle'
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox): # check for collision
                    if self.direction.x > 0: #moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: #moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: #moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0: #if length doesnt equal 0
            self.direction = self.direction.normalize() #equalize it to 1(bcs when x and y != 0 speed will be faster)

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    

    # def try_dodge(self):
    #     # Check if enough time has passed since the last dodge
    #     current_time = time.time()
    #     if current_time - self.last_dodge_time >= self.dodge_cooldown:
    #         self.dodge()
    #         self.last_dodge_time = current_time  # Update the last dodge time

    # def dodge(self):
    #     self.hitbox.x += self.direction.x * self.speed * 10
    #     self.hitbox.y += self.direction.y * self.speed * 10
    #     self.rect.center = self.hitbox.center


    #update the game
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.move(self.speed)