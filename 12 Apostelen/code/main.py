import pygame
import os
import random
from settings import *
from groups import GameGroups
from player import Player
from sprites import Enemy

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont(None, 90)
        self.font_mid = pygame.font.SysFont(None, 60)
        self.font_small = pygame.font.SysFont(None, 40)

        # sounds
        self.shoot_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "shoot.wav"))
        self.impact_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "impact.ogg"))

        # background fullscreen
        bg = pygame.image.load(os.path.join(BASE_DIR, "images", "background.png")).convert()
        self.background = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        self.state = "menu"          # menu -> countdown -> game -> gameover
        self.countdown = 3
        self.countdown_timer = 0

        self.reset_game()

    def reset_game(self):
        self.groups = GameGroups()
        self.player = Player((WIDTH//2, HEIGHT//2), self.groups, self.shoot_sound)

        self.spawn_timer = 0
        self.enemy_types = ["skeleton", "bat", "blob"]

    def spawn_enemy(self):
        enemy_type = random.choice(self.enemy_types)

        # spawn aan randen
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = -40, random.randint(0, HEIGHT)
        elif side == "right":
            x, y = WIDTH + 40, random.randint(0, HEIGHT)
        elif side == "top":
            x, y = random.randint(0, WIDTH), -40
        else:
            x, y = random.randint(0, WIDTH), HEIGHT + 40

        Enemy((x, y), self.player, self.groups, enemy_type, self.impact_sound)

    def draw_center_text(self, text, font, y):
        surf = font.render(text, True, "white")
        rect = surf.get_rect(center=(WIDTH//2, y))
        self.screen.blit(surf, rect)

    def draw_bars(self):
        # health bar
        x, y = 20, 20
        w, h = 300, 20
        ratio = max(0, self.player.health) / PLAYER_HEALTH

        pygame.draw.rect(self.screen, (60,60,60), (x, y, w, h))
        pygame.draw.rect(self.screen, (200,50,50), (x, y, w * ratio, h))
        pygame.draw.rect(self.screen, (255,255,255), (x, y, w, h), 2)

        # stamina bar (onder health)
        y2 = y + 28
        h2 = 12
        stamina_ratio = max(0, self.player.stamina) / STAMINA_MAX

        pygame.draw.rect(self.screen, (60,60,60), (x, y2, w, h2))
        pygame.draw.rect(self.screen, (50,200,50), (x, y2, w * stamina_ratio, h2))
        pygame.draw.rect(self.screen, (255,255,255), (x, y2, w, h2), 2)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.state == "menu":
                        self.state = "countdown"
                        self.countdown = 3
                        self.countdown_timer = 0

                    elif self.state == "gameover":
                        self.reset_game()
                        self.state = "menu"

            self.screen.blit(self.background, (0, 0))

            # MENU
            if self.state == "menu":
                self.draw_center_text("12 Apostelen", self.font_big, 250)
                self.draw_center_text("Press ENTER to start", self.font_small, 340)

            # COUNTDOWN
            elif self.state == "countdown":
                self.countdown_timer += dt
                if self.countdown_timer >= 1:
                    self.countdown -= 1
                    self.countdown_timer = 0

                if self.countdown <= 0:
                    self.state = "game"
                else:
                    self.draw_center_text(str(self.countdown), self.font_big, HEIGHT//2)

            # GAME
            elif self.state == "game":
                self.spawn_timer += dt
                if self.spawn_timer >= SPAWN_INTERVAL:
                    self.spawn_enemy()
                    self.spawn_timer = 0

                self.groups.all_sprites.update(dt)

                # draw
                self.groups.all_sprites.draw(self.screen)
                self.player.draw_gun(self.screen)
                self.draw_bars()

                if self.player.health <= 0:
                    self.state = "gameover"

            # GAME OVER
            elif self.state == "gameover":
                self.draw_center_text("GAME OVER", self.font_big, 280)
                self.draw_center_text("Press ENTER to try again", self.font_small, 360)

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    Game().run()
