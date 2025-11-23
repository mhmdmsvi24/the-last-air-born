import json
import os
from typing import Tuple

import pygame

from config import Config as config
from entities.guns import BasicGun
from game_types import GunType
from utils.utils import load_json


def show_fps() -> None:
    """Render and display the current FPS on the virtual screen."""
    fps = int(config.clock.get_fps())
    fps_text = pygame.font.SysFont(None, 16).render(f"FPS: {fps}", True, (255, 0, 255))
    config.v_screen.blit(
        fps_text, (config.VIRTUAL_WIDTH * 0.9, config.VIRTUAL_HEIGHT * 0.05)
    )


def load_image(directory: str, image_name: str) -> pygame.Surface:
    """Load an image from the assets directory.

    Args:
        directory (str): Subfolder inside assets containing the image.
        image_name (str): Name of the image file.

    Returns:
        pygame.Surface: Loaded image surface.
    """
    path = os.path.join(
        os.path.dirname(__file__), f"../../assets/{directory}/{image_name}"
    )
    image = pygame.image.load(path)
    return image


def scale_image(image: pygame.Surface, x: int, y: int) -> pygame.Surface:
    """Scale an image to a specific width and height.

    Args:
        image (pygame.Surface): Image to scale.
        x (int): Target width.
        y (int): Target height.

    Returns:
        pygame.Surface: Scaled image surface.
    """
    return pygame.transform.scale(image, (x, y))


def transparent_image(
    img: pygame.Surface,
) -> Tuple[pygame.Surface, pygame.Rect, pygame.mask.Mask]:
    """Extract a trimmed, alpha-enabled image along with its rect and mask.

    Useful for pixel-perfect collision detection.

    Args:
        img (pygame.Surface): Source image.

    Returns:
        tuple: A tuple containing:
            - pygame.Surface: Trimmed image surface.
            - pygame.Rect: Rect of the trimmed surface.
            - pygame.mask.Mask: Collision mask of the image.
    """
    image = img.convert_alpha()
    image_mask = pygame.mask.from_surface(image)
    bbox = image_mask.get_bounding_rects()[0]

    image = image.subsurface(bbox).copy()
    image_rect = image.get_rect()

    return (image, image_rect, image_mask)


def scale_n_build_screen() -> None:
    """Scale the virtual screen to the user's window size, center it, and draw it."""
    scaled_surface = pygame.transform.smoothscale(
        config.v_screen, (config.scaled_width, config.scaled_height)
    )
    config.screen.fill((0, 0, 0))
    config.screen.blit(scaled_surface, (config.offset_x, config.offset_y))
    pygame.display.flip()


def load_spritesheet(
    path: str, name: str, frame_width: int, frame_height: int, num_frames: int
) -> list[pygame.Surface]:
    """Load a spritesheet and extract individual animation frames.

    Args:
        path (str): Directory inside assets containing the spritesheet.
        name (str): Filename of the spritesheet.
        frame_width (int): Width of each frame.
        frame_height (int): Height of each frame.
        num_frames (int): Number of animation frames to extract.

    Returns:
        list[pygame.Surface]: List of individual frame surfaces.
    """
    sheet = load_image(path, name).convert_alpha()
    frames = []

    for i in range(num_frames):
        frame = sheet.subsurface(
            pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        )
        frames.append(frame)

    return frames


def get_guns() -> dict:
    """Load gun configuration data from guns.json.

    Returns:
        dict: Parsed gun configuration dictionary.
    """
    data_file = config.root_dir / "src" / "data" / "guns.json"

    with data_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def planes_to_row_cols(
    planes_width: int, planes_count: int, spacing: int, padding: int
) -> Tuple[int, int]:
    """Determine how many enemy planes can fit per row and how many rows are needed.

    Ensures the formation fits within the virtual screen width by decreasing
    columns and increasing rows as needed.

    Args:
        planes_width (int): Width of a single plane sprite.
        planes_count (int): Number of planes in the wave.
        spacing (int): Horizontal spacing between planes.
        padding (int): Padding on both sides of the formation.

    Returns:
        tuple[int, int]: (rows, columns) for plane placement.
    """
    screen_width = config.VIRTUAL_WIDTH

    gap = spacing * (planes_count - 1)
    real_padding = padding * 2

    total_width = planes_width * planes_count + gap + real_padding

    rows = 1
    cols = planes_count

    while total_width > screen_width:
        cols -= 1
        total_width = planes_width * cols + (cols * spacing) + real_padding
        rows += 1

    return (rows, cols)


def load_gun(gun_type: str, gun_level: int, enemy: bool = False) -> GunType:
    """Uses waves.json data to get the enemy level and type and loads gun data from enemy-guns.json

    Args:
      gun_type (str)
      gun_level (int)
      enemy (bool) = True

    Returns:
      GunType
    """
    if not enemy:
        guns = load_json(config.root_dir / "src" / "data" / "player-guns.json")
    else:
        guns = load_json(config.root_dir / "src" / "data" / "enemy-guns.json")

    gun_data = guns[gun_type][str(gun_level)]

    if gun_type == "basic_gun":
        return BasicGun(gun_level, gun_data)
