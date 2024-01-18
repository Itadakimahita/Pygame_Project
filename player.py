import pygame
import time
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load('level_graphics/graphics/test/player.png').convert_alpha(), (64, 64))
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.inflate(-10, -26)

        self.direction = pygame.math.Vector2() # have [x: and y: ]
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

        self.dodge_cooldown = 2.0  # Set the initial cooldown time (in seconds)
        self.last_dodge_time = 0.0


    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0


        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pygame.K_LSHIFT]:
            self.speed = 8
        else:
            self.speed = 5

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
        self.move(self.speed)