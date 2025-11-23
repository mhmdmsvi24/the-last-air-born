import math

import pygame
from pygame.mask import Mask
from pygame.rect import Rect
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from config import Config as config
from entities.animations import Explosion
from entities.guns import BasicGun
from utils.helpers import load_spritesheet, transparent_image


class Plane(Sprite):
    """Base plane entity with movement, shooting, collision handling, and death effects."""

    surface: Surface
    rect: Rect
    mask: Mask
    image: Surface

    gun: BasicGun
    bullets_group: Group

    speed: float
    hp: int
    is_alive: bool
    last_shot: int

    def __init__(self, surface: Surface, speed: float, hp: int, image: Surface) -> None:
        super().__init__()
        self.plane, self.rect, self.mask = transparent_image(image)
        self.image = self.plane
        self.surface = surface

        # Weapons
        self.gun = BasicGun()
        self.bullets_group: Group = Group()
        self.last_shot: int = pygame.time.get_ticks()

        # Status
        self.is_alive: bool = True
        self.speed = float(speed)
        self.hp = int(hp)

    def move(self, x: float, y: float) -> None:
        """
        Move the plane to a specific (x, y) center position.

        Args:
            x: X-coordinate for the plane center.
            y: Y-coordinate for the plane center.
        """
        self.rect.center = (x, y)
        self.rect.clamp_ip(config.v_screen.get_rect())

    def shoot(self, mouse_buttons: tuple[bool, bool, bool]) -> None:
        """
        Fire bullets if the plane is alive and the left mouse button is pressed.

        Args:
            mouse_buttons: Tuple from pygame.mouse.get_pressed()
        """
        if self.is_alive and mouse_buttons[0]:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.gun.shooting_delay:
                self.last_shot = now
                bullet = self.gun.create_bullet((self.rect.midtop[0], self.rect.top))
                self.bullets_group.add(bullet)

    def take_damage(
        self, bullet_list: list[Sprite], explosion_group: Group, damage: int
    ) -> None:
        """
        Apply damage for each incoming bullet and trigger death if HP reaches zero.

        Args:
            bullet_list: Bullets that hit the plane.
            explosion_group: Group to spawn explosion effects.
            damage: Damage applied per bullet.
        """
        for bullet in bullet_list:
            bullet.kill()
            self.hp -= damage

            if self.hp <= 0:
                self.die(explosion_group)
                return

    def check_offset(self, target: Sprite) -> tuple[int, int]:
        """
        Calculate position offset between this plane and another target.

        Args:
            target: Target to compare against.

        Returns:
            (dx, dy) difference in positions.
        """
        return (self.rect.x - target.rect.x, self.rect.y - target.rect.y)

    def die(self, explosion_group: Group) -> None:
        """
        Kill the plane and spawn an explosion animation.

        Args:
            explosion_group: Group to add the explosion into.
        """
        explosion_frames = load_spritesheet(
            "graphics/sprites", "explosion.png", 60, 60, 4
        )
        explosion = Explosion(self.rect.center, explosion_frames)
        explosion_group.add(explosion)

        self.is_alive = False
        self.kill()


class Player(Plane):
    """Player-controlled plane with WASD movement."""

    def move(self, keys: pygame.key.ScancodeWrapper, delta_time: float) -> None:
        """
        Move based on keyboard input and frame delta time.

        Args:
            keys: Keyboard state.
            delta_time: Time multiplier for frame-independent movement.
        """
        if keys[pygame.K_w]:
            self.rect.y -= self.speed * delta_time
        if keys[pygame.K_s]:
            self.rect.y += math.ceil(self.speed * delta_time)
        if keys[pygame.K_a]:
            self.rect.x -= self.speed * delta_time
        if keys[pygame.K_d]:
            self.rect.x += math.ceil(self.speed * delta_time)

        self.rect.clamp_ip(config.v_screen.get_rect())


class Enemy(Plane):
    """Enemy plane with automatic movement paths and timed shooting."""

    start_x: float | None
    start_y: float | None
    target_x: float | None
    target_y: float | None
    travel_duration: int
    travel_start_time: int | None
    reached_target: bool

    def __init__(
        self,
        surface: Surface,
        speed: float,
        hp: int,
        image: Surface,
        bullets_group: Group,
    ) -> None:
        super().__init__(surface, speed, hp, image)
        self.gun = BasicGun(enemy=True)
        self.bullets_group = bullets_group

        # Movement interpolation variables
        self.start_x = self.start_y = None
        self.target_x = self.target_y = None
        self.travel_duration = 3000  # ms
        self.travel_start_time = None
        self.reached_target = False

    def set_path(self, start_pos: tuple[int, int], target_pos: tuple[int, int]) -> None:
        """
        Initialize movement path using linear interpolation.

        Args:
            start_pos: Starting (x, y) coordinates.
            target_pos: Destination (x, y) coordinates.
        """
        self.start_x, self.start_y = start_pos
        self.target_x, self.target_y = target_pos

        self.rect.center = start_pos
        self.travel_start_time = pygame.time.get_ticks()
        self.reached_target = False

    def shoot(self) -> None:
        """Automatically fire bullets downward on cooldown."""
        now = pygame.time.get_ticks()

        if self.is_alive and now - self.last_shot > self.gun.shooting_delay:
            self.last_shot = now
            bullet = self.gun.create_bullet(
                (self.rect.midbottom[0] + 2, self.rect.bottom), "bottom"
            )
            self.bullets_group.add(bullet)

    def auto_move(self) -> None:
        """
        Move towards target position using linear interpolation over time.
        Stops once the destination is reached.
        """
        if self.reached_target or self.travel_start_time is None:
            return

        now = pygame.time.get_ticks()
        elapsed = now - self.travel_start_time
        t = min(1.0, elapsed / self.travel_duration)

        if self.start_x is None or self.target_x is None:
            return

        # LERP
        new_x = self.start_x + (self.target_x - self.start_x) * t
        new_y = self.start_y + (self.target_y - self.start_y) * t

        self.rect.center = (new_x, new_y)

        if t >= 1.0:
            self.reached_target = True
