import math
from typing import Tuple

from entities.bullets import Bullet


class BasicGun:
    """Basic single-barrel gun used by the player or enemies."""

    gun_level: int
    current_gun: dict
    bullet_color: Tuple[int, int, int]
    bullet_size: int
    shooting_delay: int
    bullet_damage: int
    bullet_velocity_variance: float
    bullet_speed: float

    def __init__(self, gun_level: int, gun_data: dict) -> None:
        """
        Initialize the basic gun and load weapon stats.

        Args:
            enemy (bool): Whether this gun belongs to an enemy.
                Enemy guns shoot slower, weaker, and slower-speed bullets.
        """
        self.gun_level = gun_level
        self.gun_data = gun_data

        # Bullet color (RGB)
        self.bullet_color = (
            self.gun_data["color"]["r"],
            self.gun_data["color"]["g"],
            self.gun_data["color"]["b"],
        )

        # Core bullet attributes
        self.bullet_size = self.gun_data["size"]
        self.bullet_velocity_variance = float(self.gun_data["velocity_variance"])

        # Gun behavior varies if used by an enemy
        self.shooting_delay = int(self.gun_data["delay"])
        self.bullet_damage = int(self.gun_data["damage"])
        self.bullet_speed = float(self.gun_data["speed"])

    def create_bullet(
        self, shooting_pos: Tuple[int, int], direction: str = "top"
    ) -> Bullet:
        """
        Create and return a bullet fired from this gun.

        Args:
            shooting_pos (tuple[int, int]):
                (x, y) position from which the bullet is fired.
            direction (str, optional):
                Direction of the bullet. Defaults to "top".
                Accepted values: "top", "bottom", "left", "right".

        Returns:
            Bullet: A fully constructed bullet instance.
        """
        x, y = shooting_pos

        return Bullet(
            x=x,
            y=y,
            color=self.bullet_color,
            size=self.bullet_size,
            bullet_speed=self.bullet_speed,
            variance=self.bullet_velocity_variance,
            direction=direction,
        )

    def upgrade_gun(self) -> None:
        """
        Increase the gun level by one.

        Note:
            Gun stats are not reloaded automatically.
            You can implement auto-reload logic if needed.
        """
        self.gun_level += 1


class DualBarrelGun:
    """Placeholder for a dual-barrel gun (not implemented yet)."""

    def __init__(self) -> None:
        """Initialize a dual barrel gun."""
        pass


class MiniGun:
    """Placeholder for a minigun weapon type (not implemented yet)."""

    def __init__(self) -> None:
        """Initialize a minigun weapon."""
        pass
