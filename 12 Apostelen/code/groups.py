import pygame

class GameGroups:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # dynamisch aangepast door Game
        self.enemy_speed = 0
