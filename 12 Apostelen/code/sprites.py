import pygame
import os
from settings import *

def load_frames(path, scale=1.0):
    frames = []
    for f in sorted(os.listdir(path)):
        img = pygame.image.load(os.path.join(path, f)).convert_alpha()
        if scale != 1.0:
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

        d = pygame.Vector2(target) - pygame.Vector2(pos)
        self.direction = d.normalize() if d.length() else pygame.Vector2(1,0)

    def update(self, dt):
        self.rect.center += self.direction * BULLET_SPEED * dt
        if not pygame.Rect(0,0,WIDTH,HEIGHT).colliderect(self.rect):
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, enemy_type, impact_sound, game):
        super().__init__(groups.all_sprites, groups.enemies)
        self.player = player
        self.groups = groups
        self.game = game
        self.impact_sound = impact_sound

        self.frames = load_frames(
            os.path.join(BASE_DIR, "images", "enemies", enemy_type)
        )
        self.frame_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length():
            direction.normalize_ip()
        self.rect.center += direction * self.groups.enemy_speed * dt

        self.frame_index += ENEMY_ANIMATION_SPEED * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        if pygame.sprite.spritecollide(self, self.groups.bullets, True):
            self.impact_sound.play()
            self.game.score += 1
            self.kill()

        if self.rect.colliderect(self.player.rect):
            self.player.health -= ENEMY_DAMAGE_PER_SEC * dt
