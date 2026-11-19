from dataclasses import dataclass
import pygame

from .render_data import RenderData
from .collision_system import CollisionSystem
from .component import Component
from .transform import Transform


@dataclass
class Hitbox:
    offset_position: tuple[int,int]
    size: tuple[int,int]
    color: tuple[int,int,int]
        

class Collider(Component):
    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)
        
        self.hitboxes: list[Hitbox] = []
        self.last_pos: tuple[float,float] = (0,0)

        self.parent_transform: Transform = self.parent.get_component("Transform")

        self.render_data = RenderData()
        self.render_data.transform_type = self.parent_transform.__class__.__name__

        self.collider_system: CollisionSystem = self.scene.get_gameobject("CollisionSystem")

    def add_hitbox(
            self, 
            offset_position: tuple[float,float], 
            size: tuple[float,float], 
            color: tuple[float,float,float,float] = (0,255,0, 200)
        ):
        self.hitboxes.append(Hitbox(offset_position, size, color))

    def clear_all_hitboxes(self):
        self.hitboxes.clear()

    def is_colliding(self):
        if len(self.collider_system.get_colliding_colliders(self)) >= 1:
            return True
        else:
            return False
    
    def get_colliding_gameobjects(self):
            return [c.parent for c in self.collider_system.get_colliding_colliders(self)]
    
                
    def update(self):
        if self.engine.debug_settings["show_colliders"]:
            self._update_debug_surface()

        return super().update()
    
    def _update_debug_surface(self) -> None:

        position = self.parent_transform.position
        scale = self.parent_transform.scale


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

        self.render_data.surface = combined_surface
        self.render_data.position.xy = (position.x + x, position.y + y)
        self.render_data.layer = self.parent_transform.layer +1