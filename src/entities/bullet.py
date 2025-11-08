import pygame

from config import Config as config


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10):
        super().__init__()
        self.image = pygame.Surface((5, 15), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 0), [0, 0, 2, 8])  # yellow bullet
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        # Remove the bullet if it goes off screen
        if self.rect.bottom < 0:
            self.kill()
