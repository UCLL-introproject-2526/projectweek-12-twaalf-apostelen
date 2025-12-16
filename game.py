import pygame

def main(): 
    screen = pygame.display.set_mode((1024 , 768))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            

        screen.fill((0,0,255))
        player_pos = 0
        pygame.draw.rect(screen, 'red', player_pos ,(30, 0, 300, 500))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            player_pos.y -= 300 

        pygame.draw.rect(screen, 'red', player_pos ,(30, 0, 300, 500))













        
        pygame.display.flip()
    
        













main()