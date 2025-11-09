import pygame

from config import Config as config
from entities.bullet import Bullet
from utils.helpers import transparent_image


class Plane(pygame.sprite.Sprite):
    def __init__(self, speed, hp, ammo, damage, image):
        super().__init__()
        self.level = 1
        self.perks = []
        self.plane, self.rect, self.mask = transparent_image(image)
        self.image = self.plane
        #
        self.ammo = 10
        self.bullet = pygame.Rect(*self.rect.midright, 2, 10)
        #
        self.speed = speed
        self.hp = hp
        self.ammo = ammo
        self.dmg = damage
        self.shoot_delay = 200
        self.last_shot = pygame.time.get_ticks()

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

    def shoot(self, bullets_group, mouse_buttons):
        if mouse_buttons[0]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                bullet_right = Bullet(self.rect.midright[0] - 5, self.rect.top + 20, 12)
                bullet_left = Bullet(self.rect.midleft[0] + 5, self.rect.top + 20, 12)
                bullets_group.add(bullet_left, bullet_right)

    def take_damage(self, hits):
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                bullet.kill()
                enemy.hp -= self.dmg
                if enemy.hp <= 0:
                    enemy.kill()

    def check_offset(self, target):
        offset = (
            self.rect.x - target.rect.x,
            self.rect.y - target.rect.y,
        )

        return offset

    def blitme(self, surface: pygame.SurfaceType):
        surface.blit(self.plane, self.rect)
