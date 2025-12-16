import pygame
import sys
import os

pygame.init()

# scherm
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Knight idle animation")
clock = pygame.time.Clock()

# map van het script
script_dir = os.path.dirname(os.path.abspath(__file__))

# frames laden
frames = []
frame_files = sorted([f for f in os.listdir(script_dir) if f.startswith("frame_")])
if not frame_files:
    print("❌ Geen frames gevonden! Zet ze in dezelfde map als het script (frame_0.png, frame_1.png, ...)")
    sys.exit()

for file in frame_files:
    img = pygame.image.load(os.path.join(script_dir, file)).convert()
    img.set_colorkey((0, 0, 0))  # zwart transparant
    img = pygame.transform.scale(img, (128, 180))
    frames.append(img)

current_frame = 0
animation_speed = 0.15  # snelheid van animatie

# positie (stilstaand)
x, y = 350, 250
facing_right = True  # je kan dit aanpassen als je wilt

# game loop
running = True
while running:
    dt = clock.tick(60) / 1000  # delta tijd in seconden

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # animatie altijd updaten
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
