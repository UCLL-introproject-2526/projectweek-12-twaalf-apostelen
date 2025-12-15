import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Game - Basis")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (200, 0, 0)

COLS = 4
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = 120
SPEED = 5

tiles = []
score = 0
font = pygame.font.SysFont(None, 36)

class Tile:
    def __init__(self, col):
        self.col = col
        self.x = col * TILE_WIDTH
        self.y = -TILE_HEIGHT
        self.rect = pygame.Rect(self.x, self.y, TILE_WIDTH, TILE_HEIGHT)
        self.active = True

    def move(self):
        self.y += SPEED
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)

def spawn_tile():
    col = random.randint(0, COLS - 1)
    tiles.append(Tile(col))

running = True
spawn_timer = 0

while running:
    clock.tick(FPS)
    spawn_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys = {
                pygame.K_a: 0,
                pygame.K_s: 1,
                pygame.K_d: 2,
                pygame.K_f: 3
            }

            if event.key in keys:
                col = keys[event.key]
                for tile in tiles:
                    if tile.col == col and tile.y > HEIGHT - TILE_HEIGHT - 20:
                        tiles.remove(tile)
                        score += 1
                        break

    if spawn_timer > 60:
        spawn_tile()
        spawn_timer = 0

    for tile in tiles[:]:
        tile.move()
        if tile.y > HEIGHT:
            running = False

    screen.fill(WHITE)

    for i in range(1, COLS):
        pygame.draw.line(screen, GRAY, (i * TILE_WIDTH, 0), (i * TILE_WIDTH, HEIGHT))

    for tile in tiles:
        tile.draw()

    score_text = font.render(f"Score: {score}", True, RED)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
