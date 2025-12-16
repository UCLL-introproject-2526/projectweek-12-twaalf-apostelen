import pygame


def main(): 
    surface = create_main_surface()
    pygame.draw.circle(surface,(255,0,0),(512,384),50)
    pygame.display.flip()

    while True:
        pass

def create_main_surface():
    screen_size = (1024, 768)
    surface = pygame.display.set_mode(screen_size)
    return surface
pygame.init()

screen = main()
