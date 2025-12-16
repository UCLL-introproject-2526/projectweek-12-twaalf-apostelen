import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Temple Run")

clock = pygame.time.Clock()
FPS = 60

# Player
player_width, player_height = 40, 40
player_x = 100
player_y = HEIGHT - player_height - 50
player_velocity = 0
gravity = 1
jump_strength = -15
on_ground = True

player = pygame.Rect(player_x, player_y, player_width, player_height)

# Obstacles
obstacle_width, obstacle_height = 40, 40
obstacle_list = []
obstacle_speed = 6
spawn_timer = 0

# Score
score = 0
font = pygame.font.SysFont(None, 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Game loop
while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_velocity = jump_strength
                on_ground = False

    # Gravity
    player_velocity += gravity
    player.y += player_velocity

    if player.y >= HEIGHT - player_height - 50:
        player.y = HEIGHT - player_height - 50
        player_velocity = 0
        on_ground = True

    # Spawn obstacles
    spawn_timer += 1
    if spawn_timer > 90:  # every 1.5 seconds at 60 FPS
        lane_y = HEIGHT - obstacle_height - 50
        obstacle_list.append(pygame.Rect(WIDTH, lane_y, obstacle_width, obstacle_height))
        spawn_timer = 0

    # Move obstacles
    for obs in obstacle_list:
        obs.x -= obstacle_speed
        if obs.x < -obstacle_width:
            obstacle_list.remove(obs)
            score += 1

    # Collision
    for obs in obstacle_list:
        if player.colliderect(obs):
            print(f"Game Over! Score: {score}")
            pygame.quit()
            sys.exit()

    # Draw player and obstacles
    pygame.draw.rect(screen, BLACK, player)
    for obs in obstacle_list:
        pygame.draw.rect(screen, RED, obs)

    # Draw score
    score_text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)
