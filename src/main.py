import sys

import pygame

pygame.init()

from config import Config as config
from game_state import GameState
from ui.button import Button
from ui.menu import Menu
from utils.helpers import scale_n_build_screen, show_fps


def main(initial_state="Menu"):
    state = initial_state

    while True:
        if state == "Menu":
            state = menu_loop()
        elif state == "Start":
            state = game_loop()
        elif state in ("Quit", "Exit"):
            terminate()
        else:
            # unknown state -> go to menu
            state = "Menu"


def update_game(state: GameState):
    main_plane = state.player
    enemies_group = state.enemies_group
    enemies_bullets_group = state.enemies_bullets_group
    explosions_group = state.explosions_group

    # ---- Input ----
    keys = pygame.key.get_pressed()
    main_plane.move(keys, config.delta_time)

    mouse = pygame.mouse.get_pressed()
    main_plane.shoot(mouse)

    main_plane.bullets_group.update(config.delta_time)

    # ---- Enemies ----
    enemies_group.update()
    for enemy in enemies_group:
        enemy.auto_move()
        enemy.shoot()

    for bullet in enemies_bullets_group:
        bullet.update(config.delta_time)

    # ---- Collisions ----
    hits = pygame.sprite.groupcollide(
        enemies_group, main_plane.bullets_group, False, True, pygame.sprite.collide_mask
    )
    for enemy, bullets in hits.items():
        enemy.take_damage(bullets, explosions_group, main_plane.gun.bullet_damage)

    player_hits = pygame.sprite.groupcollide(
        state.player_group,
        pygame.sprite.Group(*[e.bullets_group for e in enemies_group]),
        False,
        True,
        pygame.sprite.collide_mask,
    )
    if player_hits:
        main_plane.take_damage(
            player_hits,
            explosions_group,
            enemy.gun.bullet_damage if enemies_group else 1,
        )

    # ---- Next Wave ----
    if len(enemies_group) == 0:
        state.enemy_manager.next_wave()
        state.enemies_group = state.enemy_manager.get_current_group()

    # ---- Player died ----
    if not state.player_group:
        return "Menu"

    # ---- Draw ----
    state.player_group.draw(config.v_screen)
    main_plane.bullets_group.draw(config.v_screen)
    enemies_group.draw(config.v_screen)
    for enemy in enemies_group:
        enemy.bullets_group.draw(config.v_screen)

    explosions_group.update(config.delta_time)
    explosions_group.draw(config.v_screen)

    return None


def menu_loop():
    """
    Runs the menu frame loop and returns the next state string: "Start", "Settings", "Quit", etc.
    """
    # ---- Main Menu ----
    main_menu = Menu((config.VIRTUAL_WIDTH, config.VIRTUAL_HEIGHT), (255, 255, 0))

    start_button = Button("Start", (200, 50))
    setting_button = Button("Setting", (200, 50))
    quit_button = Button("Quit", (200, 50))

    def start_button_handler():
        return "Start"

    def setting_button_handler():
        return "Settings"

    def quit_button_handler():
        return "Quit"

    start_button.handler = start_button_handler
    setting_button.handler = setting_button_handler
    quit_button.handler = quit_button_handler

    main_menu.components = [start_button, setting_button, quit_button]
    main_menu.center_buttons(config.v_screen_rect, gap=20)

    # main menu loop
    while True:
        config.v_screen.fill((0, 0, 0))
        main_menu.blits(config.v_screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Quit"

            if start_button.is_clicked(event):
                return start_button.handler()
            if setting_button.is_clicked(event):
                return setting_button.handler()
            if quit_button.is_clicked(event):
                return quit_button.handler()

        scale_n_build_screen()


def game_loop():
    state = GameState()  # initialize once

    while True:
        dt = config.clock.tick()
        config.delta_time = dt / 1000.0
        config.v_screen.fill((0, 0, 0))

        # input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "Menu"

        next_state = update_game(state)
        if next_state:
            return next_state

        show_fps()
        scale_n_build_screen()


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
