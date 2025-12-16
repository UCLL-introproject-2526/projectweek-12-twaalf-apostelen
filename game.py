# import pygame

# # --------
# # init
# # -------


# pygame.init()
# # --------------------
# # CONSTANTS
# # --------------------
# TILE_SIZE = 40
# PLAYER_SPEED = 4
# # --------------------
# # CONSTANTS
# # --------------------
# SCREEN_WIDTH = 1024
# SCREEN_HEIGHT = 680
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Tile Map Example")

# clock = pygame.time.Clock()

# # --------------------
# # LEVEL DATA
# # --------------------

# level = [
#     "WWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W...........P............W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "W........................W",
#     "WWWWWWWWWWWWWWWWWWWWWWWWWW"
# ]

# # --------------------
# # BUILD LEVEL
# # --------------------

# def build_level(level_data):
#     walls = []
#     player_rect = None

#     for y, row in enumerate(level_data):
#         for x, tile in enumerate(row):
#             world_x = x * TILE_SIZE
#             world_y = y * TILE_SIZE

#             if tile == "W":
#                 wall = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
#                 walls.append(wall)

#             if tile == "P":
#                 player_rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)

#     return walls, player_rect

# walls, player = build_level(level)

# player_img = pygame.image.load("afbeeldingen mannetje/frame_04.png").convert_alpha()
# player_img = pygame.transform.scale(player_img, (200, 200))

# running = True
# while running:
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LCTRL]:
#         clock.tick(80)
#     else:
#         clock.tick(60)


#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

  
    
#     dx = 0
#     dy = 0

#     if keys[pygame.K_LEFT]:
#         dx = -PLAYER_SPEED
#     if keys[pygame.K_RIGHT]:
#         dx = PLAYER_SPEED
#     if keys[pygame.K_UP]:
#         dy = -PLAYER_SPEED
#     if keys[pygame.K_DOWN]:
#         dy = PLAYER_SPEED


  
#     future_rect = player.move(dx, 0)
#     for wall in walls:
#         if future_rect.colliderect(wall):
#             if dx > 0:
#                 dx = wall.left - player.right
#             elif dx < 0:
#                 dx = wall.right - player.left
#     player.x += dx



#     future_rect = player.move(0, dy)
#     for wall in walls:
#         if future_rect.colliderect(wall):
#             if dy > 0:
#                 dy = wall.top - player.bottom
#             elif dy < 0:
#                 dy = wall.bottom - player.top
#     player.y += dy

#     screen.fill((30, 30, 30))

#     for wall in walls:
#         pygame.draw.rect(screen, (100, 100, 100), wall)

#     screen.blit(player_img ,player )

#     pygame.display.flip()

# pygame.quit()

import pygame

# --------------------
# INIT
# --------------------
pygame.init()

# --------------------
# CONSTANTS
# --------------------
TILE_SIZE = 40
PLAYER_SPEED = 4

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 680
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Map Example")

CLOCK = pygame.time.Clock()
BG_COLOR = (30, 30, 30)
WALL_COLOR = (100, 100, 100)

# --------------------
# LEVEL DATA
# --------------------
LEVEL = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W...........P............W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
    "W........................W",
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
                # Collision rect size = TILE_SIZE
                player_rect = pygame.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)

    return walls, player_rect

walls, collision_rect = build_level(LEVEL)

# --------------------
# LOAD PLAYER IMAGE
# --------------------
# Big player sprite (can be bigger than TILE_SIZE)
player_img = pygame.image.load("afbeeldingen mannetje/frame_04.png").convert_alpha()
PLAYER_IMG_WIDTH = 200
PLAYER_IMG_HEIGHT = 200
player_img = pygame.transform.scale(player_img, (PLAYER_IMG_WIDTH, PLAYER_IMG_HEIGHT))

# Offset to draw image correctly relative to collision rect
offset_x = (PLAYER_IMG_WIDTH - TILE_SIZE) // 2
offset_y = PLAYER_IMG_HEIGHT - TILE_SIZE

# --------------------
# MAIN LOOP
# --------------------
running = True
while running:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL]:
        CLOCK.tick(80)
    else:
        CLOCK.tick(60)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # INPUT
    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        dx = PLAYER_SPEED
    if keys[pygame.K_UP]:
        dy = -PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        dy = PLAYER_SPEED

    # --------------------
    # HORIZONTAL COLLISION (predictive)
    # --------------------
    future_rect = collision_rect.move(dx, 0)
    for wall in walls:
        if future_rect.colliderect(wall):
            if dx > 0:
                dx = wall.left - collision_rect.right
            elif dx < 0:
                dx = wall.right - collision_rect.left
    collision_rect.x += dx

    # --------------------
    # VERTICAL COLLISION (predictive)
    # --------------------
    future_rect = collision_rect.move(0, dy)
    for wall in walls:
        if future_rect.colliderect(wall):
            if dy > 0:
                dy = wall.top - collision_rect.bottom
            elif dy < 0:
                dy = wall.bottom - collision_rect.top
    collision_rect.y += dy

    # --------------------
    # DRAW
    # --------------------
    SCREEN.fill(BG_COLOR)

    # draw walls
    for wall in walls:
        pygame.draw.rect(SCREEN, WALL_COLOR, wall)

    # draw player image with offset
    SCREEN.blit(player_img, (collision_rect.x - offset_x, collision_rect.y - offset_y))

    pygame.display.flip()

pygame.quit()