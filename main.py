import pygame, sys
from settings import *
from debug import debug

class Game:
    def __init__(self):

        #setup для игры
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Dungeon Crawler')
        self.cloack = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black')
            pygame.display.update()
            self.cloack.tick(FPS)

#запуск мейн файла
if __name__ == '__main__':
    game = Game()
    game.run()