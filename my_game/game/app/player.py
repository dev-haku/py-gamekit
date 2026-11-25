import pygame

from ..package import (
    Gameobject,
    Component,
    Transform,
    SpriteRenderer,
    Collider
)


class Player(Gameobject):

    def __init__(
        self, 
        engine, 
        scene, 
        parent, 
        name,
        position: tuple[float,float], 
        scale: tuple[float,float], 
        layer: int, 
        move_speed: int
    ) -> None:
        super().__init__(engine, scene, parent, name)
        
        self.transform = self.add_component(Transform)
        self.transform.position = position
        self.transform.scale = scale
        self.transform.layer = layer

        surf = pygame.Surface((8,8))
        surf.fill((255,0,0))
        self._sprite_renderer = self.add_component(
            SpriteRenderer, 
            surface= surf
        )

        collider = self.add_component(Collider)
        collider.is_collision_enabled = False
        collider.add_hitbox((0,0), (8,8), (0,255,0,100))
        
        self.add_component(Controller)

        self.move_speed = move_speed

        camera = self.scene.get_gameobject("Camera")
        self._camera_transform = camera.get_component("Transform")

    def update(self):

        scaled_size = self._sprite_renderer.scaled_size
        
        self._camera_transform.position = (
            self.transform.position.x + scaled_size[0] // 2,
            self.transform.position.y + scaled_size[1] // 2
        )
        
        return super().update()
  
        
class Controller(Component):

    def __init__(self, engine, scene, parent) -> None:
        super().__init__(engine, scene, parent)

        self._parent_transform: Transform = self.parent.get_component("Transform")
        self._parent_sprite_renderer: SpriteRenderer = self.parent.get_component("SpriteRenderer")
        self._parent_collider: Collider = self.parent.get_component("Collider")

        self._last_pos: tuple[float,float] = (0,0)

    def update(self) -> None:

        dt = self.engine.delta_time

        scaled_size = self._parent_sprite_renderer.scaled_size

        m = {
            "w" : (
                0,
                -(scaled_size[1] / 2) * self.parent.move_speed * dt
            ),
            "s" : (
                0,
                (scaled_size[1] / 2) * self.parent.move_speed * dt
            ),
            "a" : (
                -(scaled_size[0] / 2) * self.parent.move_speed * dt,
                0
            ),
            "d" : (
                (scaled_size[0] / 2) * self.parent.move_speed * dt,
                0
            )
        }

        if self._parent_collider.is_colliding():
            self._parent_transform.position.xy = self._last_pos
        else:
            self._last_pos = self._parent_transform.position.xy

        for key in m:
            
            if self.engine.keyboard.pressed(key):
                x, y = m[key]
                self._parent_transform.position.x += x
                self._parent_transform.position.y += y

        return super().update()