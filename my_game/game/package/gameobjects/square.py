import pygame

from ..core.collider import Collider
from ..core.gameobject import Gameobject
from ..components.sprite_renderer import SpriteRenderer
from ..components.transform import Transform


class Square(Gameobject):
    def __init__(
        self, 
        context,
        position: tuple[float,float], 
        scale: tuple[float,float], 
        layer: int, 
        color: tuple[int,int,int], 
        hitbox_color: tuple[int,int,int]
    ):
        super().__init__(context)
        
        transfrom: Transform = self.add_component(Transform)
        transfrom.position = position
        transfrom.scale = scale
        transfrom.layer = layer

        surf = pygame.Surface((8,8))
        surf.fill(color)
        self.add_component(SpriteRenderer, surface= surf)

        collider: Collider = self.add_component(Collider)
        collider.add_hitbox((0,0),(8,8), (hitbox_color))