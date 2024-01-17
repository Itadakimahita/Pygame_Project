import pygame
import time
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load('assets/player.png').convert_alpha(), (86, 86))
        self.rect = self.image.get_rect(topleft = pos)

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
            self.try_dodge()

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect): # check for collision
                    if self.direction.x > 0: #moving right
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: #moving down
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: #moving up
                        self.rect.top = sprite.rect.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0: #if length doesnt equal 0
            self.direction = self.direction.normalize() #equalize it to 1(bcs when x and y != 0 speed will be faster)

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')


    def try_dodge(self):
        # Check if enough time has passed since the last dodge
        current_time = time.time()
        if current_time - self.last_dodge_time >= self.dodge_cooldown:
            self.dodge()
            self.last_dodge_time = current_time  # Update the last dodge time

    def dodge(self):
        self.rect.x += self.direction.x * self.speed * 3
        self.rect.y += self.direction.y * self.speed * 3


    #update the game
    def update(self):
        self.input()
        self.move(self.speed)