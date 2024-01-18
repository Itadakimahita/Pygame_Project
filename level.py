import pygame
from settings import * 
from support import *
from tile import Tile
from player import Player
from random import choice
from weapon import Weapon



class Level: 
    def __init__(self):

        #get the screen
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = YSortCameraGroup() #not touchebles objects
        self.obstacle_sprites = pygame.sprite.Group() #touchbles objects

        # attack sprites
        self.current_attack = None

        self.create_map()

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])
        
    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    #will create map from settings
    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('level_graphics/map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('level_graphics/map/map_Grass.csv'),
            'object': import_csv_layout('level_graphics/map/map_Objects.csv'),
        }

        graphics = {
            'grass': import_folder('level_graphics/graphics/Grass'),
            'objects': import_folder('level_graphics/graphics/objects')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout): #get index with value
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)


        #         if col == 'x':
        #             Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
        self.player = Player((2000,1430), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

    

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
        self.floor_surf = pygame.image.load('level_graphics/graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player): #drawning method that will replace draw method

        #gettign offset for player
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #drawning the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery): # draw all of out elements
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        