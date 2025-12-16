import pygame
import sys

pygame.init()

# Scherm
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gun schieten")

clock = pygame.time.Clock()

# Afbeeldingen laden (convert ipv convert_alpha)
gun_img = pygame.image.load("Jules/Gun1.jpeg").convert_alpha()  # convert gebruikt geen transparantie
bullet_img = pygame.image.load("Jules/Bullet1.jpeg").convert_alpha()


# Grootte aanpassen (optioneel)
gun_img = pygame.transform.scale(gun_img, (80, 60))
bullet_img = pygame.transform.scale(bullet_img, (20, 10))

# Gun positie
gun_x = 100
gun_y = HEIGHT // 2 - gun_img.get_height() // 2

# Loop-offset (hoeveel pixels vanaf bovenkant wapen de loop zit)
loop_offset = 25  # pas dit aan zodat de kogel exact uit de loop komt

# Kogels lijst
bullets = []
BULLET_SPEED = 10

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Linker muisklik → kogel schieten
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # linker muisknop
                bullet_x = gun_x + gun_img.get_width() - 17
                bullet_y = gun_y + loop_offset - bullet_img.get_height() // 2 - 9
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_img.get_width(), bullet_img.get_height()))

    # Kogels bewegen
    for bullet in bullets:
        bullet.x += BULLET_SPEED

    # Kogels verwijderen als ze uit scherm zijn
    bullets = [bullet for bullet in bullets if bullet.x < WIDTH]

    # Tekenen
    screen.fill((30, 30, 30))  # achtergrond
    screen.blit(gun_img, (gun_x, gun_y))

    for bullet in bullets:
        screen.blit(bullet_img, bullet.topleft)

    pygame.display.update()
    clock.tick(60)
