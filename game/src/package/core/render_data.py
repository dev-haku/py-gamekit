import pygame
from src.paths import CB_IMAGE

class RenderData:
    def __init__(self):
        self.surface: pygame.Surface = pygame.image.load(CB_IMAGE)
        self.position: pygame.Vector2 = pygame.Vector2()
        self.layer: int = 0
        self.transform_type = None