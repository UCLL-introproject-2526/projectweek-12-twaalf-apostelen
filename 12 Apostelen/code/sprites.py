import pygame
import os
from settings import *

def load_frames(folder_path, scale=1.0):
    frames = []
    for file in sorted(os.listdir(folder_path)):
        img = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
        if scale != 1.0:
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
        frames.append(img)
    return frames


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, target, groups):
        super().__init__(groups.all_sprites, groups.bullets)
        self.groups = groups

        self.image = pygame.image.load(
            os.path.join(BASE_DIR, "images", "gun", "bullet.png")
        ).convert_alpha()

        self.rect = self.image.get_rect(center=pos)

        direction = pygame.Vector2(target) - pygame.Vector2(pos)
        if direction.length() == 0:
            direction = pygame.Vector2(1, 0)
        self.direction = direction.normalize()

    def update(self, dt):
        self.rect.center += self.direction * BULLET_SPEED * dt

        # kill buiten scherm
        if (
            self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.bottom < 0 or self.rect.top > HEIGHT
        ):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups, enemy_type, impact_sound):
        super().__init__(groups.all_sprites, groups.enemies)
        self.groups = groups
        self.player = player
        self.impact_sound = impact_sound

        # frames 0-3 uit images/enemies/<type>/
        folder = os.path.join(BASE_DIR, "images", "enemies", enemy_type)
        self.frames = load_frames(folder, 1.0)
        self.frame_index = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)

    def animate(self, dt):
        self.frame_index += ENEMY_ANIMATION_SPEED * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        # bewegen naar player
        direction = pygame.Vector2(self.player.rect.center) - pygame.Vector2(self.rect.center)
        if direction.length() > 0:
            direction.normalize_ip()
        self.rect.center += direction * ENEMY_SPEED * dt

        self.animate(dt)

        # bullet hit => enemy weg + sound
        if pygame.sprite.spritecollide(self, self.groups.bullets, True):
            self.impact_sound.play()
            self.kill()

        # damage bij aanraken
        if self.rect.colliderect(self.player.rect):
            self.player.health -= ENEMY_DAMAGE_PER_SEC * dt


