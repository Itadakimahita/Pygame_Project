import pygame

class Level: 
    def __init__(self):


        #get the screen
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.visible_sprites = pygame.sprite.Group() #not touchebles objects
        self.obstacle_sprites = pygame.sprite.Group() #touchbles objects

    def run(self):
        #will update actions
        pass