import pygame

from ...paths import CB_IMAGE


class RenderData:
    def __init__(self):
        self.active = False
        self.transform_type = None
        self.surface: pygame.Surface = pygame.image.load(CB_IMAGE)
        self.position: pygame.Vector2 = pygame.Vector2()
        self.layer: int = 0