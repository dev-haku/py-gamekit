from ..package import Scene, Square
from .player import Player


class GameScene(Scene):

    def __init__(self, engine):
        super().__init__(engine)

        camera = self.get_gameobject("Camera")
        camera.anchor = (0.5,0.5)

        self.add_gameobject(
            Player, 
            position= (-100,0), 
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
            hitbox_color=(0,255,0)
        )