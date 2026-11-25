import pygame

from .gameobject import Gameobject
from .transform import Transform

from .exceptions import PyGamekitError

class Camera(Gameobject):
    
    def __init__(self, engine, scene, parent, name):
        super().__init__(engine, scene, parent, name)
        self.tags.append("camera")
        self.add_component(Transform)

        self._anchor = pygame.Vector2()
        self._pos_ratio: tuple = (0,0)
        self._zoom: int = 1

    @property
    def anchor(self) -> pygame.Vector2:
        return self._anchor

    @anchor.setter
    def anchor(self, value: tuple[float, float]):
        self._pos_ratio = (
            max(0.0, min(1.0, value[0])), 
            max(0.0, min(1.0, value[1]))
        )  

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: int):
        if value == 0:
            raise PyGamekitError("Camera: zoom は 0より大きい値にしてください。")
        
        self._zoom = value

    def update(self):
        world_screen_size = (
            self.engine.screen_size[0] // self._zoom,
            self.engine.screen_size[1] // self._zoom
        )

        self._anchor = pygame.Vector2(
            world_screen_size[0] * self._pos_ratio[0],
            world_screen_size[1] * self._pos_ratio[1]
        )

        return super().update()