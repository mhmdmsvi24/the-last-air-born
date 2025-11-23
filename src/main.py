import pygame

pygame.init()

from config import Config as config
from game_loops import menu_loop
from game_state import GameState
from game_types import GameStateTypes
from utils.helpers import scale_n_build_screen, show_fps
from utils.utils import terminate


def main(initial_state: GameStateTypes = GameStateTypes.DEFAULT) -> None:
    """Each function like menu_loop or game_loop must return an state at the end

    Args:
      initial_state:  (Default value = "Menu")

    Returns:
        None
    """

    state = initial_state

    while True:
        if state is GameStateTypes.MENU:
            state = menu_loop()
        elif state is GameStateTypes.START:
            state = game_loop()
        elif state in (GameStateTypes.QUIT, GameStateTypes.EXIT):
            terminate()
        else:
            state = GameStateTypes.MENU


def update_game(state: GameState) -> None | GameStateTypes:
    """Runs a single frame of the game

    Args:
      state: GameState

    Returns:
      None: on successful run
      state (str): changed state
    """

    main_plane = state.player
    enemies_group = state.enemies_group
    enemies_bullets_group = state.enemies_bullets_group
    explosions_group = state.explosions_group

    # ---- Input ----
    keys = pygame.key.get_pressed()
    main_plane.move(keys, config.delta_time)

    mouse = pygame.mouse.get_pressed()
    main_plane.shoot(mouse)

    # ---- Effects ----
    main_plane.bullets_group.update(config.delta_time)

    # ---- Enemies AI ----
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
        return GameStateTypes.MENU

    # ---- Draw ----
    state.player_group.draw(config.v_screen)
    main_plane.bullets_group.draw(config.v_screen)
    enemies_group.draw(config.v_screen)
    for enemy in enemies_group:
        enemy.bullets_group.draw(config.v_screen)

    explosions_group.update(config.delta_time)
    explosions_group.draw(config.v_screen)

    return None


def game_loop() -> GameStateTypes:
    """Main Loop of the game, manages the update_game function gives control to the main"""
    state = GameState()  # initialize once

    while True:
        dt = config.clock.tick()
        config.delta_time = dt / 1000.0
        config.v_screen.fill((0, 0, 0))

        # input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameStateTypes.QUIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameStateTypes.EXIT

        next_state = update_game(state)

        # update_game returns None while the player is playing, otherwise next_state will be returned, resulting in returning to main function
        if next_state:
            return next_state

        show_fps()
        scale_n_build_screen()


if __name__ == "__main__":
    main()
