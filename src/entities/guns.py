import math
from typing import Tuple

from config import Config as config
from entities.bullets import Bullet
from utils.helpers import load_json


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

    def __init__(self, enemy: bool = False) -> None:
        """
        Initialize the basic gun and load weapon stats.

        Args:
            enemy (bool): Whether this gun belongs to an enemy.
                Enemy guns shoot slower, weaker, and slower-speed bullets.
        """
        self.gun_level = 1

        gun_data = load_json(config.root_dir / "src" / "data" / "guns.json")
        self.current_gun = gun_data["basic_gun"][str(self.gun_level)]

        # Bullet color (RGB)
        self.bullet_color = (
            self.current_gun["color"]["r"],
            self.current_gun["color"]["g"],
            self.current_gun["color"]["b"],
        )

        # Core bullet attributes
        self.bullet_size = int(self.current_gun["size"])
        self.bullet_velocity_variance = float(self.current_gun["velocity_variance"])

        # Gun behavior varies if used by an enemy
        if not enemy:
            self.shooting_delay = int(self.current_gun["delay"])
            self.bullet_damage = int(self.current_gun["damage"])
            self.bullet_speed = float(self.current_gun["speed"])
        else:
            self.shooting_delay = int(self.current_gun["delay"] * 10)
            self.bullet_damage = int(math.ceil(self.current_gun["damage"] / 2))
            self.bullet_speed = float(math.ceil(self.current_gun["speed"] / 3))

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
            speed=self.bullet_speed,
            velocity_variance=self.bullet_velocity_variance,
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
