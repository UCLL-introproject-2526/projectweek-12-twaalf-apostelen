import pygame
import sys
import random

pygame.init()

# =====================
# SETTINGS
# =====================
WIDTH, HEIGHT = 1100, 500
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Portal Piano Adventure")
clock = pygame.time.Clock()

# =====================
# LOAD ASSETS
# =====================
player_img = pygame.image.load("assets/player.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (128, 128))  # 👈 VEEL GROTER

background = pygame.image.load("assets/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

portal_img = pygame.image.load("assets/portal.png").convert_alpha()
portal_img = pygame.transform.scale(portal_img, (200, 260))  # 👈 VEEL GROTER

# =====================
# PLAYER
# =====================
player_rect = player_img.get_rect(midbottom=(150, HEIGHT - 40))
player_speed = 5

# =====================
# PORTAL
# =====================
portal_rect = portal_img.get_rect(midbottom=(850, HEIGHT - 40))

# =====================
# GAME STATES
# =====================
WORLD = "world"
PIANO = "piano"
state = WORLD

# =====================
# PIANO GAME
# =====================
lanes = ["A", "S", "D", "F"]
lane_x = {"A": 350, "S": 450, "D": 550, "F": 650}
notes = []
font = pygame.font.SysFont(None, 36)

def spawn_note():
    key = random.choice(lanes)
    rect = pygame.Rect(lane_x[key], -40, 40, 40)
    notes.append({"key": key, "rect": rect})

# =====================
# MAIN LOOP
# =====================
spawn_timer = 0
running = True

while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == PIANO and event.type == pygame.KEYDOWN:
            for note in notes[:]:
                if event.key == pygame.key.key_code(note["key"].lower()):
                    if note["rect"].y > HEIGHT - 140:
                        notes.remove(note)

    # =====================
    # WORLD
    # =====================
    if state == WORLD:
        screen.blit(background, (0, 0))
        screen.blit(portal_img, portal_rect)
        screen.blit(player_img, player_rect)

        # Movement
        if keys[pygame.K_a]:
            player_rect.x -= player_speed
        if keys[pygame.K_d]:
            player_rect.x += player_speed

        # Portal interaction
        if player_rect.colliderect(portal_rect):
            text = font.render("Press E to enter portal", True, (255, 255, 255))
            screen.blit(text, (portal_rect.x - 20, portal_rect.y - 40))

            if keys[pygame.K_e]:
                state = PIANO
                notes.clear()
                spawn_timer = 0

    # =====================
    # PIANO GAME
    # =====================
    elif state == PIANO:
        screen.fill((15, 15, 25))

        # Lanes
        for key, x in lane_x.items():
            pygame.draw.rect(screen, (60, 60, 60), (x, 0, 40, HEIGHT))
            label = font.render(key, True, (255, 255, 255))
            screen.blit(label, (x + 10, HEIGHT - 40))

        # Spawn notes
        spawn_timer += 1
        if spawn_timer > 35:
            spawn_note()
            spawn_timer = 0

        # Move notes
        for note in notes[:]:
            note["rect"].y += 6
            pygame.draw.rect(screen, (180, 200, 255), note["rect"])
            if note["rect"].y > HEIGHT:
                notes.remove(note)

        exit_text = font.render("ESC to exit piano", True, (255, 255, 255))
        screen.blit(exit_text, (20, 20))

        if keys[pygame.K_ESCAPE]:
            state = WORLD

    pygame.display.update()

pygame.quit()
sys.exit()
