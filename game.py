import pygame

# --------
# init
# -------


pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 680
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Map Example")

clock = pygame.time.Clock()
# --------------------
# CONSTANTS
# --------------------

TILE_SIZE = 40
PLAYER_SPEED = 4

# --------------------
# LEVEL DATA
# --------------------

level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W.........P..............W",
    "W........................W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW"
]

# --------------------
# BUILD LEVEL
# --------------------

def build_level(level_data):
    walls = []
    player_rect = None

    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE

            if tile == "W":
                wall = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
                walls.append(wall)

            if tile == "P":
                player_rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)

    return walls, player_rect

walls, player = build_level(level)


running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL]:
        clock.tick(90)
    else:
        clock.tick(60)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
    
    dx = 0
    dy = 0

    if keys[pygame.K_LEFT]:
        dx = -PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx = PLAYER_SPEED
    if keys[pygame.K_UP]:
        dy = -PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy = PLAYER_SPEED


    player.x += dx
    for wall in walls:
        if player.colliderect(wall):
            if dx > 0:
                player.right = wall.left
            if dx < 0:
                player.left = wall.right

    player.y += dy
    for wall in walls:
        if player.colliderect(wall):
            if dy > 0:
                player.bottom = wall.top
            if dy < 0:
                player.top = wall.bottom

    screen.fill((30, 30, 30))

    for wall in walls:
        pygame.draw.rect(screen, (100, 100, 100), wall)

    pygame.draw.rect(screen, (50, 200, 50), player)

    pygame.display.flip()

pygame.quit()

