import pygame
import sys

pygame.init()

# ------------------ SETTINGS ------------------
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.8
JUMP_POWER = -15
PLAYER_SPEED = 5

# ------------------ SETUP ------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Platformer")
clock = pygame.time.Clock()

# ------------------ COLORS ------------------
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
BROWN = (139, 69, 19)

# ------------------ PLAYER ------------------
player = pygame.Rect(100, 400, 40, 50)
player_vel_y = 0
on_ground = False

# ------------------ PLATFORMS ------------------
platforms = [
    pygame.Rect(0, 550, 800, 50),
    pygame.Rect(200, 450, 150, 20),
    pygame.Rect(450, 350, 150, 20),
    pygame.Rect(600, 250, 150, 20)
]

# ------------------ ENEMIES ------------------
enemies = [
    pygame.Rect(300, 510, 40, 40),
    pygame.Rect(550, 510, 40, 40)
]
enemy_speed = 2
enemy_directions = [1, -1]

# ------------------ GAME LOOP ------------------
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ------------------ INPUT ------------------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED
    if keys[pygame.K_SPACE] and on_ground:
        player_vel_y = JUMP_POWER
        on_ground = False

    # ------------------ GRAVITY ------------------
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # ------------------ PLATFORM COLLISION ------------------
    on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and player_vel_y > 0:
            player.bottom = platform.top
            player_vel_y = 0
            on_ground = True

    # ------------------ ENEMY MOVEMENT ------------------
    for i, enemy in enumerate(enemies):
        enemy.x += enemy_speed * enemy_directions[i]
        if enemy.left <= 0 or enemy.right >= WIDTH:
            enemy_directions[i] *= -1

        # Player-enemy collision
        if player.colliderect(enemy):
            if player_vel_y > 0:
                enemies.pop(i)
                enemy_directions.pop(i)
                player_vel_y = JUMP_POWER / 2
                break
            else:
                # Player dies -> reset
                player.x, player.y = 100, 400
                player_vel_y = 0

    # ------------------ DRAW ------------------
    screen.fill(BLUE)

    for platform in platforms:
        pygame.draw.rect(screen, BROWN, platform)

    pygame.draw.rect(screen, RED, player)

    for enemy in enemies:
        pygame.draw.rect(screen, GREEN, enemy)

    pygame.display.update()