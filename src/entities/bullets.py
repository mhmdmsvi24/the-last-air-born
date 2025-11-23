import math
import random

import pygame

from config import Config as config


class Bullet(pygame.sprite.Sprite):
    """A projectile fired by player or enemy entities.

    This class handles bullet creation, movement, direction variance,
    and automatic removal when going off-screen.

    Attributes:
        image (pygame.Surface): The rendered bullet sprite.
        rect (pygame.Rect): Hitbox and position on the screen.
        x (float): Continuous horizontal position for smooth movement.
        y (float): Continuous vertical position for smooth movement.
        vx (float): Horizontal velocity component.
        vy (float): Vertical velocity component.
        direction (str): Bullet direction, typically "top" or "bottom".
    """

    def __init__(
        self,
        x: float,
        y: float,
        color: dict[str:int],
        size: list[int],
        bullet_speed: float,
        variance: float,
        direction: str = "top",
    ) -> None:
        """Initialize a bullet with physics-based movement.

        Args:
            x (float): Initial X position.
            y (float): Initial Y position.
            color (tuple[int, int, int, int]): RGBA bullet color.
            size (list[int]): Width and height of the bullet rectangle.
            bullet_speed (float): Base travel speed.
            variance (float): Random angular variance (radians).
            direction (str, optional): Movement direction ("top" or "bottom").
                Defaults to "top".
        """
        super().__init__()

        # Create sprite surface
        self.image = pygame.Surface((5, 15), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image,
            color,
            size,
            border_top_left_radius=10,
            border_top_right_radius=10,
        )
        self.rect = self.image.get_rect(center=(x, y))

        # Float-based coordinates
        self.x: float = float(x)
        self.y: float = float(y)
        # Bullet angle
        base_angle = -math.pi / 2 if direction == "top" else math.pi / 2
        angle = base_angle + random.uniform(-variance, variance)

        # Velocity components
        self.vx: float = math.cos(angle) * bullet_speed
        self.vy: float = math.sin(angle) * bullet_speed

        self.direction: str = direction

    def update(self, delta_time: float) -> None:
        """Update bullet position and remove it if it leaves the screen.

        Args:
            delta_time (float): Frame delta time (seconds or ms-based depending on game loop).
        """
        # Apply continuous movement
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        # Sync integer rect position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        # Remove when out of screen bounds
        if self.direction == "top" and self.rect.bottom < 0:
            self.kill()
        elif self.direction == "bottom" and self.rect.top > config.VIRTUAL_HEIGHT:
            self.kill()
