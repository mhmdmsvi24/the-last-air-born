from enum import Enum
from typing import Protocol, Tuple

from entities.bullets import Bullet


class GameStateTypes(Enum):
    """
    Game State Types for different state of the game
    """

    MENU = "MENU"
    SETTING = "SETTING"
    START = "START"
    QUIT = "QUIT"
    EXIT = "EXIT"

    DEFAULT = MENU


class GunType(Protocol):
    """Contract for all guns. Only for static type checking."""

    gun_level: int
    bullet_color: Tuple[int, int, int]
    bullet_size: int
    shooting_delay: int
    bullet_damage: int
    bullet_velocity_variance: float
    bullet_speed: float

    def create_bullet(
        self, shooting_pos: Tuple[int, int], direction: str = "top"
    ) -> Bullet: ...

    def upgrade_gun(self) -> None: ...
