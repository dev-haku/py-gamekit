import pygame
import json

from game import paths
from game.package.base_objects import Worldobject, Component
from game.package.components import SpriteRenderer, Animator, Collider

class Player(Worldobject):

    def __init__(self, position:tuple, scale:tuple, layer:int,):
        super().__init__()
        
        transform = self.get_component("Transform")
        transform.position = position
        transform.scale = scale
        transform.layer = layer

        self.add_component(SpriteRenderer())

        animator = Animator()

        with open(paths.APP_ASSET_DIR / "player/animations_data.json", "r") as f:
            data = json.load(f)

        for name, info in data.items():
            frames: list[pygame.Surface] = []
            spritesheet_surface = pygame.image.load(paths.APP_ASSET_DIR / info["spritesheet_image_path"])
            for frame_info in info["frames"]:
                x, y, w, h = frame_info
                crop_area = pygame.Rect(x*w, y*h, w, h)
                cropped_surface = spritesheet_surface.subsurface(crop_area)
                frames.append(cropped_surface)

            animator.add_animation(name, frames, info["fps"],  info["is_loop"])

        self.add_component(animator)

        collider = Collider()
        collider.is_collision_enabled = False
        collider.add_hitbox((-0,-0), (14,14), (0,255,0,100))
        self.add_component(collider)

        state = State() 
        state.speed = 5
        self.add_component(state)
        
        self.add_component(Controller())
        

class State(Component):
    def __init__(self):
        super().__init__()
        
class Controller(Component):

    def start(self):
        self.transform = self.parent.get_component("Transform")
        self.sprite_renderer = self.parent.get_component("SpriteRenderer")
        self.animator: Animator = self.parent.get_component("Animator")
        self.collider: Collider = self.parent.get_component("Collider")
        self.state: State = self.parent.get_component("State")

        self.camera = self.engine.current_scene.camera

        return super().start()
    
    def update(self):
        keys = self.engine.input_status.keys
        dt = self.engine.delta_time

        camera_transform = self.camera.get_component("Transform")

        w, h = self.animator.animation_player.get_current_frame().get_size()
        scaled_size = (
            w * self.transform.scale.x, 
            h * self.transform.scale.y
        )

        state = self.state

        if keys.get("w", False):
            self.transform.position.y -= (scaled_size[1] / 2) * state.speed * dt
            self.animator.change_animation("up_walk", True)
            if self.collider.is_colliding():
                self.transform.position.y += (scaled_size[1] / 2) * state.speed * dt

        if keys.get("s", False):
            self.transform.position.y += (scaled_size[1] / 2) * state.speed * dt
            self.animator.change_animation("down_walk", True)
            if self.collider.is_colliding():
                self.transform.position.y -= (scaled_size[1] / 2) * state.speed * dt

        if keys.get("a", False):
            self.transform.position.x -= (scaled_size[0] / 2) * state.speed * dt
            self.animator.change_animation("left_walk", True)
            if self.collider.is_colliding():
                self.transform.position.x += (scaled_size[0] / 2) * state.speed * dt
        
        if keys.get("d", False):
            self.transform.position.x += (scaled_size[0] / 2) * state.speed * dt
            self.animator.change_animation("right_walk", True)
            if self.collider.is_colliding():
                self.transform.position.x -= (scaled_size[0] / 2) * state.speed * dt


        camera_transform.position = (
            self.transform.position.x + (scaled_size[0] // 2),
            self.transform.position.y + scaled_size[1] // 2
        )
        
        return super().update()