import pygame

from ..core.gameobject import Gameobject
from ..core.transform import Transform
from ..core.sprite_renderer import SpriteRenderer
from ..core.collider import Collider


class Square(Gameobject):
    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

        transfrom: Transform = self.add_component(Transform)
        transfrom.position = kwargs["position"]
        transfrom.scale = kwargs["scale"]
        transfrom.layer = kwargs["layer"]

        surf = pygame.Surface((8,8))
        surf.fill(kwargs["color"])
        sprite_renderer: SpriteRenderer = self.add_component(SpriteRenderer)
        sprite_renderer.surface = surf

        collider: Collider = self.add_component(Collider)
        collider.add_hitbox((0,0),(8,8), (kwargs["hitbox_color"]))