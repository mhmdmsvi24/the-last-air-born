import pygame

from config import Config as config
from entities.enemy_manager import EnemyManager
from entities.planes import Player
from utils.helpers import load_image, scale_image


class GameState:
    """
    Game State is a one time init class for things that need to be initialized only once, like images, groups, managers
    """

    def __init__(self):
        # Player
        main_plane_img = scale_image(load_image("graphics", "plane-1.webp"), 30, 55)
        self.player = Player(config.v_screen, 150, 1, main_plane_img)
        self.player.rect.bottom = config.v_screen_rect.bottom * 0.9
        self.player.rect.centerx = config.v_screen_rect.centerx
        self.player_group = pygame.sprite.Group(self.player)

        # Enemies
        self.enemies_bullets_group = pygame.sprite.Group()
        self.enemy_manager = EnemyManager(self.enemies_bullets_group)
        self.enemy_manager.load_wave()
        self.enemies_group = self.enemy_manager.get_current_group()

        # Effects
        self.explosions_group = pygame.sprite.Group()
