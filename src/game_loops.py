import pygame

from config import Config as config
from game_types import GameStateTypes
from ui.button import Button
from ui.menu import Menu
from utils.helpers import scale_n_build_screen


def menu_loop():
    """Runs the menu frame loop and returns the next state string: "Start", "Settings", "Quit", etc."""

    # ---- Main Menu ----
    main_menu = Menu((config.VIRTUAL_WIDTH, config.VIRTUAL_HEIGHT), (255, 255, 0))

    start_button = Button("Start", (200, 50))
    setting_button = Button("Setting", (200, 50))
    quit_button = Button("Quit", (200, 50))

    start_button.state = GameStateTypes.START
    setting_button.state = GameStateTypes.SETTING
    quit_button.state = GameStateTypes.QUIT

    main_menu.components = [start_button, setting_button, quit_button]
    main_menu.center_buttons(config.v_screen_rect, gap=20)

    # main menu loop
    while True:
        config.v_screen.fill((0, 0, 0))
        main_menu.blits(config.v_screen)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameStateTypes.QUIT
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return GameStateTypes.EXIT

            if start_button.is_clicked(event):
                return start_button.state
            if setting_button.is_clicked(event):
                return setting_button.state
            if quit_button.is_clicked(event):
                return quit_button.state

        scale_n_build_screen()
