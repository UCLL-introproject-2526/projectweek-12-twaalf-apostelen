import pygame
import os
from settings import *

def load_frames(path, scale=1):
    frames = []
    for file in sorted(os.listdir(path)):
        img = pygame.image.load(os.path.join(path, file)).convert_alpha()
        if scale != 1:
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w*scale), int(h*scale)))
        frames.append(img)
    return frames


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target, groups):
        super().__init__(groups.all_sprites, groups.bullets)

        self.image = pygame.image.load(
            os.path.join(BASE_DIR, "images", "gun", "bullet.png")
        ).convert_alpha()

        self.rect = self.image.get_rect(center=pos)
        self.direction = (pygame.Vector2(target) - pygame.Vector2(pos)).normalize()

    def update(self, dt):
        self.rect.center += self.direction * BULLET_SPEED * dt
        if not pygame.Rect(0,0,WIDTH,HEIGHT).collidepoint(self.rect.center):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, enemy_type):
        super().__init__(groups.all_sprites, groups.enemies)

        base = os.path.join(BASE_DIR, "images", "enemies", enemy_type)
        self.frames = load_frames(base, 1)
        self.frame_index = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

        self.player = player

    def animate(self, dt):
        self.frame_index += ENEMY_ANIMATION_SPEED * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.normalize_ip()
        self.rect.center += direction * ENEMY_SPEED * dt

        self.animate(dt)

        if pygame.sprite.spritecollide(self, self.player.groups.bullets, True):
            self.kill()

        if self.rect.colliderect(self.player.rect):
            self.player.health -= ENEMY_DAMAGE * dt

