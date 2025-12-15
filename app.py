import pygame


def main(): 
    while True:
        create_main_surface()

def create_main_surface():
    screen_size = (1024, 768)
    pygame.display.set_mode(screen_size)

pygame.init()

screen = main()
