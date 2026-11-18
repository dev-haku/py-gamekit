import pygame

from src.package import (
    Gameobject,
    Component, 
    Transform,
    SpriteRenderer, 
    Animator, 
    Collider
)


class Player(Gameobject):

    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

        self.move_speed = kwargs["move_speed"]
        
        transform = self.add_component(Transform)
        transform.position = kwargs["position"]
        transform.scale = kwargs["scale"]
        transform.layer = kwargs["layer"]

        surf = pygame.Surface((8,8))
        surf.fill((255,0,0))
        self.add_component(SpriteRenderer, surface=surf)

        collider = self.add_component(Collider)
        collider.is_collision_enabled = False
        collider.add_hitbox((-0,-0), (8,8), (0,255,0,100))
        
        self.add_component(Controller)
  
        
class Controller(Component):

    def __init__(self, engine, scene, parent, kwargs):
        super().__init__(engine, scene, parent, kwargs)

        self.keys = self.engine.input_status.keys

        self.parent_transform: Transform = self.parent.get_component("Transform")
        self.parent_sprite_renderer: SpriteRenderer = self.parent.get_component("SpriteRenderer")
        self.parent_collider: Collider = self.parent.get_component("Collider")

        self.camera = self.scene.get_gameobject("Camera1")

        self.last_pos = 0

    def update(self):

        dt = self.engine.delta_time

        scaled_size = self.parent_sprite_renderer.scaled_size

        m = {
            "w" : (0,-(scaled_size[1] / 2) * self.parent.move_speed * dt),
            "s" : (0,(scaled_size[1] / 2) * self.parent.move_speed * dt),
            "a" : (-(scaled_size[0] / 2) * self.parent.move_speed * dt,0),
            "d" : ((scaled_size[0] / 2) * self.parent.move_speed * dt,0)
        }

        if self.parent_collider.is_colliding():
            self.parent_transform.position.xy = self.last_pos
        else:
            self.last_pos = self.parent_transform.position.xy

        for key in m:
            
            if self.keys.get(key, False):
                x, y = m.get(key)
                self.parent_transform.position.x += x
                self.parent_transform.position.y += y
       

        self.parent_transform.position.xy = round(self.parent_transform.position.xy)

        camera = self.engine.current_scene.get_gameobject("Camera")
        camera_transform = camera.get_component("Transform")
        camera_transform.position = (
            self.parent_transform.position.x + scaled_size[0] //2,
            self.parent_transform.position.y + scaled_size[1] //2
            )
        
        return super().update()