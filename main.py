import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
clock = pygame.time.Clock()

# Player Class
# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed


# Enemy Class
# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def update(self, *args, **kwargs):
        if args and isinstance(args[0], Player):
            player = args[0]
            # Simple AI: Move towards the player
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed
            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > player.rect.y:
                self.rect.y -= self.speed


# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player and enemies
player = Player(WIDTH // 2, HEIGHT // 2)
all_sprites.add(player)

for _ in range(5):
    enemy = Enemy(random.randrange(WIDTH), random.randrange(HEIGHT))
    all_sprites.add(enemy)
    enemies.add(enemy)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        print("Player got hit!")

    # Draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
