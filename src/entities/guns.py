import math

from config import Config as config
from entities.bullets import Bullet
from utils.helpers import load_json


class BasicGun:
    def __init__(self, enemy=False):
        self.gun_level = 10
        self.current_gun = load_json(config.root_dir / "src" / "data" / "guns.json")[
            "basic_gun"
        ][f"{self.gun_level}"]
        self.bullet_color = (
            self.current_gun["color"]["r"],
            self.current_gun["color"]["g"],
            self.current_gun["color"]["b"],
        )
        self.bullet_size = self.current_gun["size"]
        self.shooting_delay = (
            self.current_gun["delay"] if not enemy else self.current_gun["delay"] * 4
        )
        self.bullet_damage = (
            self.current_gun["damage"]
            if not enemy
            else math.ceil(self.current_gun["damage"] / 2)
        )
        self.bullet_velocity_varaince = self.current_gun["velocity_variance"]
        self.bullet_speed = (
            self.current_gun["speed"]
            if not enemy
            else math.ceil(self.current_gun["speed"] / 2)
        )

    def create_bullet(self, shooting_pos, direction="top"):
        return Bullet(
            shooting_pos[0],
            shooting_pos[1],
            self.bullet_color,
            self.bullet_size,
            self.bullet_speed,
            self.bullet_velocity_varaince,
            direction,
        )

    def upgrade_gun(self):
        self.gun_level += 1


class DualBarrelGun:
    def __init__(self):
        pass


class MiniGun:
    def __init__(self):
        pass
