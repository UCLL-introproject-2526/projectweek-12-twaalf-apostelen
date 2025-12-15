import pygame
import sys

pygame.init()
pygame.mixer.init

pygame.mixer.music.load("01. Ground Theme.mp3")
pygame.mixer.music.play(-1)

# Screen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)

# Player
player_width, player_height = 40, 50
player = pygame.Rect(100, HEIGHT - player_height - 50, player_width, player_height)
player_velocity_y = 0
gravity = 1
jump_strength = -15
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 50, WIDTH, 50),         # Ground
    pygame.Rect(200, 300, 100, 20),                 # Floating platform
    pygame.Rect(400, 250, 150, 20),                 # Floating platform
]



# Game loop
while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_strength
        on_ground = False

    # Gravity
    player_velocity_y += gravity
    player.y += player_velocity_y

    # Collision with platforms
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and player_velocity_y >= 0:
            player.bottom = platform.top
            player_velocity_y = 0
            on_ground = True

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)

    # Draw player
    pygame.draw.rect(screen, BLUE, player)

    pygame.display.update()
    clock.tick(FPS)
