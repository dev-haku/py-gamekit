from dataclasses import dataclass

import pygame

from .collision_system import CollisionSystem
from .component import Component
from ..components.transform import Transform


@dataclass
class Hitbox:
    offset_position: tuple[int,int]
    size: tuple[int,int]
    color: tuple[int,int,int]
        

class Collider(Component):

    def __init__(self, context):
        super().__init__(context)
        
        self._hitboxes: list[Hitbox] = []

        self._parent_transform: Transform = self.parent.get_component("Transform")
        self._collider_system: CollisionSystem = self.scene.get_gameobject("CollisionSystem")
             
        if self.engine.debug_config.show_colliders:
            self.render_data.active = True
            self.render_data.transform_type = self._parent_transform.__class__.__name__

    @property
    def hitboxes(self) -> list[Hitbox]:
        return self._hitboxes.copy()

    def add_hitbox(
            self, 
            offset_position: tuple[float,float], 
            size: tuple[float,float], 
            color: tuple[float,float,float,float] = (0,255,0, 200)
        ):
        self._hitboxes.append(Hitbox(offset_position, size, color))

    def clear_all_hitboxes(self):
        self._hitboxes.clear()

    def is_colliding(self):
        if len(self._collider_system.get_colliding_colliders(self)) >= 1:
            return True
        else:
            return False
    
    def get_colliding_gameobjects(self):
            return [collider.parent for collider in self._collider_system.get_colliding_colliders(self)]
                
    def update(self):
        if self.render_data.active:
            self._update_debug_surface()

        return super().update()
    
    def _update_debug_surface(self) -> None:

        position = self._parent_transform.position
        scale = self._parent_transform.scale

        scaled_hitboxes = [
            (
                hitbox.offset_position[0] * scale[0],
                hitbox.offset_position[1] * scale[1],
                hitbox.size[0] * scale[0],
                hitbox.size[1] * scale[1],
                hitbox.color
                )
            for hitbox in self.hitboxes
        ]

        first = scaled_hitboxes[0]

        left = first[0]
        top = first[1]
        right = first[0] + first[2]
        bottom = first[1] + first[3]

        for hitbox in scaled_hitboxes:
            left = min(left, hitbox[0])
            top = min(top, hitbox[1])
            right = max(right, hitbox[0] + hitbox[2])
            bottom = max(bottom, hitbox[1] + hitbox[3])

        x = left
        y = top
        w = right - left
        h = bottom - top

        combined_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        combined_surface.fill((255,255,255,0))

        for hitbox in scaled_hitboxes:
            hitbox_surface = pygame.Surface((hitbox[2],hitbox[3]), pygame.SRCALPHA)
            hitbox_surface.fill(hitbox[4])
            combined_surface.blit(hitbox_surface, (hitbox[0] - x, hitbox[1] - y))

        self.render_data.active = True
        self.render_data.surface = combined_surface
        self.render_data.position.xy = (position.x + x, position.y + y)
        self.render_data.layer = self._parent_transform.layer +1