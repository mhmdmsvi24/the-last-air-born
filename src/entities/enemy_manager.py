import pygame
from pygame.sprite import Group
from pygame.surface import Surface

from config import Config as config
from entities.planes import Enemy
from utils.helpers import load_image, load_json, planes_to_row_cols, scale_image


class EnemyManager:
    """Handles creation, updating, and rendering of enemy waves."""

    def __init__(self, enemies_bullets_group: Group) -> None:
        """Initialize the enemy manager.

        Args:
            enemies_bullets_group (pygame.sprite.Group): Shared group for all enemy-fired bullets.
        """
        self.current_wave: int = 1
        self.waves_data: dict = load_json(
            config.root_dir / "src" / "data" / "waves.json"
        )
        self.current_wave_group: Group = pygame.sprite.Group()
        self.enemies_bullets_group: Group = enemies_bullets_group

        # Enemies Type Data
        self.enemies_type_data: dict = load_json(
            config.root_dir / "src" / "data" / "enemy-type.json"
        )

    def load_wave(self) -> None:
        """Loads and spawns the enemies for the current wave.

        This sets up:
        - enemy plane graphics
        - formation layout (rows & columns)
        - each enemy’s start and target position
        """
        enemies_wave_data = self.waves_data[str(self.current_wave)]

        enemies_count: int = enemies_wave_data["enemies_count"]

        enemy_type: str = enemies_wave_data["enemy_type"]
        enemy_level: int = enemies_wave_data["enemies_level"]

        # --- Loading Specific Enemy data using enemy-type.json
        enemies_type_level: int = self.enemies_type_data[enemy_type][str(enemy_level)]

        enemies_hp = enemies_type_level["hp"]
        enemies_gun_level = enemies_type_level["gun_level"]
        enemies_gun_type = enemies_type_level["gun_type"]

        # Load and rotate enemy sprite
        enemy_plane_img = pygame.transform.rotate(
            scale_image(load_image("graphics", "enemy-2.webp"), 30, 55),
            180,
        )

        enemy_plane_width = enemy_plane_img.get_width()
        enemy_plane_height = enemy_plane_img.get_height()

        # Layout calculations
        spacing: int = int(enemy_plane_width * 0.5)
        padding: int = int(config.VIRTUAL_WIDTH * 0.1)

        rows, cols = planes_to_row_cols(
            enemy_plane_width, enemies_count, spacing, padding
        )

        row_spacing = int(enemy_plane_height * 1.5)
        total_width = cols * enemy_plane_width + (cols - 1) * spacing
        start_x = (config.VIRTUAL_WIDTH - total_width) // 2
        start_y = int(config.VIRTUAL_HEIGHT * 0.15)

        count_spawned = 0

        for row in range(rows):
            for col in range(cols):

                if count_spawned >= enemies_count:
                    return

                enemy = Enemy(
                    config.v_screen,
                    speed=3,
                    hp=enemies_hp,
                    image=enemy_plane_img,
                    bullets_group=self.enemies_bullets_group,
                    gun_type=enemies_gun_type,
                    gun_level=enemies_gun_level,
                )

                target_x = start_x + col * (enemy_plane_width + spacing)
                target_y = start_y + row * row_spacing

                start_pos = (target_x, -50)

                enemy.set_path(start_pos, (target_x, target_y))

                self.current_wave_group.add(enemy)
                count_spawned += 1

    def get_current_group(self) -> Group:
        """Returns the sprite group containing all active enemies.

        Returns:
            pygame.sprite.Group: Active enemy group.
        """
        return self.current_wave_group

    def update(self, dt: float) -> None:
        """Updates all active enemies.

        Args:
            dt (float): Delta time for movement updates.
        """
        self.current_wave_group.update(dt)

    def draw(self, surface: Surface) -> None:
        """Draws all active enemies onto the provided surface.

        Args:
            surface (pygame.Surface): The rendering surface.
        """
        self.current_wave_group.draw(surface)

    def next_wave(self) -> None:
        """Advances to the next wave and loads it."""
        self.current_wave += 1
        self.current_wave_group.empty()
        self.load_wave()
