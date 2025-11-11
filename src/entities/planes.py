import pygame

from config import Config as config
from entities.animations import Explosion
from entities.bullets import Bullet
from entities.guns import BasicGun, DualBarrelGun, MiniGun
from utils.helpers import load_spritesheet, transparent_image


class Plane(pygame.sprite.Sprite):

    def __init__(self, surface: pygame.SurfaceType, speed, hp, image):
        super().__init__()
        self.plane, self.rect, self.mask = transparent_image(image)
        self.image = self.plane
        self.surface = surface
        #
        self.gun = BasicGun()
        self.bullets_group = pygame.sprite.Group()
        self.last_shot = pygame.time.get_ticks()
        #
        self.is_alive = True
        self.speed = speed
        self.hp = hp

    def move(self, x, y):
        self.rect.center = (x, y)
        self.rect.clamp_ip(config.v_screen.get_rect())

    def shoot(self, mouse_buttons):
        if self.is_alive and mouse_buttons[0]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.gun.shooting_delay:
                self.last_shot = now
                bullet = self.gun.create_bullet((self.rect.midtop[0], self.rect.top))
                self.bullets_group.add(bullet)

    def take_damage(self, hits, explosion_group, damage):
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                bullet.kill()
                enemy.hp -= damage
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
    def __init__(self, surface: pygame.SurfaceType, speed, hp, image):
        super().__init__(surface, speed, hp, image)

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

    def __init__(self, surface: pygame.SurfaceType, speed, hp, image):
        super().__init__(surface, speed, hp, image)
        self.gun = BasicGun(enemy=True)

    def shoot(self):
        now = pygame.time.get_ticks()

        if self.is_alive and now - self.last_shot > self.gun.shooting_delay:
            self.last_shot = now
            bullet = self.gun.create_bullet(
                (self.rect.midbottom[0] + 2, self.rect.bottom), "bottom"
            )
            self.bullets_group.add(bullet)
