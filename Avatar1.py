import pygame
import sys
import os

pygame.init()


# scherm
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Knight movement")
clock = pygame.time.Clock()

# frames laden
frames = []
frame_files = sorted([f for f in os.listdir() if f.startswith("frame_")])
if not frame_files:
    print("❌ Geen frames gevonden! Zet ze in dezelfde map als frame_0.png, frame_1.png, ...")
    sys.exit()

for file in frame_files:
    img = pygame.image.load(file).convert()
    img.set_colorkey((0, 0, 0))  # zwart transparant
    img = pygame.transform.scale(img, (128, 180))
    frames.append(img)

current_frame = 0
animation_speed = 0.15  # snelheid van animatie

# positie & snelheid
x, y = 350, 250
speed = 5
facing_right = True

# game loop
running = True
while running:
    dt = clock.tick(60) / 1000  # delta tijd in seconden

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # beweging
    moving = False
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        x -= speed
        facing_right = False
        moving = True

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        x += speed
        facing_right = True
        moving = True

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        y -= speed
        moving = True

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        y += speed
        moving = True

    # animatie updaten
    if moving:
        current_frame += animation_speed
        if current_frame >= len(frames):
            current_frame = 0

    sprite = frames[int(current_frame)]
    if not facing_right:
        sprite = pygame.transform.flip(sprite, True, False)

    # tekenen
    screen.fill((40, 40, 40))
    screen.blit(sprite, (x, y))
    pygame.display.flip()

pygame.quit()
