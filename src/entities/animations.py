import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos, frames, speed=8):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed  # how fast animation plays

    def update(self, dt):
        self.frame_index += self.speed * dt
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
