import math
import random

import pygame

from config import Config as config


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, bullet_speed, variance, direction="top"):
        super().__init__()
        self.image = pygame.Surface((5, 15), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, size)
        self.rect = self.image.get_rect(center=(x, y))

        # Float positions
        self.x = float(x)
        self.y = float(y)

        # Base angle
        base_angle = -math.pi / 2 if direction == "top" else math.pi / 2
        angle = base_angle + random.uniform(-variance, variance)

        # Velocity (float)
        self.vx = math.cos(angle) * bullet_speed
        self.vy = math.sin(angle) * bullet_speed

        self.direction = direction

    def update(self, delta_time):
        # Update float positions using delta_time
        self.x += int(self.vx * delta_time)
        self.y += self.vy * delta_time

        # Sync to rect (int)
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Remove off-screen bullets
        if self.direction == "top" and self.rect.bottom < 0:
            self.kill()
        elif self.direction == "bottom" and self.rect.top > config.VIRTUAL_HEIGHT:
            self.kill()
