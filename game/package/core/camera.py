import pygame

from .gameobject import Gameobject
from .transform import Transform


class Camera(Gameobject):
    
    def __init__(self, engine, scene, kwargs):
        super().__init__(engine, scene, kwargs)

        self.tags.append("camera")
        self.add_component(Transform)
        self._anchor = pygame.Vector2()
        self.pos_ratio: tuple = (0,0)
        self._zoom: int = 1

    @property
    def anchor(self) -> pygame.Vector2:
        return self._anchor

    @anchor.setter
    def anchor(self, value: tuple[float, float]):
        self.pos_ratio = (
            max(0.0, min(1.0, value[0])), 
            max(0.0, min(1.0, value[1]))
        )  

    def update(self):
        screen_size = self.scene.screen.get_size()

        self._anchor = pygame.Vector2(
            screen_size[0] * self.pos_ratio[0],
            screen_size[1] * self.pos_ratio[1]
        )

        return super().update()

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value: int):
        if not value == 0:
            self._zoom = value
            self.scene.set_screen_size()

    
