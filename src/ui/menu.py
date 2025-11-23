import pygame


class Menu:
    """ """

    def __init__(self, size: tuple, color: tuple):
        self.menu_surface = pygame.Surface(size)
        self.menu_surface.fill(color)
        self.color = color
        self.components = []
        self.blit_sequence: list = []

    def center_buttons(self, screen_rect, gap=40):
        """

        Args:
          screen_rect: 
          gap:  (Default value = 40)

        Returns:

        """
        total_height = sum(btn.rect.height for btn in self.components) + gap * (
            len(self.components) - 1
        )

        start_y = screen_rect.centery - total_height // 2
        current_y = start_y

        for btn in self.components:
            btn.rect = btn.surface.get_rect(
                center=(screen_rect.centerx, current_y + btn.rect.height // 2)
            )
            current_y += btn.rect.height + gap

            self.blit_sequence.append((btn.surface, btn.rect))

    def blit(self, surface: pygame.Surface):
        """

        Args:
          surface: pygame.Surface: 

        Returns:

        """
        rect = self.menu_surface.get_rect(center=surface.get_rect().center)
        surface.blit(self.menu_surface, rect)

    def blits(self, surface):
        """

        Args:
          surface: 

        Returns:

        """
        surface.fill(self.color)

        for button in self.components:
            surface.blit(button.surface, button.rect)
