from pathlib import Path

import pygame


class Config:
    """Overall game configs such as width, heights, display_info, ..."""

    VIRTUAL_WIDTH, VIRTUAL_HEIGHT = 640, 360
    pygame.display.set_caption("The Last Air Born (proto)")

    font = pygame.font.SysFont(None, 18)
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    v_screen = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT))
    v_screen_rect = v_screen.get_rect()

    display_info = pygame.display.Info()
    REAL_WIDTH, REAL_HEIGHT = display_info.current_w, display_info.current_h

    scale_x = REAL_WIDTH / VIRTUAL_WIDTH  # e.g. 1920 / 640 = 3
    scale_y = REAL_HEIGHT / VIRTUAL_HEIGHT  # e.g. 1080 / 360 = 3

    scale = min(scale_x, scale_y)  # picks minimum scale to avoid stretch

    scaled_width = int(VIRTUAL_WIDTH * scale)
    scaled_height = int(VIRTUAL_HEIGHT * scale)

    # calculate the empty space/padding left from each sides if the users resolution is not optimal
    offset_x = (REAL_WIDTH - scaled_width) // 2
    offset_y = (REAL_HEIGHT - scaled_height) // 2

    root_dir = Path(__file__).resolve().parent.parent
