import pygame

from config import Config as config
from entities.animations import Explosion
from entities.bullet import Bullet
from utils.helpers import load_spritesheet, transparent_image


class Plane(pygame.sprite.Sprite):

    def __init__(self, surface: pygame.SurfaceType, speed, hp, damage, image):
        super().__init__()
        self.level = 1
        self.perks = []
        self.plane, self.rect, self.mask = transparent_image(image)
        self.image = self.plane
        self.surface = surface
        #
        self.bullet = pygame.Rect(*self.rect.midright, 2, 10)
        #
        self.is_alive = True
        self.speed = speed
        self.hp = hp
        self.dmg = damage
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()

    def move(self, x, y):
        self.rect.center = (x, y)

        self.rect.clamp_ip(config.v_screen.get_rect())

    def shoot(self, bullets_group, mouse_buttons):
        if self.is_alive and mouse_buttons[0]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet_right = Bullet(self.rect.midright[0] - 5, self.rect.top + 20, 12)
                bullet_left = Bullet(self.rect.midleft[0] + 5, self.rect.top + 20, 12)
                bullets_group.add(bullet_left, bullet_right)

    def take_damage(self, hits, explosion_group):
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                bullet.kill()
                enemy.hp -= self.dmg
                if enemy.hp <= 0:
                    enemy.die(explosion_group)

    def check_offset(self, target):
        offset = (
            self.rect.x - target.rect.x,
            self.rect.y - target.rect.y,
        )

        return offset

    def die(self, explosion_group):
        explosion_frames = load_spritesheet(
            "graphics/sprites", "explosion.png", 60, 60, 4
        )
        explosion = Explosion(self.rect.center, explosion_frames)
        explosion_group.add(explosion)
        self.is_alive = False
        self.kill()

    def blitme(self):
        self.surface.blit(self.plane, self.rect)


class Player(Plane):
    def __init__(self, surface: pygame.SurfaceType, speed, hp, damage, image):
        super().__init__(surface, speed, hp, damage, image)

    def move(self, keys):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        self.rect.clamp_ip(config.v_screen.get_rect())


class Enemy(Plane):
    def __init__(self, surface: pygame.SurfaceType, speed, hp, damage, image):
        super().__init__(surface, speed, hp, damage, image)
        self.shoot_delay = 2000

    def shoot(self, enemy_bullet_group):
        now = pygame.time.get_ticks()

        if self.is_alive and now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet_center = Bullet(self.rect.midbottom[0], self.rect.bottom, 5)
            enemy_bullet_group.add(bullet_center)
