import pygame, random, os
from settings import *
from groups import GameGroups
from player import Player
from sprites import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont(None, 80)
        self.font_small = pygame.font.SysFont(None, 40)

        self.state = "menu"
        self.countdown = 3
        self.countdown_time = 0

        bg = pygame.image.load(os.path.join(BASE_DIR, "images", "background.png")).convert()

        self.background = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        self.reset()

    def reset(self):
        self.groups = GameGroups()
        self.player = Player((WIDTH//2, HEIGHT//2), self.groups)
        self.spawn_timer = 0

    def spawn_enemy(self):
        enemy_type = random.choice(["skeleton","bat","blob"])
        x = random.choice([0, WIDTH])
        y = random.randint(0, HEIGHT)
        Enemy((x,y), self.player, self.groups, enemy_type)

    def draw_text(self, text, size, y):
        font = self.font_big if size == "big" else self.font_small
        surf = font.render(text, True, "white")
        rect = surf.get_rect(center=(WIDTH//2, y))
        self.screen.blit(surf, rect)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)/1000

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    if self.state == "menu":
                        self.state = "countdown"
                        self.countdown = 3
                        self.countdown_time = 0
                    elif self.state == "gameover":
                        self.reset()
                        self.state = "menu"

            self.screen.blit(self.background,(0,0))

            if self.state == "menu":
                self.draw_text("12 Apostelen","big",250)
                self.draw_text("Press ENTER to start","small",350)

            elif self.state == "countdown":
                self.countdown_time += dt
                if self.countdown_time >= 1:
                    self.countdown -= 1
                    self.countdown_time = 0
                if self.countdown <= 0:
                    self.state = "game"
                else:
                    self.draw_text(str(self.countdown),"big",HEIGHT//2)

            elif self.state == "game":
                self.spawn_timer += dt
                if self.spawn_timer > 2:
                    self.spawn_enemy()
                    self.spawn_timer = 0

                self.groups.all_sprites.update(dt)

                self.groups.all_sprites.draw(self.screen)
                self.player.draw_gun(self.screen)

                # health bar
                ratio = self.player.health / PLAYER_HEALTH
                pygame.draw.rect(self.screen,(60,60,60),(20,20,250,18))
                pygame.draw.rect(self.screen,(200,50,50),(20,20,250*ratio,18))

                if self.player.health <= 0:
                    self.state = "gameover"

            elif self.state == "gameover":
                self.draw_text("GAME OVER","big",300)
                self.draw_text("Press ENTER to try again","small",380)

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    Game().run()
