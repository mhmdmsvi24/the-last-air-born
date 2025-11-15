import pygame

from config import Config as config
from entities.planes import Enemy
from utils.helpers import load_image, load_json, planes_to_row_cols, scale_image


class EnemyManager:
    def __init__(self):
        self.current_wave = 1
        self.waves_data = load_json(config.root_dir / "src" / "data" / "waves.json")
        self.current_wave_group = pygame.sprite.Group()

    def load_wave(self):
        enemies_wave_data = self.waves_data[f"{self.current_wave}"]
        enemies_count = enemies_wave_data["enemies_count"]
        # enemies_hp = enemies_wave_data["hp"]
        enemies_hp = 1

        # Load & rotate enemy plane
        enemy_plane_img = pygame.transform.rotate(
            scale_image(load_image("graphics", "enemy-2.webp"), 30, 55), 180
        )
        enemy_plane_width = enemy_plane_img.get_width()
        enemy_plane_height = enemy_plane_img.get_height()

        # Compute rows & columns
        spacing = int(enemy_plane_width * 0.5)
        padding = int(config.VIRTUAL_WIDTH * 0.1)

        rows, cols = planes_to_row_cols(
            enemy_plane_width, enemies_count, spacing, padding
        )

        # Vertical spacing between rows
        row_spacing = int(enemy_plane_height * 1.5)

        # Center formation horizontally
        total_width = cols * enemy_plane_width + (cols - 1) * spacing
        start_x = (config.VIRTUAL_WIDTH - total_width) // 2

        start_y = int(config.VIRTUAL_HEIGHT * 0.15)  # lifted slightly for better look

        count_spawned = 0

        for row in range(rows):
            for col in range(cols):
                if count_spawned >= enemies_count:
                    return

                enemy = Enemy(
                    config.v_screen,  # surface
                    3,  # speed
                    enemies_hp,  # hp
                    enemy_plane_img,  # image
                )

                target_x = start_x + col * (enemy_plane_width + spacing)
                target_y = start_y + row * row_spacing

                enemy.target_x = target_x
                enemy.target_y = target_y

                start_pos = (target_x, -50)

                enemy.set_path(start_pos, (target_x, target_y))

                self.current_wave_group.add(enemy)
                count_spawned += 1

    def get_current_group(self):
        return self.current_wave_group

    def update(self, dt):
        self.current_wave_group.update(dt)

    def draw(self, surface):
        self.current_wave_group.draw(surface)

    def next_wave(self):
        self.current_wave += 1
        self.current_wave_group.empty()
        self.load_wave()
