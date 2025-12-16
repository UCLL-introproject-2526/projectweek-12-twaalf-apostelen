
import pygame


def main(): 
    screen = pygame.display.set_mode((1024 , 768))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        screen.fill((0,0,0))
        pygame.draw.circle(screen,(255,0,0),(500,500) ,20)
        pygame.display.flip()
        



main()
# import pygame


# def main(): 
#     screen_size = (1024, 768)
#     screen = pygame.display.set_mode(screen_size)

    
#     while True:
#         screen.fill((0,0,0))
#         pygame.draw.circle(screen,(255,0,0),(500,500) ,20)
#         pygame.display.flip()

        


# def create_main_surface():
#     screen_size = (1024, 768)
#     screen = pygame.display.set_mode(screen_size)
#     screen.fill((0,0,0))
#     while True:
#         pygame.draw.circle(screen,(255,0,0),(500,500) ,20)
#         pygame.display.flip()
    

# pygame.init()


   
# main()
