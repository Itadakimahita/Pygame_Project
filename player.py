import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load('assets/player.png').convert_alpha(), (86, 86))
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2() # have [x: and y: ]

    def input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = 1
        elif keys[pygame.K_DOWN]:
            self.direction.y = -1
        else:
            self.direction.y = 0


        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    #update the game
    def update(self):
        self.input()