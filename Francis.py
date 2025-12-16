import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Tiles")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Tile settings
TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 150
tile_speed = 5
tiles = []

# Score
score = 0
font = pygame.font.SysFont(None, 40)

# Function to add a new tile
def add_tile():
    x = random.choice([0, TILE_WIDTH, 2*TILE_WIDTH, 3*TILE_WIDTH])
    y = -TILE_HEIGHT
    tiles.append(pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))

# Add first tile
add_tile()

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for tile in tiles:
                if tile.collidepoint(pos):
                    tiles.remove(tile)
                    score += 1
                    break

    # Move tiles
    for tile in tiles:
        tile.y += tile_speed
        if tile.y > HEIGHT:
            print(f"Game Over! Score: {score}")
            pygame.quit()
            sys.exit()
    
    # Add new tiles
    if len(tiles) < 4:
        add_tile()

    # Draw tiles
    for tile in tiles:
        pygame.draw.rect(screen, BLACK, tile)
        pygame.draw.rect(screen, GRAY, tile, 2)  # tile border

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLUE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
