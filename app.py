import pygame



# Create window with given 
def create_main_surface():
    while True :
        screen_size = (1024, 768)

        pygame.display.set_mode(screen_size)

pygame.init()

screen = create_main_surface()
