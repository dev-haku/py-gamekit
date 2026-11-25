from ..package import Scene, Square, Text
from .player import Player


class GameScene(Scene):

    def __init__(self, engine) -> None:
        super().__init__(engine)

        _camera = self.get_gameobject("Camera")
        _camera.anchor = (0.5,0.5)
        _camera.zoom = 1

        self.add_gameobject(
            Player, 
            position= (0,0), 
            scale= (4,4), 
            layer= 4,
            move_speed= 16
        )

        self.add_gameobject(
            Square, 
            position=(100,0), 
            scale=(20,20), 
            layer=1, 
            color=(0,0,255), 
            hitbox_color=(0,255,0,200)
        )

        self.add_gameobject(
            Square, 
            position=(-200,0), 
            scale=(20,20), 
            layer=1, 
            color=(0,0,255), 
            hitbox_color=(0,255,0,200)
        )

        self.add_gameobject(
            Text,
            position= (0.6,0.9),
            scale= (1,1),
            layer= 0,
            text= "Hello World",
            size= 100,
            color= (255,255,255),
            init_active= True
        )