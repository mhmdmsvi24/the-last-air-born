import pygame

pygame.init()

import sys

from config import Config as config
from entities.plane import Plane
from utils.helpers import load_image, scale_image, show_fps


def main(state="P"):

    if state == "P":
        game_loop()
    elif state == "L":
        game_loop()


def game_loop():
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    main_plane_img = scale_image(load_image("graphics", "plane-1.png"), 30, 55)
    main_plane = Plane(8, 10, 250, 1, main_plane_img)
    main_plane.rect.center = config.v_screen.get_rect().center
    all_sprites.add(main_plane)

    enemy_plane_img = pygame.transform.rotate(
        scale_image(load_image("graphics", "enemy-2.png"), 30, 55), 180
    )
    enemy_plane = Plane(6, 1, 999, 1, enemy_plane_img)
    enemy_plane.rect.centerx = config.v_screen.get_rect().centerx
    all_sprites.add(enemy_plane)

    while True:
        config.v_screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            main_plane.move("top")
        if keys[pygame.K_s]:
            main_plane.move("bottom")
        if keys[pygame.K_a]:
            main_plane.move("left")
        if keys[pygame.K_d]:
            main_plane.move("right")

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            main_plane.shoot(bullets)

        main_plane_to_enemy_offset = main_plane.check_offest(enemy_plane)
        if main_plane.mask.overlap(enemy_plane.mask, main_plane_to_enemy_offset):
            main("L")
            break

        bullets.update()
        all_sprites.draw(config.v_screen)
        bullets.draw(config.v_screen)

        show_fps()
        scaled_surface = pygame.transform.smoothscale(
            config.v_screen, (config.scaled_width, config.scaled_height)
        )
        config.screen.fill((0, 0, 0))
        config.screen.blit(scaled_surface, (config.offset_x, config.offset_y))
        pygame.display.flip()
        config.clock.tick(config.FPS)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
