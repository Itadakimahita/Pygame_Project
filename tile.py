import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.transform.scale(pygame.image.load('assets/map/box.png').convert_alpha(), (64, 64))
        
        self.rect = self.image.get_rect(topleft = pos)

        #hitbox
        self.hitbox = self.rect.inflate(0, -10) #takes rectangle and changes a size
