import asyncio
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

        self.fullscreen = True
        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),
            pygame.SCALED | pygame.FULLSCREEN
        )
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # fonts
        self.font_big = pygame.font.SysFont(None, 90)
        self.font_mid = pygame.font.SysFont(None, 60)
        self.font_small = pygame.font.SysFont(None, 36)

        # sounds
        self.shoot_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "assets", "audio", "shoot.wav"))
        self.shoot_sound.set_volume(SHOOT_SOUND)

        self.wave_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "assets", "audio", "Wave.mp3"))
        self.wave_sound.set_volume(WAVE_SOUND)

        self.impact_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "assets", "audio", "Hit.mp3"))
        self.impact_sound.set_volume(IMPACT_SOUND)

        self.die_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, "assets", "audio", "Die.mp3"))
        self.die_sound.set_volume(DIE_SOUND)

        # intro music (1x)
        # intro music (1x)
        pygame.mixer.music.load(
            os.path.join(BASE_DIR, "assets", "audio", "intro.mp3"))
        pygame.mixer.music.set_volume(INTRO_MUSIC_VOLUME)
        pygame.mixer.music.play(0)
        pygame.mixer.music.play(0)

        # images
        # images
        bg = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "images", "background.png")).convert()
        self.background = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        intro = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "images", "intro.png")).convert()
        self.intro_image = pygame.transform.scale(intro, (WIDTH, HEIGHT))

        controls = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "images", "controls.png")).convert()
        self.controls_image = pygame.transform.scale(controls, (WIDTH, HEIGHT))

        # weapon unlock (wave 10)
        self.weapon_unlocked = False
        self.weapon_unlock_timer = 0

        self.new_weapon_image = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "images", "New.png")).convert_alpha()


        # state
        # state
        self.state = "intro"
        self.controls_timer = 0

        # intro fade
        self.intro_alpha = 255
        self.intro_fade_speed = 120
        self.intro_mode = "in"
        self.intro_fade_speed = 120
        self.intro_mode = "in"

        # background fade
        # background fade
        self.fade_alpha = 255
        self.fade_speed = 200
        self.fading = True

        # Save state voor pauze
        self.prev_state = None

        self.weapon_unlock_started = False
        self.weapon_unlocked = False
        self.weapon_unlock_timer = 0


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
        self.wave_pause = False
        self.wave_timer = 0


        self.played_die_sound = False

        self.weapon_unlocked = False
        self.weapon_unlock_timer = 0

        self.countdown = 3
        self.countdown_timer = 0

        self.enemy_types = ["skeleton", "bat", "blob"]

        self.fade_alpha = 255
        self.fading = True

        self.weapon_unlock_started = False
        self.weapon_unlocked = False
        self.weapon_unlock_timer = 0


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
        x, y = 20, 20
        w, h = 300, 20
        hp_ratio = max(0, self.player.health) / PLAYER_HEALTH

        pygame.draw.rect(self.screen, (60, 60, 60), (x, y, w, h))
        pygame.draw.rect(self.screen, (200, 50, 50), (x, y, w * hp_ratio, h))
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, w, h), 2)

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

    def draw_pause_menu(self):
        font = pygame.font.SysFont(None, 60)
        text = font.render("PAUSED - Press ENTER to Resume", True, (255, 255, 255))
        self.screen.blit(text, (100, 250))

    # --------------------------------------------------

    async def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:      
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_RETURN:
                            # ---- PAUSE TOGGLE ----
                        if self.state == "intro":
                            pygame.mixer.music.stop()
                            self.intro_mode = "out"

                        if self.state == "game":
                            self.prev_state = self.state
                            self.state = "pause"

                        elif self.state == "pause":
                            self.state = self.prev_state
                            
                            # ---- NORMAL ENTER ACTIONS ----
                        if self.state == "intro":
                            pygame.mixer.music.stop()
                            pygame.mixer.music.stop()
                            self.intro_mode = "out"

                        elif self.state == "gameover":
                            self.reset_game()
                            self.state = "countdown"

            # ---------- INTRO ----------
            # ---------- INTRO ----------
            if self.state == "intro":
                self.screen.blit(self.intro_image, (0, 0))

                fade = pygame.Surface((WIDTH, HEIGHT))
                fade.fill((0, 0, 0))
                fade.set_alpha(self.intro_alpha)
                self.screen.blit(fade, (0, 0))

                if self.intro_mode == "in":
                    self.intro_alpha -= self.intro_fade_speed * dt
                    if self.intro_alpha <= 0:
                        if self.intro_alpha <= 0:
                         self.intro_alpha = 0

                else:
                    self.intro_alpha += self.intro_fade_speed * dt
                    if self.intro_alpha >= 255:
                        self.state = "controls"
                        self.controls_timer = 0

            # ---------- CONTROLS ----------
            # ---------- CONTROLS ----------
            elif self.state == "controls":
                self.screen.blit(self.controls_image, (0, 0))
                self.controls_timer += dt

                bar_width = 400
                bar_height = 20
                progress = min(self.controls_timer / CONTROLS_TIME, 1)

                x = (WIDTH - bar_width) // 2
                y = HEIGHT - 80

                pygame.draw.rect(self.screen, (60, 60, 60),
                                 (x, y, bar_width, bar_height))
                pygame.draw.rect(self.screen, (50, 200, 50),
                                 (x, y, bar_width * progress, bar_height))
                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (x, y, bar_width, bar_height), 2)

                if self.controls_timer >= CONTROLS_TIME:
                    self.state = "countdown"

            # ---------- COUNTDOWN ----------
            # ---------- COUNTDOWN ----------
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

            # ---------- GAME ----------
            # ---------- GAME ----------
            elif self.state == "game":
                self.screen.blit(self.background, (0, 0))

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

                # -------- WEAPON UNLOCK AT WAVE 10 --------
                if self.wave == 10 and not self.weapon_unlocked:
                    self.weapon_unlocked = True
                    self.weapon_unlock_timer = 0
                    self.prev_state = "game"
                    self.state = "weapon_unlock"


                # WAVE COMPLETE
                # WAVE COMPLETE
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
                    self.wave_sound.play()
                    self.state = "wave_text"

                if self.player.health <= 0:
                    if not self.played_die_sound:
                        self.die_sound.play()
                        self.played_die_sound = True
                    self.state = "gameover"

            # ---------- WAVE TEXT ----------
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

            # ---------- GAME OVER ----------
            # ------------------ PAUSE ------------------

            elif self.state == "pause":
                self.screen.blit(self.background, (0, 0))

                # dark overlay
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(180)
                self.screen.blit(overlay, (0, 0))

                self.draw_center_text(
                    "PAUSED",
                    self.font_big,
                    HEIGHT // 2 - 40
                )
                self.draw_center_text(
                    "Press ENTER to Resume",
                    self.font_small,
                    HEIGHT // 2 + 40
                )
            # ---------------- GAME OVER ----------------
            # ---------- WAVE TEXT ----------
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

            # ---------- GAME OVER ----------
            elif self.state == "gameover":
                self.screen.blit(self.background, (0, 0))
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(150)
                self.screen.blit(overlay, (0, 0))

                self.draw_center_text("GAME OVER", self.font_big, 260)
                self.draw_center_text(
                    f"Score: {self.score}", self.font_mid, 330)
                self.draw_center_text(
                    "Press ENTER to try again",
                    self.font_small,
                    400
                )

            elif self.state == "weapon_unlock":
                self.screen.blit(self.background, (0, 0))

                # HUD blijft zichtbaar
                self.groups.all_sprites.draw(self.screen)
                self.player.draw_gun(self.screen)
                self.draw_bars()
                self.draw_score()

                # NEW.png tonen
                rect = self.new_weapon_image.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2)
                )
                self.screen.blit(self.new_weapon_image, rect)

                # ⏱️ TIMER LOOPT OP (NIET resetten!)
                self.weapon_unlock_timer += dt

                # ⬇️ DIT MOET BEREIKBAAR ZIJN
                if self.weapon_unlock_timer >= 3:
                    # gun2 laden en schalen
                    gun2 = pygame.image.load(
                        os.path.join(BASE_DIR, "assets", "images", "gun", "gun2.png")
                    ).convert_alpha()

                    gun2 = pygame.transform.scale(
                        gun2,
                        (
                            int(gun2.get_width() * AK_WIDTH),
                            int(gun2.get_height() * AK_HEIGHT)
                        )
                    )

                    # gun effectief veranderen
                    self.player.gun_image = gun2
                    self.player.shoot_cooldown = BULLET_COOLDOWN * 0.5
                    self.player.last_shot = 0

                    # 🔴 DIT IS ESSENTIEEL
                    self.weapon_unlocked = True
                    self.state = "countdown"
            pygame.display.update()
            await asyncio.sleep(0)

        pygame.quit()


async def main():
    game = Game()
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())