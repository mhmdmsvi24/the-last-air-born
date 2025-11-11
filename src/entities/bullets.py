# import math
# import random

# import pygame

# from config import Config as config


# class Bullet(pygame.sprite.Sprite):

#     def __init__(self, x, y, color, size, bullet_speed, variance):
#         super().__init__()
#         self.image = pygame.Surface((5, 15), pygame.SRCALPHA)
#         pygame.draw.rect(self.image, color, size)
#         self.rect = self.image.get_rect(center=(x, y))
#         # Store variance
#         self.vx = (
#             math.sin(variance + random.uniform(-variance, variance)) * bullet_speed
#         )
#         self.vy = (
#             -math.cos(variance + random.uniform(-variance, variance)) * bullet_speed
#         )

#     def update(self, direction="top"):
#         if direction == "top":
#             # bullets move UP
#             self.rect.x += int(self.vx)
#             self.rect.y += int(self.vy)
#             # remove off-screen bullets for performance
#             if self.rect.bottom < 0:
#                 self.kill()

#         elif direction == "bottom":
#             # bullets move DOWN
#             self.rect.x -= int(self.vx)
#             self.rect.y -= int(self.vy)
#             # remove off-screen bullets for performance
#             if self.rect.top > config.VIRTUAL_HEIGHT:
#                 self.kill()

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

        # Base angle in radians: straight up (-pi/2) or straight down (pi/2)
        if direction == "top":
            base_angle = -math.pi / 2  # upward
        else:
            base_angle = math.pi / 2  # downward

        # Add random variance
        angle = base_angle + random.uniform(-variance, variance)

        # Compute velocity
        self.vx = math.cos(angle) * bullet_speed
        self.vy = math.sin(angle) * bullet_speed

        self.direction = direction

    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

        # Remove off-screen bullets
        if self.direction == "top" and self.rect.bottom < 0:
            self.kill()
        elif self.direction == "bottom" and self.rect.top > config.VIRTUAL_HEIGHT:
            self.kill()
