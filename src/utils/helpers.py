import json
import os

import pygame

from config import Config as config


def show_fps():
    fps = int(config.clock.get_fps())
    fps_text = pygame.font.SysFont(None, 16).render(f"FPS: {fps}", True, (255, 0, 255))
    config.v_screen.blit(
        fps_text, (config.VIRTUAL_WIDTH * 0.9, config.VIRTUAL_HEIGHT * 0.05)
    )


def load_image(directory, image_name):
    path = os.path.join(
        os.path.dirname(__file__), f"../../assets/{directory}/{image_name}"
    )
    image = pygame.image.load(path)

    return image


def scale_image(image, x, y):
    return pygame.transform.scale(image, (x, y))


def transparent_image(img):
    image = img.convert_alpha()
    image_mask = pygame.mask.from_surface(image)
    bbox = image_mask.get_bounding_rects()[0]
    image = image.subsurface(bbox).copy()
    image_rect = image.get_rect()

    return (image, image_rect, image_mask)


def scale_n_build_screen():
    scaled_surface = pygame.transform.smoothscale(
        config.v_screen, (config.scaled_width, config.scaled_height)
    )
    config.screen.fill((0, 0, 0))
    config.screen.blit(scaled_surface, (config.offset_x, config.offset_y))
    pygame.display.flip()


def load_spritesheet(path, name, frame_width, frame_height, num_frames):
    sheet = load_image(path, name).convert_alpha()
    frames = []
    for i in range(num_frames):
        frame = sheet.subsurface(
            pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        )
        frames.append(frame)
    return frames


def get_guns():
    data_file = config.root_dir / "src" / "data" / "guns.json"

    with data_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def load_json(file_path):
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    return data
