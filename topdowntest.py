import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Legend of Zelda")

clock = pygame.time.Clock()
FPS = 60
PNLink = pygame.image.load("Link.png")
PNLink = pygame.transform.scale(PNLink,(32,32))
Link = pygame.Rect(960,520,32,32)

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
WHITE = (255, 255, 255)

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        Link.x -= 1
    if keys[pygame.K_RIGHT]:
        Link.x += 1
    if keys[pygame.K_DOWN]:
        Link.y += 1
    if keys [pygame.K_UP]:
        Link.y -= 1

    screen.blit(PNLink, (Link.x, Link.y))
    pygame.display.update()
