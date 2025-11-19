import pygame

pygame.init()

import sys

from config import Config as config
from entities.enemy_manager import EnemyManager
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

    # Position player
    main_plane.rect.bottom = config.v_screen_rect.bottom * 0.9
    main_plane.rect.centerx = config.v_screen_rect.centerx

    player_group = pygame.sprite.Group(main_plane)

    # -----------------------------------------------------------------------------
    # Enemies
    enemies_bullets_group = pygame.sprite.Group()
    enemy_manager = EnemyManager(enemies_bullets_group)
    enemy_manager.load_wave()
    enemies_current_group = enemy_manager.get_current_group()

    explosions_group = pygame.sprite.Group()

    while True:
        config.v_screen.fill((0, 0, 0))

        dt = config.clock.tick(config.FPS)
        delta_time = dt / 16.67

        for event in pygame.event.get():
            terminate(event)

        # ---- Player Logic ----
        keys = pygame.key.get_pressed()
        main_plane.move(keys)

        mouse = pygame.mouse.get_pressed()
        main_plane.shoot(mouse)

        main_plane.bullets_group.update()

        # ---- Enemy Updates ----
        enemies_current_group.update()

        for enemy_plane in enemies_current_group:
            enemy_plane.shoot()

        for enemy_bullet in enemies_bullets_group:
            enemy_bullet.update()

        # ---- Collision: Player → Enemy ----
        hits_on_enemies = pygame.sprite.groupcollide(
            enemies_current_group,
            main_plane.bullets_group,
            False,
            True,
            pygame.sprite.collide_mask,
        )
        for enemy, bullets in hits_on_enemies.items():
            enemy.take_damage(bullets, explosions_group, main_plane.gun.bullet_damage)

        # ---- Collision: Enemy → Player ----
        for enemy_plane in enemies_current_group:
            hits_on_player = pygame.sprite.groupcollide(
                player_group,
                enemy_plane.bullets_group,
                False,
                True,
                pygame.sprite.collide_mask,
            )
            if hits_on_player:
                main_plane.take_damage(
                    hits_on_player,
                    explosions_group,
                    enemy_plane.gun.bullet_damage,
                )

            enemy_plane.auto_move()

        if len(enemies_current_group) == 0:
            enemy_manager.next_wave()

        # ---- Update explosion animations ----
        explosions_group.update(delta_time)

        if len(player_group) == 0:
            main("L")

        # ---- Draw Everything ----
        player_group.draw(config.v_screen)
        main_plane.bullets_group.draw(config.v_screen)

        enemies_current_group.draw(config.v_screen)
        for enemy_plane in enemies_current_group:
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
