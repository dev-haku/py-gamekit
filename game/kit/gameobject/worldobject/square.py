import pygame

from game.kit.gameobject.worldobject.base_worldobject import BaseWorldobject
from game.kit.component.sprite_renderer import SpriteRenderer
from game.kit.component.collider import Collider

class Square(BaseWorldobject):
    def __init__(
            self, 
            position: tuple[float,float], 
            scale: tuple[float,float], 
            layer: int,
            color: tuple[int,int,int] = (255,255,255)
        ):
        super().__init__()
        transfrom = self.get_component("Transform")
        transfrom.position = position
        transfrom.scale = scale
        transfrom.layer = layer

        sprite = SpriteRenderer()
        surface = pygame.Surface((8,8))
        surface.fill(color)
        sprite.set_surface(surface)
        self.add_component(sprite)

        collider = Collider()
        collider.add_hitbox((0,0),(8,8), (255,255,255))
        self.add_component(collider)