import pygame

from game.kit.gameobject.uiobject.base_uiobject import BaseUiobject
from game.kit.component.sprite_renderer import SpriteRenderer

class Image(BaseUiobject):
    def __init__(self, position, size, scale, layer):
        super().__init__()

        transform = self.get_component("RectTransform")
        transform.position = position
        transform.scale = scale

        sprite = SpriteRenderer()
        surface = pygame.Surface(size)
        surface.fill((255,255,255))
        sprite.set_surface(surface)
        self.add_component(sprite)