from typing import Sequence

import pygame


class Explosion(pygame.sprite.Sprite):
    """Animated explosion effect for destroyed objects.

    Handles frame-based animation playback and self-removal once
    the animation finishes.

    Attributes:
        frames (Sequence[pygame.Surface]): List of animation frames.
        frame_index (float): Current animation index (supports fractional progress).
        image (pygame.Surface): Currently displayed frame.
        rect (pygame.Rect): Position and collision rectangle.
        speed (float): Playback speed multiplier (higher = faster animation).
    """

    def __init__(
        self, pos: tuple[int, int], frames: Sequence[pygame.Surface], speed: float = 8.0
    ) -> None:
        """Initialize an explosion animation at a given position.

        Args:
            pos (tuple[int, int]): (x, y) center position of the explosion.
            frames (Sequence[pygame.Surface]): List of animation frames.
            speed (float, optional): Animation playback speed multiplier.
                Defaults to 8.0.
        """
        super().__init__()

        self.frames: Sequence[pygame.Surface] = frames
        self.frame_index: float = 0.0
        self.speed: float = speed

        self.image: pygame.Surface = self.frames[int(self.frame_index)]
        self.rect: pygame.Rect = self.image.get_rect(center=pos)

    def update(self, dt: float) -> None:
        """Advance the explosion animation.

        Once all frames have been shown, the explosion sprite removes itself.

        Args:
            dt (float): Delta time factor controlling animation speed.
        """
        # Advance animation
        self.frame_index += self.speed * dt

        # Remove when done
        if self.frame_index >= len(self.frames):
            self.kill()
            return

        # Update current frame
        self.image = self.frames[int(self.frame_index)]
