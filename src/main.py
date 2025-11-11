import pygame

pygame.init()

import sys

from config import Config as config
from entities.planes import Enemy, Player
from utils.helpers import load_image, scale_image, scale_n_build_screen, show_fps


def main(state="P"):

    if state == "P":
        game_loop()
    elif state == "L":
        game_loop()


def game_loop():
    # Player
    main_plane_img = scale_image(load_image("graphics", "plane-1.webp"), 30, 55)
    main_plane = Player(config.v_screen, 5, 1, main_plane_img)

    # center the plane in lower center
    main_plane.rect.bottom = config.v_screen_rect.bottom * 0.9
    main_plane.rect.centerx = config.v_screen_rect.centerx

    # All the player side assets like plane, future helper planes, ... for collision detection
    player_group = pygame.sprite.Group()
    player_group.add(main_plane)
    # -----------------------------------------------------------------------------

    # Enemies
    enemy_plane_img = pygame.transform.rotate(
        scale_image(load_image("graphics", "enemy-2.webp"), 30, 55), 180
    )
    enemy_plane = Enemy(config.v_screen, 6, 10, enemy_plane_img)

    # center the enemy plane in lower center
    # *FIX: this just centers a single plane for future planes groups that will spawn a better method is required
    enemy_plane.rect.bottom = config.v_screen_rect.bottom * 0.2
    enemy_plane.rect.centerx = config.v_screen_rect.centerx

    # enemies bullets and groups for collision detection
    enemies_group = pygame.sprite.Group()
    enemies_group.add(enemy_plane)

    explosions_group = pygame.sprite.Group()

    while True:
        # Clear and fill screen
        config.v_screen.fill((0, 0, 0))

        dt = config.clock.tick(config.FPS)
        delta_time = dt / 16.67

        for event in pygame.event.get():
            terminate(event)

        main_plane.move(pygame.key.get_pressed())
        main_plane.shoot(pygame.mouse.get_pressed())
        main_plane.bullets_group.update()

        enemy_plane.shoot()
        enemy_plane.bullets_group.update()

        # check if any of the players bullets hit enemy planes
        player_damage_enemy = pygame.sprite.groupcollide(
            enemies_group,
            main_plane.bullets_group,
            False,
            True,
            pygame.sprite.collide_mask,
        )

        # Check if any of the enemy bullets hit player plane
        enemy_damage_player = pygame.sprite.groupcollide(
            player_group,
            enemy_plane.bullets_group,
            False,
            True,
            pygame.sprite.collide_mask,
        )

        if player_damage_enemy:
            enemy_plane.take_damage(
                player_damage_enemy, explosions_group, main_plane.gun.bullet_damage
            )
        elif enemy_damage_player:
            main_plane.take_damage(
                enemy_damage_player, explosions_group, enemy_plane.gun.bullet_damage
            )

        # update animations
        explosions_group.update(delta_time)

        player_group.draw(config.v_screen)
        enemies_group.draw(config.v_screen)
        main_plane.bullets_group.draw(config.v_screen)
        enemy_plane.bullets_group.draw(config.v_screen)
        explosions_group.draw(config.v_screen)

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
