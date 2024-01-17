import pygame
from settings import * 
from tile import Tile
from player import Player



class Level: 
    def __init__(self):


        #get the screen
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = pygame.sprite.Group() #not touchebles objects
        self.obstacle_sprites = pygame.sprite.Group() #touchbles objects

        self.create_map()

    #will create map from settings
    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP): #get index with value
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x,y), [self.visible_sprites])

    def run(self):
        #will update actionsse
        self.visible_sprites.draw(self.display_surface) #show all tiles
        self.visible_sprites.update()
        pass