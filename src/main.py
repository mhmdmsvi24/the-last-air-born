import pygame

pygame.init()

import sys

from config import Config as config
from entities.plane import Plane
from utils.helpers import load_image, scale_image, scale_n_build_screen, show_fps


def main(state="P"):

    if state == "P":
        game_loop()
    elif state == "L":
        game_loop()


def game_loop():
    # Player
    main_plane_img = scale_image(load_image("graphics", "plane-1.webp"), 30, 55)
    main_plane = Plane(8, 10, 250, 1, main_plane_img)

    # center the plane in lower center
    main_plane.rect.bottom = config.v_screen_rect.bottom * 0.9
    main_plane.rect.centerx = config.v_screen_rect.centerx

    # players bullets group for collisin detection
    main_plane_bullets = pygame.sprite.Group()

    # -----------------------------------------------------------------------------

    # Enemies
    enemy_plane_img = pygame.transform.rotate(
        scale_image(load_image("graphics", "enemy-2.webp"), 30, 55), 180
    )
    enemy_plane = Plane(6, 10, 999, 1, enemy_plane_img)

    # center the enemy plane in lower center
    # *FIX: this just centers a single plane for future planes groups that will spawn a better method is required
    enemy_plane.rect.bottom = config.v_screen_rect.bottom * 0.2
    enemy_plane.rect.centerx = config.v_screen_rect.centerx

    # enemies bullets and groups for collision detection
    enemies_group = pygame.sprite.Group()
    enemies_group.add(enemy_plane)

    enemies_bullets = pygame.sprite.Group()

    while True:
        # Clear and fill screen
        config.v_screen.fill((0, 0, 0))

        for event in pygame.event.get():
            terminate(event)

        main_plane.move(pygame.key.get_pressed())
        main_plane.shoot(main_plane_bullets, pygame.mouse.get_pressed())
        main_plane_bullets.update()

        # check if any of the players bullers hit enemy planes
        player_damage_enemy = pygame.sprite.groupcollide(
            enemies_group, main_plane_bullets, False, True, pygame.sprite.collide_mask
        )

        if player_damage_enemy:
            enemy_plane.take_damage(player_damage_enemy)

        # draw every thing with latest updates
        main_plane.blitme(config.v_screen)
        enemies_group.draw(config.v_screen)
        main_plane_bullets.draw(config.v_screen)

        show_fps()
        scale_n_build_screen()


def terminate(event):
    if (
        event.type == pygame.QUIT
        or event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE
    ):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
