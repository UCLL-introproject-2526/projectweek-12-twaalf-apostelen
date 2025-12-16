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
        

