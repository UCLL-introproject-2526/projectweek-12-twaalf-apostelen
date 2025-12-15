import pygame
import sys

pygame.init()

# Window
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Run & Jump Game")

clock = pygame.time.Clock()

# Player
player = pygame.Rect(100, 300, 40, 40)
player_velocity = 0
gravity = 1
on_ground = True

# Obstacle
obstacle = pygame.Rect(800, 320, 40, 20)
obstacle_speed = 6

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Jump
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_velocity = -15
                on_ground = False

    # Gravity
    player_velocity += gravity
    player.y += player_velocity

    if player.y >= 300:
        player.y = 300
        player_velocity = 0
        on_ground = True

    # Move obstacle
    obstacle.x -= obstacle_speed
    if obstacle.x < -40:
        obstacle.x = WIDTH

    # Collision
    if player.colliderect(obstacle):
        print("Game Over!")
        pygame.quit()
        sys.exit()

    # Draw
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, player)
    pygame.draw.rect(screen, RED, obstacle)

    pygame.display.update()
    clock.tick(60)
