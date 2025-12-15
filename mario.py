import pygame
import sys

pygame.init()
pygame.mixer.init()

# Load and play music
pygame.mixer.music.load("01. Ground Theme.mp3")
pygame.mixer.music.play(-1)

# Screen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario")

clock = pygame.time.Clock()
FPS = 60

# Colors
BROWN = (139, 69, 19)

# Load background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Player sprite
Mario_img = pygame.image.load("mario.png")
Mario_img = pygame.transform.scale(Mario_img, (50, 50))
player_x, player_y = 100, HEIGHT - 100
player_velocity_y = 0
gravity = 1
jump_strength = -15
on_ground = False

# Player rect for collisions
player_rect = pygame.Rect(player_x, player_y, 50, 50)

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 50, WIDTH, 50),         # Ground
    pygame.Rect(200, 300, 100, 20),                 # Floating platform
    pygame.Rect(400, 250, 150, 20),                 # Floating platform
]

# Game loop
while True:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5
    if keys[pygame.K_SPACE] and on_ground:
        player_velocity_y = jump_strength
        on_ground = False

    # Gravity
    player_velocity_y += gravity
    player_rect.y += player_velocity_y

    # Collision with platforms
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity_y >= 0:
            player_rect.bottom = platform.top
            player_velocity_y = 0
            on_ground = True

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)

    # Draw player
    screen.blit(Mario_img, (player_rect.x, player_rect.y))

    pygame.display.update()
    clock.tick(FPS)
