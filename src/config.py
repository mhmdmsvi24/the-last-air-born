from pathlib import Path

import pygame


class Config:
    VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 640, 360
    pygame.display.set_caption("The Last Air Born (proto)")

    font = pygame.font.SysFont(None, 18)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    v_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    v_screen_rect = v_screen.get_rect()

    display_info = pygame.display.Info()
    REAL_WIDTH, REAL_HEIGHT = display_info.current_w, display_info.current_h

    scale_x = REAL_WIDTH / VIRTUAL_WIDTH
    scale_y = REAL_HEIGHT / VIRTUAL_HEIGHT
    scale = min(scale_x, scale_y)  # maintain aspect ratio
    scaled_width = int(VIRTUAL_WIDTH * scale)
    scaled_height = int(VIRTUAL_HEIGHT * scale)

    offset_x = (REAL_WIDTH - scaled_width) // 2
    offset_y = (REAL_HEIGHT - scaled_height) // 2

    root_dir = Path(__file__).resolve().parent.parent
