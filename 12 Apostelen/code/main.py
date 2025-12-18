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

        # fonts
        self.font_big = pygame.font.SysFont(None, 90)
        self.font_mid = pygame.font.SysFont(None, 60)
        self.font_small = pygame.font.SysFont(None, 36)

        # sounds
        self.shoot_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "audio", "shoot.wav"))
        self.impact_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "audio", "impact.ogg"))

        # background
        bg = pygame.image.load(
            os.path.join(BASE_DIR, "images", "background.png")).convert()
        self.background = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        # intro image
        intro = pygame.image.load(
            os.path.join(BASE_DIR, "images", "intro.png")).convert()
        self.intro_image = pygame.transform.scale(intro, (WIDTH, HEIGHT))

        self.state = "intro"   # intro -> countdown -> game -> wave_text -> gameover
        self.first_launch = True

        self.reset_game()

    # --------------------------------------------------

    def reset_game(self):
        self.groups = GameGroups()
        self.player = Player(
            (WIDTH // 2, HEIGHT // 2),
            self.groups,
            self.shoot_sound
        )

        self.score = 0
        self.wave = 1

        self.spawn_timer = 0
        self.spawned_this_wave = 0

        self.spawn_interval = 1.1
        self.groups.enemy_speed = ENEMY_SPEED

        self.wave_pause = False
        self.wave_timer = 0

        self.countdown = 3
        self.countdown_timer = 0

        self.enemy_types = ["skeleton", "bat", "blob"]

    # --------------------------------------------------

    def spawn_enemy(self):
        enemy_type = random.choice(self.enemy_types)

        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            pos = (-40, random.randint(0, HEIGHT))
        elif side == "right":
            pos = (WIDTH + 40, random.randint(0, HEIGHT))
        elif side == "top":
            pos = (random.randint(0, WIDTH), -40)
        else:
            pos = (random.randint(0, WIDTH), HEIGHT + 40)

        Enemy(
            pos,
            self.player,
            self.groups,
            enemy_type,
            self.impact_sound,
            self
        )

        self.spawned_this_wave += 1

    # --------------------------------------------------

    def draw_center_text(self, text, font, y):
        surf = font.render(text, True, "white")
        rect = surf.get_rect(center=(WIDTH // 2, y))
        self.screen.blit(surf, rect)

    # --------------------------------------------------

    def draw_bars(self):
        # HP
        x, y = 20, 20
        w, h = 300, 20
        hp_ratio = max(0, self.player.health) / PLAYER_HEALTH

        pygame.draw.rect(self.screen, (60, 60, 60), (x, y, w, h))
        pygame.draw.rect(self.screen, (200, 50, 50), (x, y, w * hp_ratio, h))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, w, h), 2)

        # stamina
        y2 = y + 28
        stamina_ratio = self.player.stamina / STAMINA_MAX

        pygame.draw.rect(self.screen, (60, 60, 60), (x, y2, w, 12))
        pygame.draw.rect(self.screen, (50, 200, 50),
                         (x, y2, w * stamina_ratio, 12))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y2, w, 12), 2)

    # --------------------------------------------------

    def draw_score(self):
        text = self.font_small.render(
            f"Score: {self.score}", True, "white")
        rect = text.get_rect(topright=(WIDTH - 20, 20))
        self.screen.blit(text, rect)

    # --------------------------------------------------

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
        

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.state == "intro":
                        self.state = "countdown"
                        self.countdown = 3
                        self.countdown_timer = 0

                    elif self.state == "gameover":
                        self.reset_game()
                        self.state = "countdown"

            # --------------------------------------------------
            # INTRO
            if self.state == "intro":
                self.screen.blit(self.intro_image, (0, 0))

            # --------------------------------------------------
            # COUNTDOWN
            elif self.state == "countdown":
                self.screen.blit(self.background, (0, 0))
                self.countdown_timer += dt

                if self.countdown_timer >= 1:
                    self.countdown -= 1
                    self.countdown_timer = 0

                if self.countdown <= 0:
                    self.state = "game"
                else:
                    self.draw_center_text(
                        str(self.countdown),
                        self.font_big,
                        HEIGHT // 2
                    )

            # --------------------------------------------------
            # WAVE TEXT
            elif self.state == "wave_text":
                self.screen.blit(self.background, (0, 0))
                self.wave_timer += dt

                self.draw_center_text(
                    f"WAVE {self.wave}",
                    self.font_mid,
                    HEIGHT // 2
                )

                if self.wave_timer >= WAVE_TEXT_TIME:
                    self.wave_timer = 0
                    self.state = "countdown"

            # --------------------------------------------------
            # GAME
            elif self.state == "game":
                self.screen.blit(self.background, (0, 0))

                # spawn enemies
                if self.spawned_this_wave < KILLS_PER_WAVE:
                    self.spawn_timer += dt
                    if self.spawn_timer >= self.spawn_interval:
                        self.spawn_enemy()
                        self.spawn_timer = 0

                self.groups.all_sprites.update(dt)

                self.groups.all_sprites.draw(self.screen)
                self.player.draw_gun(self.screen)
                self.draw_bars()
                self.draw_score()

                # wave klaar
                if (
                    self.spawned_this_wave >= KILLS_PER_WAVE
                    and len(self.groups.enemies) == 0
                ):
                    self.wave += 1
                    self.spawned_this_wave = 0

                    self.groups.enemy_speed += WAVE_SPEED_INCREASE
                    self.spawn_interval = max(
                        MIN_SPAWN_INTERVAL,
                        self.spawn_interval - WAVE_SPAWN_DECREASE
                    )

                    self.state = "wave_text"

                if self.player.health <= 0:
                    self.state = "gameover"

            # --------------------------------------------------
            # GAME OVER
            elif self.state == "gameover":
                self.screen.blit(self.background, (0, 0))
                self.draw_center_text("GAME OVER", self.font_big, 260)
                self.draw_center_text(
                    f"Score: {self.score}",
                    self.font_mid,
                    330
                )
                self.draw_center_text(
                    "Press ENTER to try again",
                    self.font_small,
                    400
                )

            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    Game().run()
