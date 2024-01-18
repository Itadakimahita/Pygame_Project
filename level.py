import pygame
from settings import * 
from tile import Tile
from player import Player



class Level: 
    def __init__(self):


        #get the screen
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YSortCameraGroup() #not touchebles objects
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
                    self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        #will update actionsse
        self.visible_sprites.custom_draw(self.player) #show all tiles
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group): # Y-camera
    def __init__(self):
        #geenral setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #creating the floor
        self.floor_surf = pygame.image.load('../').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player): #drawning method that will replace draw method

        #gettign offset for player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): # draw all of out elements
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        