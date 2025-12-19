import pygame
import os
import math
from settings import *
from sprites import Bullet, load_frames

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, shoot_sound):
        super().__init__(groups.all_sprites)
        self.groups = groups
        self.shoot_sound = shoot_sound

        self.animations = {}
        self.import_assets()

        self.status = "down"
        self.frame_index = 0
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(center=pos)

        self.last_shot = 0
        self.shoot_cooldown = BULLET_COOLDOWN

        self.direction = pygame.Vector2()
        self.last_shot = 0
        self.health = PLAYER_HEALTH

        self.stamina = STAMINA_MAX
        self.sprinting = False

        self.gun_image = pygame.image.load(
            os.path.join(BASE_DIR, "assets", "images", "gun", "gun.png")).convert_alpha()

        self.gun_image = pygame.transform.scale(
            self.gun_image,
            (int(self.gun_image.get_width() * 0.45),
             int(self.gun_image.get_height() * 0.45))
        )

    def import_assets(self):
        base = os.path.join(BASE_DIR, "assets" ,"images", "player")
        for d in ["up", "down", "left", "right"]:
            self.animations[d] = load_frames(os.path.join(base, d), PLAYER_SCALE)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"

        self.shift_held = keys[pygame.K_LSHIFT]

        if pygame.mouse.get_pressed()[0]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_cooldown:
            self.last_shot = now
            Bullet(self.rect.center, pygame.mouse.get_pos(), self.groups)
            self.shoot_sound.play()


    def move(self, dt):
        if self.direction.length():
            self.direction.normalize_ip()
        speed = PLAYER_SPEED

        # Decide sprint FIRST
        if self.shift_held and self.stamina > 0.05:
            speed *= SPRINT_MULTIPLIER

        # Drain stamina
            self.stamina -= STAMINA_DRAIN * dt
            if self.stamina < 0:
                self.stamina = 0
        else:
        # Recover stamina
            self.stamina += STAMINA_RECOVER * dt
            if self.stamina > STAMINA_MAX:
                self.stamina = STAMINA_MAX

        self.rect.center += self.direction * speed * dt
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def animate(self, dt):
        if self.direction.length() == 0:
            self.image = self.animations[self.status][0]
            return

        self.frame_index += PLAYER_ANIMATION_SPEED * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def draw_gun(self, surface):
        mouse = pygame.mouse.get_pos()
        angle = math.degrees(math.atan2(
            mouse[1] - self.rect.centery,
            mouse[0] - self.rect.centerx
        ))

        gun = pygame.transform.rotate(self.gun_image, -angle)
        offset = pygame.Vector2(18, 6).rotate(angle)
        pos = pygame.Vector2(self.rect.center) + offset
        surface.blit(gun, gun.get_rect(center=pos))

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
    