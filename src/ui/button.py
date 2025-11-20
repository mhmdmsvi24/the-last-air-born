import pygame

from config import Config as config


class Button:
    def __init__(self, text: str, size: tuple):
        self.text = text
        self.size = size

        # button text & font
        self.button_text = config.font.render(text, False, (0, 255, 255))
        # Final button creation
        self.surface = pygame.Surface(size)
        self.surface.fill((0, 0, 255))

        self.rect = self.surface.get_rect(center=config.v_screen_rect.center)

        text_rect = self.button_text.get_rect(center=self.surface.get_rect().center)

        self.surface.blit(self.button_text, text_rect)

    def is_clicked(self, event):
        """Returns True when button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # because the menu is drawn on virtual width the event.pos is not the same as button.rect positions
            mx, my = event.pos

            scaled_x = mx * (config.VIRTUAL_WIDTH / config.REAL_WIDTH)
            scaled_y = my * (config.VIRTUAL_HEIGHT / config.REAL_HEIGHT)

            if self.rect.collidepoint((scaled_x, scaled_y)):
                return True
        return False

    def blit(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)
